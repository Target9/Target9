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

Danish UI text appears quoted verbatim because it is what the page actually
shows; glosses are given inline.

* **The checker is case-insensitive.** An all-lowercase reading of a mixed-case
  code was accepted outright (`htg2ym` for `HTG2YM`).
* **Each submission issues a new code**, so it is one answer per challenge —
  trying several spellings in a row just answers different puzzles.
* **A correctly read code can still fail with `Der er opstået en fejl`** ("an
  error has occurred"). This was verified not to be a wrong answer: codes I
  confirmed by eye against the image produced it, while a deliberately wrong code
  (`aaaaaa`) returned `Koden var forkert` ("the code was wrong") 7 times out of 7.
  It means the answer was accepted but the redirect chain collapsed.
* **The challenge page has no `<form>`.** Submission is performed by F5's
  obfuscated JavaScript, so a plain HTTP client cannot submit it at all — it gets
  `Please enable JavaScript to view the page content.`
* **Gateway trust does not transfer between clients.** Cookies taken from a
  browser session that had already passed the gateway, imported into a `requests`
  session, were challenged again. Trust is bound to the live browser session.
* **The picker's three providers are not equivalent.** "Lokalt login" ("local
  login", `showIdpList`) detours through a school-search page and a *second*
  challenge; **Unilogin** (`selectedIdp=uni_idp`) goes straight to the
  `Brugernavn` ("username") → `Næste` ("next") → `Adgangskode` ("password") form.
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

**No assignment has been completed.** The login does not complete, so nothing was
entered on the site.

What works:

* the captcha reader — 4/5 on a hand-verified regression set, and correct on the
  clear majority of live challenges. Audio gives the letters, the image corrects
  positions where it is clearly the better match.
* the login flow shape is correct and verified stage by stage: gateway →
  provider picker → Unilogin → `Brugernavn` → `Næste` → `Adgangskode` → `Log ind`
* a single submission to the first gateway passes roughly 1 time in 3–4

What blocks completion: the flow needs **two** gateway passes in one session (the
gateway re-challenges after the provider click), and each pass is an independent
low-probability event that can also fail after being answered correctly. Across
rough runs the first gateway passed on the order of 1 attempt in 10, the second
far less often, and never with the sign-in completing.

Things ruled out with tests rather than guesses: it is not browser
fingerprinting (a plain, non-automated Chrome fails identically), not answer
grading (wrong codes still return `Koden var forkert` cleanly), not challenge TTL
(25 s delays behave the same), and not transferable session state (imported
cookies are still challenged). A plain `requests` client cannot submit the
challenge at all, because the page has no form.

The practical route from here is to log in once by hand in a real browser and
supply the resulting session cookies for `grammatip.com`, so the student area can
be fetched directly without the gateway, or to have the account owner confirm
whether a non-UniLogin login route exists.

## Artifacts

Every attempt writes to `artifacts/`:

* `aN_g_*.png`, `aN_g_*.mp3` — the challenges it was shown
* `aN_picker.png`, `aN_password.png`, `aN_afterlogin.*` — each login stage
* `aN_student.png`, `aN_student.html` — the student area, once reached
