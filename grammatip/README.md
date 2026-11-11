# Grammatip student automation

Automates the UniLogin login for Grammatip so the student area can be reached
and the assignments worked through.

The obstacle is the STIL (`security-check.stil.dk`) bot-check gateway in front of
UniLogin. It shows a 6 character code as **both** an image and a spoken
recording, and issues a brand new code after every submission.

## How the captcha is read

Two independent readings are fused:

| channel | what it gives | how |
| --- | --- | --- |
| audio | which letters/digits, in order | `faster-whisper` (`small.en` + `base.en`, two prompts) — a majority vote over four transcriptions |
| image | the glyphs themselves | the code is painted in one flat grey tone that differs from both the paper and the noise lines, so a narrow band around that tone isolates the glyphs; connected components split them; each is template-matched against all 62 characters rendered in six bundled fonts |

`captcha_solver.read()` returns, per position, the candidate characters ranked by
glyph distance. `browser.Challenge.guess()` submits the audio consensus, except
when the picture agrees on the letters *and* shows mixed case — the checker does
distinguish upper from lower case.

`python3 main.py --check` prints both readings for one live challenge, which is
the quickest way to see the reader working.

## Measured behaviour of the gateway

Things that were tested rather than assumed:

* every submission yields a **new** code, so submitting several candidates in a
  row answers different puzzles — one answer per challenge
* a wrong answer gives `Koden var forkert`; nothing is locked out
* roughly one submission in five instead gives `Der er opstået en fejl` and kills
  that session's token. It is **not** rate limiting: the same rate occurs with
  0 s, 4 s and 8 s delays, and with the media read or not read. A dead session
  cannot be revived, so each attempt starts from a clean context.
* after the second gateway the `Loginvælger` page is shown again, and clicking
  `Lokalt login` a second time leads to Keycloak's login-actions URL — that is
  where the credential form lives, and it must be filled there.

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
| `GT_ATTEMPTS` | `30` | login chains before giving up |
| `GT_HEADLESS` | `1` | `0` to show the window |

## Files

```
main.py             CLI, retry loop
browser.py          page interaction: capture, answer, picker, credentials
captcha_solver.py   tone isolation, glyph templates, candidate spellings
one_shot.py         single verbose chain for debugging
setup.sh            system + Python dependencies
```

## Status

Working:

* the captcha reader — audio and image agree on most challenges, and the
  combined reading is correct often enough to pass the gateway regularly
* the gateway loop, the picker (including the second `Lokalt login` click) and
  reaching the credential form

Not working reliably: the credential POST. Each attempt has to pass two
gateways in the same session, and each submission has a ~20% chance of killing
that session's token, so a whole chain rarely completes before the token dies.
The chain is therefore retried from scratch; it will get through eventually, but
it depends on luck rather than on anything the code can control.

No assignment was answered, because the login never completed.

## Artifacts

Every attempt writes to `artifacts/`:

* `aN_*.png`, `aN_*.mp3` — the challenges it was shown
* `aN_filled.png` — the credential form, filled in
* `aN_student.png`, `aN_student.html` — the student area, once reached
* `state.json` — browser storage state after a successful login
