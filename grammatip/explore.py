"""Interactive browser session for poking at the UniLogin flow by hand.

Opens a real (headed by default) Chromium window against `--url` and lets you
drive it, while logging every request/response so the login sequence can be
studied. Nothing is automated here on purpose: this is the instrument, not the
solution.

    python3 explore.py                      # open grammatip/unilogin
    python3 explore.py --url <url>          # open somewhere else
    python3 explore.py --wait 600           # keep the window open (seconds)
    python3 explore.py --headless 0         # force a visible window

Commands typed on stdin while it runs:

    b               print every button and input on the current page
    u               print the current URL and visible text
    s               save the page HTML + a screenshot into the log directory
    g <url>         navigate to a URL
    c <selector>    click a selector
    t <selector> <text>   type text into a selector
    q               quit
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import time

from playwright.async_api import async_playwright


def log(*parts) -> None:
    print(time.strftime("%H:%M:%S"), *parts, flush=True)


async def dump_page(page, outdir: str, tag: str) -> None:
    """Print and save the interactive elements of the current page."""
    try:
        url = page.url
    except Exception:
        url = "(gone)"
    log(f"URL {url}")
    try:
        text = (await page.inner_text("body")).replace("\n", " | ")
    except Exception:
        text = ""
    log(f"TEXT {text[:300]!r}")

    try:
        buttons = await page.eval_on_selector_all(
            "button, input[type=submit], a",
            "e=>e.map(x=>[x.tagName, x.name||'', x.value||'', "
            "(x.innerText||'').trim().slice(0,40), x.id||''])")
    except Exception:
        buttons = []
    for row in buttons:
        log(f"  {row}")

    os.makedirs(outdir, exist_ok=True)
    try:
        with open(os.path.join(outdir, f"{tag}.html"), "w") as handle:
            handle.write(await page.content())
        await page.screenshot(path=os.path.join(outdir, f"{tag}.png"), full_page=True)
        log(f"  saved {tag}.html / {tag}.png")
    except Exception as exc:
        log(f"  could not save: {exc}")


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="https://www.grammatip.com/unilogin")
    parser.add_argument("--headless", default="0")
    parser.add_argument("--out", default="/tmp/work/explore")
    parser.add_argument("--wait", type=float, default=900)
    args = parser.parse_args()

    headless = args.headless not in ("0", "false", "False")
    os.makedirs(args.out, exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=headless)
        context = await browser.new_context(viewport={"width": 1400, "height": 1000},
                                            locale="da-DK")
        page = await context.new_page()

        # Record the whole exchange; this is what makes the flow legible.
        page.on("request", lambda r: log(f"  -> {r.method} {r.url[:110]}")
                if r.method in ("POST", "GET") and "security-check" not in r.url
                else None)
        page.on("response", lambda r: log(f"  <- {r.status} {r.url[:90]}")
                if "security-check" not in r.url else None)

        await page.goto(args.url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(1500)
        await dump_page(page, args.out, "start")

        loop = asyncio.get_running_loop()
        deadline = time.time() + args.wait
        counter = 0
        while time.time() < deadline:
            try:
                line = await asyncio.wait_for(
                    loop.run_in_executor(None, sys.stdin.readline), timeout=1.0)
            except (asyncio.TimeoutError, Exception):
                continue
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            counter += 1
            parts = line.split()
            command = parts[0].lower()

            if command == "q":
                break
            elif command == "b":
                await dump_page(page, args.out, f"snap{counter}")
            elif command == "u":
                log(f"URL {page.url}")
            elif command == "s":
                await dump_page(page, args.out, f"snap{counter}")
            elif command == "g" and len(parts) > 1:
                await page.goto(parts[1], wait_until="domcontentloaded")
                await page.wait_for_timeout(1500)
                await dump_page(page, args.out, f"snap{counter}")
            elif command == "c" and len(parts) > 1:
                try:
                    await page.click(parts[1], timeout=8000)
                    await page.wait_for_timeout(4000)
                    await dump_page(page, args.out, f"snap{counter}")
                except Exception as exc:
                    log(f"click failed: {exc}")
            elif command == "t" and len(parts) > 2:
                try:
                    await page.fill(parts[1], " ".join(parts[2:]))
                    log(f"typed into {parts[1]}")
                except Exception as exc:
                    log(f"fill failed: {exc}")
            else:
                log(f"unknown command {command!r}")

        await dump_page(page, args.out, "final")
        await context.storage_state(path=os.path.join(args.out, "state.json"))
        await browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
