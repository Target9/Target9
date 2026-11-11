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
            # override only with a clear margin, so noise cannot flip a position
            if top_score < 0.12 and top_score * 2.0 < audio_score:
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


async def pass_gateways(page: Page, directory: str, tag: str) -> bool:
    """Clear the bot-check wherever it appears, then re-enter through UniLogin.

    The gateway challenges us twice per session: once on arriving at /unilogin,
    and again when the "Lokalt login" POST is submitted. Once both are cleared it
    stops challenging us, and re-entering /unilogin goes straight to the IdP
    picker — the click then leads to the "Søg efter lokalt login" page instead of
    Keycloak's "Der skete en fejl" page.
    """
    await page.goto(UNILOGIN, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_timeout(1200)

    # Stage 1: the challenge shown on arrival.
    if not await page.query_selector("#ans"):
        print("    no first challenge", flush=True)
        return False
    state = await answer_challenge(page, directory, f"{tag}g1")
    if state != "passed":
        print(f"    first gateway {state}", flush=True)
        return False
    print("    first gateway passed", flush=True)

    # Stage 2: click "Lokalt login"; the POST is challenged.
    await page.wait_for_timeout(1800)
    if not await _click_local_login(page):
        print("    no Lokalt login button", flush=True)
        return False
    await page.wait_for_timeout(4500)

    if await page.query_selector("#ans"):
        state = await answer_challenge(page, directory, f"{tag}g2")
        if state != "passed":
            print(f"    second gateway {state}", flush=True)
            return False
        print("    second gateway passed", flush=True)
        await page.wait_for_timeout(2000)
    else:
        # Sometimes the click goes through unchallenged; either way we need to
        # end up on the picker for the re-entry step to work.
        print("    second gateway not shown", flush=True)

    try:
        body = (await page.inner_text("body")).replace("\n", " ")
    except Exception:
        body = ""
    if "Der skete en fejl" in body:
        print("    Keycloak rejected the replay", flush=True)
        return False
    return True


async def sign_in(page: Page, directory: str, tag: str, username: str,
                  password: str) -> bool:
    """Type the credentials on whatever login page the gateway left us on.

    Important: do *not* navigate away first. Passing the second gateway leaves
    the browser on Keycloak's `login-actions` URL, already authorised to show the
    "Søg efter lokalt login" page. Going back to /unilogin throws that away.
    """
    for step in range(1, 15):
        if await page.query_selector("input[type='password']"):
            print(f"    step{step}: password form", flush=True)
            break
        if await _at_idp_search(page):
            print(f"    step{step}: IdP search page", flush=True)
            await page.screenshot(path=os.path.join(directory, f"{tag}_idp.png"),
                                  full_page=True)
            if not await _submit_idp_search(page, username):
                return False
            await page.wait_for_timeout(4500)
            continue
        if await _fill_and_submit_credentials(page, username, password):
            print(f"    step{step}: submitted a credential form", flush=True)
            await page.wait_for_timeout(9000)
            break
        if await page.query_selector("#ans"):
            state = await answer_challenge(page, directory, f"{tag}x{step}")
            if state != "passed":
                print(f"    step{step}: late gateway {state}", flush=True)
                return False
            await page.wait_for_timeout(2500)
            continue
        if await _click_local_login(page):
            print(f"    step{step}: clicked Lokalt login", flush=True)
            await page.wait_for_timeout(4500)
            continue
        try:
            body = (await page.inner_text("body")).replace("\n", " ")
        except Exception:
            body = ""
        print(f"    step{step}: nothing to do ({body[:70]!r})", flush=True)
        return False

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
    return True


async def open_student(page: Page, directory: str, tag: str, username: str,
                       password: str) -> bool:
    """Pass the gateways, save the trusted session, then sign in.

    Once the gateway has accepted one answer, its cookie stays trusted. Saving it
    means a later run can skip the captcha entirely and retry only the step that
    actually failed, which is what makes the whole thing converge.
    """
    trusted_path = os.path.join(directory, "trusted_state.json")

    if os.path.exists(trusted_path):
        try:
            await page.context.add_cookies(
                json.load(open(trusted_path)).get("cookies", []))
            print("    reusing trusted gateway cookies", flush=True)
        except Exception:
            pass
    else:
        if not await pass_gateways(page, directory, tag):
            return False
        try:
            state = await page.context.storage_state()
            with open(trusted_path, "w") as handle:
                json.dump(state, handle)
            print("    saved trusted gateway state", flush=True)
        except Exception:
            pass

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
