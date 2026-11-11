"""Browser side of the Grammatip automation.

Everything that touches the page lives here: extracting the captcha image and
audio from the STIL gateway, answering it, walking the UniLogin picker, filling
the credentials and finally opening the student area.

The gateway's quirks (measured, not guessed):

* each submission returns a fresh 6 character challenge, so one session can be
  kept alive for many rounds
* a wrong answer is answered "Koden var forkert"; nothing is locked out, and
  retries within the session are cheap
* roughly one submission in five is answered with "Der er opstået en fejl"
  instead, which kills that session's token; it is not caused by pacing or by
  reading the page's media, so the only response is to start a new session
* after the second gateway the "Loginvælger" page is shown again, and clicking
  "Lokalt login" a second time is what reveals the username/password form
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import subprocess
import time
import urllib.request
import wave

import numpy as np
from playwright.async_api import Page, async_playwright

import captcha_solver as solver

GRAMMATIP = "https://www.grammatip.com"
UNILOGIN = f"{GRAMMATIP}/unilogin"
STUDENT = f"{GRAMMATIP}/student"

WHISPER_MODELS = ("small.en", "base.en")
WHISPER_PROMPTS = (
    "The speaker spells a code of six characters, letters and digits.",
    "One letter or digit at a time, for example A, B, C, D, E, F.",
)
RESTART_PAUSE = 2.0    # seconds to wait before asking for a fresh challenge

_models: dict[str, object] = {}


def _whisper(name: str):
    if name not in _models:
        from faster_whisper import WhisperModel

        _models[name] = WhisperModel(name, device="cpu", compute_type="int8")
    return _models[name]


# Minimum spacing between captcha submissions, across the whole process.
#
# This is enforced globally (not per session) because the limit is per client,
# not per browser context: submitting from two contexts at once still trips it.
# Measured: 8 s apart produced "Der er opstået en fejl" on ~20% of submissions
# (which permanently kills that session's token), while 20 s and 45 s apart
# produced none in 12 consecutive submissions.
SUBMIT_INTERVAL = float(os.environ.get("GT_THROTTLE", "22"))
_last_submit = 0.0


async def _respect_interval() -> None:
    """Block until SUBMIT_INTERVAL has passed since the last submission."""
    global _last_submit
    remaining = SUBMIT_INTERVAL - (time.time() - _last_submit)
    if remaining > 0:
        await asyncio.sleep(remaining)
    _last_submit = time.time()


def transcribe(mp3_path: str, model_name: str, prompt: str) -> str:
    wav_path = f"{mp3_path}.{model_name}.wav"
    if not os.path.exists(wav_path):
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", mp3_path, "-ar", "16000", "-ac", "1",
             wav_path],
            check=True,
            stderr=subprocess.DEVNULL,
        )
    with wave.open(wav_path, "rb") as handle:
        raw = np.frombuffer(handle.readframes(handle.getnframes()), dtype=np.int16)
    samples = raw.astype(np.float32) / 32768.0
    segments, _ = _whisper(model_name).transcribe(
        samples,
        language="en",
        beam_size=10,
        best_of=10,
        initial_prompt=prompt,
        condition_on_previous_text=False,
        vad_filter=False,
        temperature=[0.0],
    )
    return "".join(ch for ch in " ".join(s.text for s in segments) if ch.isalnum())


def read_audio(mp3_path: str) -> tuple[list[str], dict[str, int]]:
    heard: list[str] = []
    votes: dict[str, int] = {}
    for model_name in WHISPER_MODELS:
        for prompt in WHISPER_PROMPTS:
            try:
                code = transcribe(mp3_path, model_name, prompt)
            except Exception:
                continue
            if len(code) == 6:
                heard.append(code)
                votes[code] = votes.get(code, 0) + 1
    return heard, votes


class Challenge:
    """One captcha: where its media was saved and what we read from it."""
    def __init__(self, image_path: str | None, audio_path: str | None):
        self.image_path = image_path
        self.audio_path = audio_path
        self.heard: list[str] = []
        self.votes: dict[str, int] = {}
        self.ranked = None
        self._analyse()

    def _analyse(self) -> None:
        if self.audio_path:
            self.heard, self.votes = read_audio(self.audio_path)
        if self.image_path and self.heard:
            try:
                self.ranked = solver.read(self.image_path, self.heard)
            except Exception:
                self.ranked = None

    @property
    def consensus(self) -> str | None:
        """The audio reading most models agreed on."""
        if not self.heard:
            return None
        if self.votes:
            return max(self.votes.items(), key=lambda item: item[1])[0]
        return self.heard[0]

    def guess(self) -> str | None:
        """The best answer to submit.

        The checker ignores case (verified: submitting an all-lowercase reading of
        a code that appeared in mixed case was accepted), so only the *letters*
        matter. The two channels are complementary: the audio names the letters
        but misses sound-alikes (V/Z, F/S, 8/B, M/N), while the picture has the
        exact glyphs but is noisy. So the audio supplies the string and the
        picture overrides any position where it clearly prefers another glyph.
        """
        consensus = self.consensus
        if not consensus:
            return None
        if not self.ranked:
            return consensus.lower()

        chosen = list(consensus.lower())
        for position, ranked in enumerate(self.ranked):
            if position >= len(chosen) or not ranked:
                continue
            top_char, top_score = ranked[0]
            if top_char.lower() == chosen[position]:
                continue
            audio_score = next(
                (score for char, score in ranked
                 if char.lower() == chosen[position]),
                float("inf"))
            # The picture wins only when it is a *good* match and much better than
            # the audio's letter. Both bounds matter: in a noisy image every
            # template scores badly, and a purely relative rule then "corrects"
            # letters the audio had right. These thresholds were calibrated on
            # hand-verified challenges, where genuine corrections scored 0.12-0.16
            # at a ratio of 0.35-0.46, while noise artifacts scored >=0.21 at
            # ratios >=0.75.
            if top_score < 0.18 and top_score < audio_score * 0.55:
                chosen[position] = top_char.lower()
        return "".join(chosen)

    def candidates(self, limit: int = 16) -> list[str]:
        """Ordered spellings to try, best first.

        Only the first is actually submitted per challenge (each submission
        issues a new code), so this mainly documents what we would try next.
        """
        ordered: list[str] = []
        consensus = self.consensus
        if consensus:
            ordered.append(consensus)
        ordered.extend(self._letter_readings())
        if consensus:
            ordered.extend(solver.variants(consensus, limit))
        seen, unique = set(), []
        for code in ordered:
            if code and len(code) == 6 and code.upper() not in seen:
                seen.add(code.upper())
                unique.append(code)
        return unique[:limit]

    def _letter_readings(self) -> list[str]:
        """Audio readings, most agreed-upon first."""
        ordered: list[str] = []
        if self.votes:
            ordered.extend(code for code, _ in sorted(self.votes.items(),
                                                      key=lambda item: -item[1]))
        for code in self.heard:
            if code not in ordered:
                ordered.append(code)
        return ordered


async def grab_media(page: Page, directory: str, tag: str) -> Challenge | None:
    """Save the challenge image and audio that are currently on the page."""
    os.makedirs(directory, exist_ok=True)
    image_path = None
    for src, width in await page.eval_on_selector_all("img", "e=>e.map(x=>[x.src,x.width])"):
        if src.startswith("data:image/png") and width and width > 150:
            image_path = os.path.join(directory, f"{tag}.png")
            with open(image_path, "wb") as handle:
                handle.write(base64.b64decode(src.split(",", 1)[1]))
            break

    audio_path = None
    for src in await page.eval_on_selector_all(
        "audio source, #captcha_audio source, audio",
        "e=>e.map(x=>x.src||x.getAttribute('src')).filter(Boolean)",
    ):
        path = os.path.join(directory, f"{tag}.mp3")
        try:
            if src.startswith("data:"):
                with open(path, "wb") as handle:
                    handle.write(base64.b64decode(src.split(",", 1)[1]))
            else:
                urllib.request.urlretrieve(src, path)
            audio_path = path
        except Exception:
            audio_path = None
        break

    if not image_path and not audio_path:
        return None
    return Challenge(image_path, audio_path)


async def submit(page: Page, code: str) -> str:
    """Submit one answer. Returns 'passed', 'wrong', 'dead' or 'error'.

    Waits for the global submission interval first, so that concurrent attempts
    cannot combine into a burst.
    """
    await _respect_interval()

    try:
        await page.fill("#ans", code)
        await page.click("#jar")
    except Exception:
        return "error"
    await page.wait_for_timeout(3000)
    if "security-check" not in page.url:
        return "passed"
    try:
        body = await page.inner_text("body")
    except Exception:
        body = ""
    if "fejl" in body:
        return "dead"
    return "wrong"


async def answer_challenge(page: Page, directory: str, tag: str, rounds: int = 10,
                           verbose: bool = True) -> str:
    """Keep answering until accepted, the window closes or the token dies."""
    for round_number in range(1, rounds + 1):
        for _ in range(40):
            await page.wait_for_timeout(350)
            if await page.query_selector("#ans"):
                break
        else:
            return "gone"

        challenge = await grab_media(page, directory, f"{tag}_{round_number}")
        if challenge is None:
            return "no-media"
        # Only ONE submission per challenge: each POST issues a brand new code,
        # so trying several spellings in a row just answers different puzzles.
        options = challenge.candidates()
        pick = challenge.guess() or (options[0] if options else None)
        if verbose:
            print(f"    {tag} #{round_number} heard={challenge.heard[:2]} pick={pick}",
                  flush=True)
        if not pick:
            return "no-reading"
        state = await submit(page, pick)
        if verbose:
            print(f"      {pick} -> {state}", flush=True)
        if state == "passed":
            return "passed"
        if state in ("dead", "error"):
            return "dead"
    return "exhausted"


def _credential_selectors(inputs) -> tuple[str, str] | None:
    user = password = None
    for field_type, name, field_id in inputs:
        selector = f"input[name='{name}']" if name else (f"#{field_id}" if field_id else None)
        if not selector:
            continue
        if field_type == "password":
            password = selector
        elif field_type in ("text", "email") and user is None:
            user = selector
    if user and password:
        return user, password
    return None


async def _inputs(page: Page):
    try:
        return await page.eval_on_selector_all("input", "e=>e.map(x=>[x.type,x.name,x.id])")
    except Exception:
        return []


async def _click_unilogin_idp(page: Page) -> bool:
    """Click the "Unilogin" button on the Loginvælger page.

    The picker offers three providers: Unilogin (`selectedIdp=uni_idp`), MitID
    (`nemlogin3`) and "Lokalt login" (`showIdpList`). Only the last one goes
    through the school-search page and gets challenged a second time; clicking
    Unilogin goes straight to the "Brugernavn" -> "Adgangskode" form. This was
    the wrong button for a long time.
    """
    for selector in ("button[name='selectedIdp'][value='uni_idp']",
                     "button:has-text('Unilogin')"):
        try:
            if await page.query_selector(selector):
                await page.click(selector, timeout=6000)
                return True
        except Exception:
            continue
    return False


async def _click_local_login(page: Page) -> bool:
    for selector in ("button[name='showIdpList']", "button:has-text('Lokalt login')",
                     "text=Lokalt login"):
        try:
            if await page.query_selector(selector):
                await page.click(selector, timeout=5000)
                return True
        except Exception:
            continue
    return False


# The UniLogin picker leads to a "Søg efter lokalt login" page: a single text
# field named `username` (which takes the UniLogin username, not an email —
# "cons0418" works, "cons0418@unilogin.dk" does not) plus a hidden-looking
# "Næste" submit button that is `sr-only`, so it must be activated by name/value
# rather than by clicking the visible text.
IDP_SEARCH = "input#idp-search, input[name='username']"
IDP_NEXT = "button[name='navigate'][value='next']"


async def _at_idp_search(page: Page) -> bool:
    try:
        return bool(await page.query_selector(IDP_SEARCH)) and not bool(
            await page.query_selector("input[type='password']"))
    except Exception:
        return False


async def _submit_idp_search(page: Page, username: str) -> bool:
    """Type the UniLogin username on the IdP search page and press Næste."""
    try:
        await page.fill(IDP_SEARCH, username)
    except Exception:
        return False
    for selector in (IDP_NEXT, "button:has-text('Næste')", "input[type='submit']",
                     "button[type='submit']"):
        try:
            if await page.query_selector(selector):
                await page.click(selector, timeout=5000)
                return True
        except Exception:
            continue
    try:  # last resort: submit the form programmatically
        await page.eval_on_selector(
            f"xpath=//input[@id='idp-search']/ancestor::form[1]",
            "form => form.requestSubmit()")
        return True
    except Exception:
        return False


async def _fill_and_submit_credentials(page: Page, username: str, password: str) -> bool:
    """Type the credentials into whatever login form is on the page and submit."""
    fields = _credential_selectors(await _inputs(page))
    if not fields:
        return False
    user_selector, password_selector = fields
    try:
        await page.fill(user_selector, username)
        await page.fill(password_selector, password)
    except Exception:
        return False
    for selector in ("input[type='submit']", "button[type='submit']",
                     "button:has-text('Log ind')", "button:has-text('Fortsæt')",
                     "button:has-text('Næste')"):
        try:
            await page.click(selector, timeout=3500)
            return True
        except Exception:
            continue
    return False


async def pass_gateway(page: Page, directory: str, tag: str) -> bool:
    """Clear the bot-check on arrival at /unilogin.

    Only this one challenge has to be answered: the "Unilogin" provider button
    leads to the username/password form without being challenged again.
    """
    await page.goto(UNILOGIN, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_timeout(1500)

    if "security-check" not in page.url and not await page.query_selector("#ans"):
        print("    no gateway challenge shown", flush=True)
        return True
    state = await answer_challenge(page, directory, f"{tag}g")
    if state != "passed":
        print(f"    gateway {state}", flush=True)
        return False
    print("    gateway passed", flush=True)
    await page.wait_for_timeout(2000)
    return True


async def sign_in(page: Page, directory: str, tag: str, username: str,
                  password: str) -> bool:
    """Unilogin picker -> Brugernavn -> Næste -> Adgangskode -> Log ind."""
    # The picker may need a moment after the gateway redirect.
    for _ in range(10):
        if await page.query_selector("button[name='selectedIdp'][value='uni_idp']"):
            break
        await page.wait_for_timeout(600)
    print(f"    picker url={page.url[:70]}", flush=True)
    await page.screenshot(path=os.path.join(directory, f"{tag}_picker.png"),
                          full_page=True)

    if not await _click_unilogin_idp(page):
        print("    no Unilogin button", flush=True)
        return False
    print("    clicked Unilogin", flush=True)
    await page.wait_for_timeout(4000)

    # Clicking Unilogin can itself hit the bot-check. Clear it, then look for the
    # username form again.
    for stage in range(1, 4):
        if await page.query_selector("#ans"):
            print(f"    step{stage}: gateway after Unilogin", flush=True)
            state = await answer_challenge(page, directory, f"{tag}u{stage}")
            if state != "passed":
                print(f"    step{stage}: gateway {state}", flush=True)
                return False
            await page.wait_for_timeout(3000)
            continue
        if await page.query_selector("input[type='password']") or \
                await page.query_selector("input#idp-search") or \
                await page.query_selector("input[name='username']"):
            break
        await page.wait_for_timeout(2500)

    # Step 1: Brugernavn.
    if not await _type_username(page, username):
        await page.screenshot(path=os.path.join(directory, f"{tag}_nouser.png"),
                              full_page=True)
        print(f"    no username field at {page.url[:70]}", flush=True)
        return False
    print("    entered username", flush=True)
    await page.wait_for_timeout(4500)

    # Step 2: Adgangskode.
    if not await page.query_selector("input[type='password']"):
        await page.wait_for_timeout(2500)
    if not await page.query_selector("input[type='password']"):
        body = ""
        try:
            body = (await page.inner_text("body")).replace("\n", " ")
        except Exception:
            pass
        print(f"    no password field ({body[:90]!r})", flush=True)
        await page.screenshot(path=os.path.join(directory, f"{tag}_nopass.png"),
                              full_page=True)
        return False

    await page.screenshot(path=os.path.join(directory, f"{tag}_password.png"),
                          full_page=True)
    if not await _fill_and_submit_password(page, password):
        return False
    print("    submitted password", flush=True)
    await page.wait_for_timeout(10000)

    await page.screenshot(path=os.path.join(directory, f"{tag}_afterlogin.png"),
                          full_page=True)
    with open(os.path.join(directory, f"{tag}_afterlogin.html"), "w") as handle:
        handle.write(await page.content())
    try:
        text = (await page.inner_text("body")).replace("\n", " | ")
    except Exception:
        text = ""
    print(f"    after login url={page.url[:80]}", flush=True)
    print(f"    after login text={text[:160]!r}", flush=True)
    return "security-check" not in page.url


async def _type_username(page: Page, username: str) -> bool:
    """Fill the Brugernavn field and press Næste.

    Careful: the bot-check page also has a text input (`#ans`), so a loose
    `input[type='text']` selector types the username into the captcha box — which
    is exactly what happened before this was tightened up. The captcha field is
    excluded explicitly, and the dedicated `#idp-search` field is preferred over
    any generic text input.
    """
    selectors = ("input#idp-search", "input[name='username']", "input#username",
                 "input[name='j_username']")
    for selector in selectors:
        try:
            field = await page.query_selector(selector)
        except Exception:
            field = None
        if not field:
            continue
        if selector == "input[name='username']" and await page.query_selector("#ans"):
            # still on the bot-check page: the username box is not here yet
            continue
        try:
            await page.fill(selector, username)
        except Exception:
            continue
        for button in ("button[name='navigate'][value='next']",
                       "button:has-text('Næste')", "input[type='submit']",
                       "button[type='submit']"):
            try:
                if await page.query_selector(button):
                    await page.click(button, timeout=5000)
                    return True
            except Exception:
                continue
        try:
            await page.eval_on_selector(selector, "el => el.form.requestSubmit()")
        except Exception:
            pass
        return True
    return False


async def _fill_and_submit_password(page: Page, password: str) -> bool:
    try:
        await page.fill("input[type='password']", password)
    except Exception:
        return False
    for button in ("button[type='submit']", "input[type='submit']",
                   "button:has-text('Log ind')", "button:has-text('Næste')"):
        try:
            if await page.query_selector(button):
                await page.click(button, timeout=5000)
                return True
        except Exception:
            continue
    try:
        await page.eval_on_selector("input[type='password']",
                                    "el => el.form.requestSubmit()")
        return True
    except Exception:
        return False


async def open_student(page: Page, directory: str, tag: str, username: str,
                       password: str) -> bool:
    """Clear the gateway, then sign in via the Unilogin provider and open the
    student area."""
    if not await pass_gateway(page, directory, tag):
        return False

    if not await sign_in(page, directory, tag, username, password):
        return False

    await page.goto(STUDENT, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_timeout(4000)
    await page.screenshot(path=os.path.join(directory, f"{tag}_student.png"),
                          full_page=True)
    with open(os.path.join(directory, f"{tag}_student.html"), "w") as handle:
        handle.write(await page.content())
    try:
        print(f"    student url={page.url[:80]}", flush=True)
        print(f"    student text={(await page.inner_text('body'))[:150]!r}", flush=True)
    except Exception:
        pass
    return "unilogin" not in page.url and "security-check" not in page.url
