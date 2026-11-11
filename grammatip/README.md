# Grammatip student automation

Automates the UniLogin login for Grammatip so the student area can be reached and
the assignments worked through.

The obstacle is the STIL (`security-check.stil.dk`) bot-check gateway in front of
UniLogin. It shows a 6 character code as **both** an image and a spoken
recording, and issues a brand new code after every submission.

## How the captcha is read

Two independent readings are combined:

| channel | what it gives | how |
| --- | --- | --- |
| audio | which letters/digits, in order | `faster-whisper` (`small.en` + `base.en`, two prompts) — a majority vote over four transcriptions |
| image | the actual glyphs | the code is painted in one flat grey tone that differs from both the paper and the noise lines, so a narrow band around that tone isolates it; connected components split the glyphs; each is template-matched against all 62 characters rendered in six bundled fonts |

`captcha_solver.read()` returns, per position, the candidate glyphs ranked by
template distance. `browser.Challenge.guess()` takes the audio consensus and lets
the picture override a position when it clearly prefers another glyph — which is
what fixes whisper's sound-alike errors (`v`↔`z`, `f`↔`s`, `8`↔`b`, `m`↔`n`).

`python3 main.py --check` prints both readings for one live challenge.

## Facts established by experiment

These were tested, not assumed, and several contradict what the code originally
believed:

* **The checker ignores case.** An all-lowercase reading of a code shown in mixed
  case was accepted outright (`htg2ym` for `HTG2YM`). Only the letters matter.
* **Every submission issues a new code**, so submitting several candidate
  spellings in a row answers different puzzles. One answer per challenge.
* **A wrong answer gives `Koden var forkert`** — no lockout, retry freely.
* **`Der er opstået en fejl` is rate limiting, and it is sticky.** It kills that
  session's token immediately. At 20 s and 45 s spacing, 12 consecutive
  submissions produced none; below ~15 s it appears on a large fraction. The
  budget is per client, not per browser context, so parallel contexts do not
  help — they only burn it faster. It also takes many minutes of complete
  silence to recover, which is why hammering makes things worse for a long time.
* **The gateway challenges twice per session**: once on arriving at `/unilogin`,
  and again when the `Lokalt login` POST is submitted.
* **Passing the second gateway leaves the browser on Keycloak's `login-actions`
  URL**, which is the "Søg efter lokalt login" page — a single `username` field
  plus an `sr-only` `Næste` button. That page *is* the login step. Navigating
  back to `/unilogin` at that point destroys the authorisation, so the credential
  form must be filled in place.
* The username is a UniLogin username (`cons0418`), not an email; the plain
  `/login/local` form on grammatip.com rejects it.

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
browser.py          page interaction: capture, answer, picker, IdP page, credentials
captcha_solver.py   tone isolation, glyph templates, candidate spellings
one_shot.py         single verbose chain for debugging
setup.sh            system + Python dependencies
```

## Status — read this before relying on it

**No assignment has been completed.** The login does not reliably complete, so
nothing was entered on the site.

Working:

* the captcha reader. Audio and picture agree on most challenges, and the
  combined reading is correct on the clear majority of them.
* the first gateway is cleared regularly.
* the flow now knows the correct shape of the whole login: two gateways, then the
  `login-actions` IdP page in place, then the credentials.

Not working: getting *both* gateways cleared in one session before the rate
limiter intervenes. Each attempt needs two correct captcha answers in the same
session, and each submission carries a substantial chance of killing the token.
Across roughly 200 attempts the first gateway was passed a few dozen times; the
second only a handful, and never with the sign-in completing afterwards.

Because the limit is per client and recovers slowly, repeated automated attempts
actively make the situation worse — the practical way through is to solve the two
gateways by hand in one sitting at a normal human pace, or to have whoever owns
the account confirm whether a non-UniLogin login route exists.

## Artifacts

Every attempt writes to `artifacts/`:

* `aN_*.png`, `aN_*.mp3` — the challenges it was shown
* `aN_idp.png`, `aN_afterlogin.*` — the IdP page and what followed the credentials
* `aN_student.png`, `aN_student.html` — the student area, once reached
* `trusted_state.json` — gateway cookies after the first gateway was cleared
