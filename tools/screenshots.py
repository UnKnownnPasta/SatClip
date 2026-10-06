"""Capture UI screenshots for docs and the deck (M4/M7).

Needs a running API on :8000 serving the frontend (cd backend && uvicorn satclip.api.main:app --port 8000)
and Playwright with Chromium. Live questions query real Sentinel catalogues, so they take 20 to 60 s each.
Usage: python tools/screenshots.py [--only NAME]
"""
import argparse
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "screenshots")
BASE = os.environ.get("SATCLIP_URL", "http://localhost:8000/")

SHOTS = [  # name, question, viewport, colour scheme
    ("01-home-desktop", None, (1366, 900), "light"),
    ("02-flood-extent-desktop", "How much of Barpeta was under water on 2024-07-11?", (1366, 1000), "light"),
    ("03-flood-extent-mobile", "How much of Barpeta was under water on 2024-07-11?", (390, 844), "light"),
    ("04-ambiguous-district", "How much of Aurangabad was under water on 2024-08-10?", (1366, 900), "light"),
    ("05-out-of-scope", "How many cars are parked in Mumbai today?", (390, 844), "light"),
    ("06-crop-change-desktop", "Did the crop decline in Darbhanga between 2024-03-01 and 2024-04-25?", (1366, 1000), "light"),
    ("08-flood-change-abstain", "Did the flood spread in Barpeta between 2024-06-05 and 2024-07-11?", (1366, 1000), "light"),
    ("07-flood-extent-dark", "How much of Barpeta was under water on 2024-07-11?", (1366, 1000), "dark"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, q, (w, h), scheme in SHOTS:
            if a.only and a.only not in name:
                continue
            ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme, device_scale_factor=2 if w < 500 else 1)
            page = ctx.new_page()
            page.goto(BASE, wait_until="networkidle")
            if q:
                page.fill("#q", q)
                page.click("#go")
                page.wait_for_selector("#card:not(.hidden)", timeout=180_000)
                page.wait_for_timeout(2500)  # let overlays and base map tiles load
                page.evaluate("window.scrollTo(0, 0)")  # sticky map: capture from the top
                page.wait_for_timeout(500)
            path = os.path.join(OUT, f"{name}.png")
            page.screenshot(path=path, full_page=True)
            print("saved", path, file=sys.stderr)
            ctx.close()
        b.close()


if __name__ == "__main__":
    main()
