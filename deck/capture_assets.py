"""Capture deck screenshots from the running prototype (M7).

Needs the API on :8000 (cd backend && uvicorn satclip.api.main:app --port 8000) and Playwright.
Each asset is an element screenshot of the evidence card, optionally composed side by side
with the map panel, so the slides show the real UI at a readable size.
Run tools/screenshots.py first: it warms the scene cache, so these repeats take seconds.
Usage: python deck/capture_assets.py
"""
import io
import os
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "deck", "assets")
BASE = os.environ.get("SATCLIP_URL", "http://localhost:8000/")
BG = (237, 240, 248)

EXTENT = "How much of Barpeta was under water on 2024-07-11?"
CHANGE = "Did the flood spread in Barpeta between 2024-06-05 and 2024-07-11?"
ASSETS = [  # file, question, viewport width, follow-up click, compose with map
    ("extent.png", EXTENT, 1366, False, True),
    ("change_abstain.png", CHANGE, 1366, False, True),
    ("followup.png", CHANGE, 1366, True, True),
    ("mobile.png", EXTENT, 390, False, False),
    ("oos.png", "How many cars are parked in Mumbai today?", 390, False, False),
    ("ambiguous.png", "How much of Aurangabad was under water on 2024-08-10?", 390, False, False),
]


def compose(card: Image.Image, mapimg: Image.Image, gap=24) -> Image.Image:
    h = max(card.height, mapimg.height)
    out = Image.new("RGB", (card.width + mapimg.width + gap, h), BG)
    out.paste(card, (0, 0))
    out.paste(mapimg, (card.width + gap, 0))
    return out


def ask(page, q, follow):
    page.goto(BASE, wait_until="networkidle")
    page.fill("#q", q)
    page.click("#go")
    page.wait_for_selector("#card:not(.hidden)", timeout=180_000)
    page.wait_for_timeout(2000)
    if follow:
        old = page.inner_text("#answer")
        page.click("#choices button >> nth=0")
        page.wait_for_function(
            "(o) => !document.querySelector('#card').classList.contains('hidden') && document.querySelector('#answer').innerText !== o",
            arg=old, timeout=180_000)
        page.wait_for_timeout(2500)


def main():
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, q, width, follow, with_map in ASSETS:
            ctx = b.new_context(viewport={"width": width, "height": 1000}, color_scheme="light", device_scale_factor=2)
            page = ctx.new_page()
            ask(page, q, follow)
            card = Image.open(io.BytesIO(page.locator("#card").screenshot()))
            img = card
            if with_map:
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(1500)
                mp = Image.open(io.BytesIO(page.locator(".mapbox").screenshot()))
                img = compose(card.convert("RGB"), mp.convert("RGB"))
            img.convert("RGB").save(os.path.join(OUT, name), optimize=True)
            if with_map:  # card on its own, for slides that show two answers side by side
                card.convert("RGB").save(os.path.join(OUT, name.replace(".png", "_card.png")), optimize=True)
            print("saved", name, img.size, file=sys.stderr)
            ctx.close()
        b.close()


if __name__ == "__main__":
    main()
