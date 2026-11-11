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
SUBMIT_INTERVAL = 1.0  # seconds between submissions (the gateway tolerates this)
RESTART_PAUSE = 2.0    # seconds to wait before asking for a fresh challenge

_models: dict[str, object] = {}
_last_submit = 0.0


def _whisper(name: str):
    if name not in _models:
        from faster_whisper import WhisperModel

        _models[name] = WhisperModel(name, device="cpu", compute_type="int8")
    return _models[name]


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
        """The answer to submit.

        The two channels agree on the letters most of the time, and when they do
        the picture supplies the exact upper/lower case, which the checker does
        distinguish. When they disagree we trust the audio consensus, because a
        mis-segmented glyph can corrupt an otherwise correct reading.
        """
        consensus = self.consensus
        if not consensus:
            return None
        if self.ranked:
            picture = solver.best_code(self.ranked)
            if (len(picture) == len(consensus)
                    and picture.upper() == consensus.upper()
                    and picture != picture.upper()):
                # same letters, and the picture sees mixed case: use it
                return picture
        return consensus

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


async def submit(page: Page, code: str, throttle: float = SUBMIT_INTERVAL) -> str:
    """Submit one answer. Returns 'passed', 'wrong', 'dead' or 'error'."""
    global _last_submit
    remaining = throttle - (time.time() - _last_submit)
    if remaining > 0:
        await page.wait_for_timeout(int(remaining * 1000))
    _last_submit = time.time()

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


async def reach_credentials(page: Page, directory: str, tag: str, username: str,
                            password: str, steps: int = 25) -> bool:
    """Walk the gateway and the UniLogin picker until we are signed in.

    Passing the bot-check in front of the "Lokalt login" POST makes Keycloak land
    on its login-actions URL, which is where the credential form appears. So the
    loop does not stop at "a form exists": it fills and submits it in place.
    """
    submitted = False
    for step in range(1, steps + 1):
        fields = _credential_selectors(await _inputs(page))
        if fields and not submitted:
            print(f"    step{step}: credential form", flush=True)
            await page.screenshot(path=os.path.join(directory, f"{tag}_filled.png"),
                                  full_page=True)
            submitted = await _fill_and_submit_credentials(page, username, password)
            print(f"    step{step}: submitted={submitted}", flush=True)
            await page.wait_for_timeout(8000)
            continue

        if await page.query_selector("#ans"):
            state = await answer_challenge(page, directory, f"{tag}s{step}")
            if state in ("dead", "gone", "no-media", "no-reading"):
                print(f"    step{step}: gateway {state}", flush=True)
                return False
            continue

        if submitted:
            # we are past the credentials; either we are in, or we are asked
            # for something else — the caller decides
            return True

        if await _click_local_login(page):
            print(f"    step{step}: clicked Lokalt login", flush=True)
            await page.wait_for_timeout(3500)
            continue

        await page.screenshot(path=os.path.join(directory, f"{tag}_stuck.png"),
                              full_page=True)
        print(f"    step{step}: restarting from {page.url[:60]}", flush=True)
        await asyncio.sleep(RESTART_PAUSE)
        await page.goto(UNILOGIN, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(1500)
        submitted = False
    return False


async def open_student(page: Page, directory: str, tag: str, username: str,
                       password: str) -> bool:
    await page.goto(UNILOGIN, wait_until="domcontentloaded", timeout=60000)
    if not await reach_credentials(page, directory, tag, username, password):
        return False

    if await page.query_selector("#ans"):
        state = await answer_challenge(page, directory, f"{tag}post")
        if state != "passed":
            return False
        await page.wait_for_timeout(3000)

    await page.goto(STUDENT, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_timeout(4000)
    await page.screenshot(path=os.path.join(directory, f"{tag}_student.png"),
                          full_page=True)
    with open(os.path.join(directory, f"{tag}_student.html"), "w") as handle:
        handle.write(await page.content())
    return "unilogin" not in page.url and "security-check" not in page.url
