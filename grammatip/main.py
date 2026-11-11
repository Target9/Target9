#!/usr/bin/env python3
"""Run everything: solve the UniLogin bot-check, log in, open the assignments.

    python3 main.py                 # normal run
    python3 main.py --check         # only verify the captcha reader works
    python3 main.py --headless 0    # watch it in a real window
    python3 main.py --attempts 40   # how many login chains to try

Credentials come from the environment when set, otherwise the defaults below
are used:

    GT_USER, GT_PASS, GT_OUT, GT_THROTTLE, GT_ATTEMPTS, GT_HEADLESS
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import time

from playwright.async_api import async_playwright

import browser
import captcha_solver as solver

DEFAULT_USER = "cons0418"
DEFAULT_PASS = "&s=d=NlVeM&.j6g"
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.join(HERE, "artifacts")


def log(*parts) -> None:
    print(time.strftime("%H:%M:%S"), *parts, flush=True)


async def check_captcha(directory: str, headless: bool) -> int:
    """Prove the reader works on one live challenge, without submitting."""
    async with async_playwright() as playwright:
        engine = await playwright.chromium.launch(headless=headless)
        context = await engine.new_context(viewport={"width": 1400, "height": 1000},
                                           locale="da-DK")
        page = await context.new_page()
        await page.goto(browser.UNILOGIN, wait_until="domcontentloaded", timeout=60000)
        for _ in range(40):
            await page.wait_for_timeout(350)
            if await page.query_selector("#ans"):
                break
        else:
            log("no captcha appeared")
            await engine.close()
            return 1
        challenge = await browser.grab_media(page, directory, "check")
        if challenge is None:
            log("could not capture the challenge")
            await engine.close()
            return 1
        log("audio readings:", challenge.heard)
        log("picture reading:",
            solver.best_code(challenge.ranked) if challenge.ranked else None)
        log("answer that would be submitted:", challenge.guess())
        await engine.close()
        return 0


async def run(args) -> int:
    directory = args.out
    os.makedirs(directory, exist_ok=True)
    log(f"artifacts -> {directory}")
    log(f"pacing submissions {browser.SUBMIT_INTERVAL:.0f}s apart")

    async with async_playwright() as playwright:
        engine = await playwright.chromium.launch(headless=args.headless)
        for attempt in range(1, args.attempts + 1):
            # A session whose token has died stays dead, so each attempt gets a
            # clean context; that also gives a fresh set of gateway cookies.
            context = await engine.new_context(viewport={"width": 1400, "height": 1000},
                                               locale="da-DK")
            page = await context.new_page()
            log(f"attempt {attempt}")
            success = False
            try:
                success = await browser.open_student(page, directory, f"a{attempt}",
                                                     args.user, args.password)
                if success:
                    log("logged in")
                    await context.storage_state(
                        path=os.path.join(directory, "state.json"))
                    log(f"student area: {page.url}")
                    await asyncio.sleep(3600)
                    return 0
            except Exception as exc:
                log(f"attempt {attempt} failed: {type(exc).__name__} {exc}")
            finally:
                if not success:
                    try:
                        await context.close()
                    except Exception:
                        pass
        await engine.close()
    log("gave up")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="test the captcha reader")
    parser.add_argument("--headless", default=os.environ.get("GT_HEADLESS", "1"),
                        help="0 to show the browser window")
    parser.add_argument("--user", default=os.environ.get("GT_USER", DEFAULT_USER))
    parser.add_argument("--password", default=os.environ.get("GT_PASS", DEFAULT_PASS))
    parser.add_argument("--out", default=os.environ.get("GT_OUT", DEFAULT_OUT))
    parser.add_argument("--attempts", type=int,
                        default=int(os.environ.get("GT_ATTEMPTS", "30")))
    args = parser.parse_args()
    args.headless = args.headless not in ("0", "false", "False")

    if args.check:
        return asyncio.run(check_captcha(args.out, args.headless))
    return asyncio.run(run(args))


if __name__ == "__main__":
    sys.exit(main())
