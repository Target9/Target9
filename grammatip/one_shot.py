#!/usr/bin/env python3
"""A single login chain with detailed logging — useful when debugging.

    python3 one_shot.py                 # one attempt, dumps everything
    python3 one_shot.py --out /tmp/run  # custom artifact directory
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import time

from playwright.async_api import async_playwright

import browser

DEFAULT_USER = "cons0418"
DEFAULT_PASS = "&s=d=NlVeM&.j6g"
HERE = os.path.dirname(os.path.abspath(__file__))


def log(*parts) -> None:
    print(time.strftime("%H:%M:%S"), *parts, flush=True)


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default=os.environ.get("GT_USER", DEFAULT_USER))
    parser.add_argument("--password", default=os.environ.get("GT_PASS", DEFAULT_PASS))
    parser.add_argument("--out", default=os.path.join(HERE, "artifacts", "one-shot"))
    parser.add_argument("--headless", default="1")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    headless = args.headless not in ("0", "false", "False")

    async with async_playwright() as playwright:
        engine = await playwright.chromium.launch(headless=headless)
        context = await engine.new_context(viewport={"width": 1400, "height": 1000},
                                           locale="da-DK")
        page = await context.new_page()
        try:
            ok = await browser.open_student(page, args.out, "one", args.user,
                                            args.password)
        except Exception as exc:
            log(f"crash: {type(exc).__name__} {exc}")
            ok = False
        log("result:", "logged in" if ok else "failed")
        if ok:
            log("student area:", page.url)
            await context.storage_state(path=os.path.join(args.out, "state.json"))
            await asyncio.sleep(600)
        await engine.close()
        return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
