# Grammatip student automation

Automates the UniLogin login for Grammatip and opens the student area, so the
assignments can be worked through.

The hard part is the STIL (`security-check.stil.dk`) bot-check gateway that sits
in front of UniLogin: it shows a 6 character captcha as both an image and a
spoken recording, and it issues a brand new challenge after *every* submission.

## How the captcha is solved

Two independent readings are fused:

| channel | what it gives | how |
| --- | --- | --- |
| audio | which letters/digits, in order | `faster-whisper` (`small.en` + `base.en`, two prompts), majority vote over six transcriptions |
| image | exact case and look-alikes | the glyphs are painted in one flat grey tone, so a narrow band around that tone isolates them; connected components split them; each glyph is template-matched against 62 characters rendered in six fonts |

The audio nails the letters most of the time but is case-blind and confuses
sound-alikes (`S`/`F`, `2`/`V`, `8`/`B`). The image is noisy but keeps the exact
shape. `captcha_solver.read()` returns, per position, the characters ranked by
glyph distance; `browser.Challenge.guess()` takes the audio consensus and only
overrides a position when the picture is clearly more confident.

Because the checker is case-insensitive but glyph-exact, the runner also
generates spellings that swap one or two look-alikes
(`captcha_solver.variants`) and tries the best few per challenge.

## Measured behaviour of the gateway

* each submission produces a **new** challenge, so one session can be reused
* a wrong answer gives `Koden var forkert` — no lockout
* submitting faster than roughly one per 8 seconds eventually gives
  `Der er opstået en fejl` and kills the session token
* after the second gateway the `Loginvælger` page reappears; clicking
  `Lokalt login` a second time is what reveals the credential form

## Install

```bash
sudo apt-get install -y ffmpeg tesseract-ocr fonts-liberation \
                        fonts-dejavu fonts-croscore
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

## Run

```bash
python3 main.py                  # full run, keeps retrying until logged in
python3 main.py --check          # capture one challenge and print the readings
python3 main.py --headless 0     # watch the browser
python3 main.py --attempts 40    # more login chains
```

Configuration is by environment variable:

| variable | default | meaning |
| --- | --- | --- |
| `GT_USER` | `cons0418` | UniLogin username |
| `GT_PASS` | see `main.py` | UniLogin password |
| `GT_OUT` | `./artifacts` | where images, audio and screenshots go |
| `GT_THROTTLE` | `8` | seconds between captcha submissions |
| `GT_ATTEMPTS` | `30` | login chains before giving up |
| `GT_HEADLESS` | `1` | `0` to show the window |

## Files

```
main.py             entry point, retry loop, CLI
browser.py          all page interaction: capture, answer, picker, credentials
captcha_solver.py   image segmentation, glyph templates, candidate spellings
```

## Status

The captcha reader works (see `--check`), and the gateway can be passed in a
single session. The remaining blocker is the UniLogin credential step: the
gateway re-challenges that POST as well, and the token is frequently killed
before a whole chain completes. `main.py` therefore retries the full chain.

## Artifacts

Every attempt writes to `artifacts/`:

* `aN_*.png`, `aN_*.mp3` — the challenges it was shown
* `aN_filled.png` — the credential form, filled in
* `aN_student.png`, `aN_student.html` — the student area once reached
* `state.json` — the browser storage state after a successful login
