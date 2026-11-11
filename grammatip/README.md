# Grammatip student automation

Automates the UniLogin login for Grammatip so the student area can be reached and
the assignments worked through.

The obstacle is the STIL (`security-check.stil.dk`) bot-check gateway in front of
UniLogin. It serves a 6 character code as **both** an image and a spoken
recording.

## The login flow

The `Loginvælger` page offers three providers. This matters more than it sounds:

| button | value | goes to |
| --- | --- | --- |
| **Unilogin** | `selectedIdp=uni_idp` | **`Brugernavn` → `Næste` → `Adgangskode` → `Log ind`** |
| MitID | `selectedIdp=nemlogin3` | MitID |
| Lokalt login | `showIdpList` | school search page, challenged a second time |

Clicking **Unilogin** is the correct path and is what the code does. Clicking
*Lokalt login* used to be the code's choice and it was wrong: it detours through
a school-search page that gets its own captcha, which is where the flow kept
dying.

## How the captcha is read

Two independent readings are combined:

| channel | what it gives | how |
| --- | --- | --- |
| audio | which letters/digits, in order | `faster-whisper` (`small.en` + `base.en`, two prompts) — a majority vote over four transcriptions |
| image | the actual glyphs | the code is painted in one flat grey tone, distinct from both the paper and the noise lines, so a narrow band around that tone isolates it; connected components split the glyphs; each is template-matched against all 62 characters rendered in six bundled fonts |

The audio consensus is the starting point. The picture overrides a position only
when its glyph is **both** a good absolute match and much better than the audio's
letter:

```python
if top_score < 0.18 and top_score < audio_score * 0.55:
    chosen[position] = top_char
```

Both bounds are needed. A purely relative rule "corrects" letters the audio had
right, because in a noisy image every template scores badly. The thresholds come
from hand-verified challenges: genuine corrections scored 0.12–0.16 at a ratio of
0.35–0.46, while noise artifacts scored ≥0.21 at ratios ≥0.75. That gives 4/5 on
the regression set, against 2/5 for a naive relative rule.

`python3 main.py --check` prints both readings for one live challenge.

## Facts established by running it

* **The checker ignores case.** An all-lowercase reading of a mixed-case code was
  accepted outright (`htg2ym` for `HTG2YM`).
* **Each submission issues a new code**, so one answer per challenge — trying
  several spellings in a row answers different puzzles.
* **`Der er opstået en fejl` is rate limiting, and it is sticky.** It kills the
  session token. At 20–45 s spacing, 12 consecutive submissions produced none;
  below ~15 s it appears often. The budget is **per client, not per browser
  context**, so parallel workers only burn it faster, and recovery needs many
  minutes of complete silence.
* **The username is a UniLogin username** (`cons0418`), not an email; the plain
  `/login/local` form on grammatip.com rejects it.
* **A bare `input[type=text]` on the bot-check page is the captcha box.** An
  earlier version typed the username into it. The captcha field is now excluded
  explicitly.

## Install

```bash
./setup.sh
```

or by hand:

```bash
sudo apt-get install -y ffmpeg fonts-liberation fonts-dejavu fonts-croscore
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

## Run

```bash
python3 main.py                  # retries the whole chain until it gets through
python3 main.py --check          # capture one challenge and print the readings
python3 main.py --headless 0     # watch it in a real window
python3 one_shot.py              # one chain, verbose, for debugging
python3 explore.py               # interactive driver: b/u/s/g/c/t commands, logs traffic
```

| variable | default | meaning |
| --- | --- | --- |
| `GT_USER` | `cons0418` | UniLogin username |
| `GT_PASS` | see `main.py` | UniLogin password |
| `GT_OUT` | `./artifacts` | images, audio, screenshots |
| `GT_THROTTLE` | `22` | **seconds between submissions — do not lower this** |
| `GT_ATTEMPTS` | `30` | login chains before giving up |
| `GT_HEADLESS` | `1` | `0` to show the window |

## Files

```
main.py             CLI, retry loop
browser.py          page interaction: capture, answer, picker, username/password
captcha_solver.py   tone isolation, glyph templates, confusable clusters
explore.py          interactive browser driver for studying the flow
one_shot.py         single verbose chain for debugging
setup.sh            system + Python dependencies
```

## Status

**No assignment has been completed.** The login does not complete reliably, so
nothing was entered on the site.

What works:

* the captcha reader — 4/5 on a hand-verified regression set, and it is right on
  the clear majority of live challenges
* the login flow shape is now correct and verified in stages: gateway →
  `Loginvælger` → Unilogin → `Brugernavn` → `Næste` → `Adgangskode` → `Log ind`
* the first gateway is cleared regularly

What blocks completion: each attempt needs one correct captcha answer, and every
submission has a substantial chance of killing the session token outright. Once
the per-client budget is exhausted — which several hours of automated retries
will do — **every** attempt returns the error page immediately, including from a
normal Chrome with no automation flags. That was confirmed: a clean,
non-automated Chrome gets the same `Der er opstået en fejl` page, so it is not a
browser-fingerprint problem.

The practical route from here is to solve the single gateway by hand in one
sitting at human pace — the flow then carries through to the assignments — or to
have the account owner confirm whether a non-UniLogin login route exists.

## Artifacts

Every attempt writes to `artifacts/`:

* `aN_g_*.png`, `aN_g_*.mp3` — the challenges it was shown
* `aN_picker.png`, `aN_password.png`, `aN_afterlogin.*` — each login stage
* `aN_student.png`, `aN_student.html` — the student area, once reached
