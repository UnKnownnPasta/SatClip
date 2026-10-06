"""Keyboard-only walkthrough of the web UI (M4 accessibility check). Needs the API on :8000.
Opens the pickers, picks a district with arrow keys, sets two dates, submits a change question from the keyboard,
and checks that focus lands on the evidence card. Exits non-zero on failure.
Usage: python tools/ui_keyboard_check.py"""
import sys

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    page = p.chromium.launch().new_page(viewport={"width": 1280, "height": 900})
    page.goto("http://localhost:8000/", wait_until="networkidle")
    page.keyboard.press("Tab")  # first stop is the skip link
    assert page.evaluate("document.activeElement.className") == "skip"
    page.focus("#q")
    page.keyboard.type("Did the flood spread between these dates?")
    page.focus("#more summary")
    page.keyboard.press("Enter")  # open the place and date pickers
    page.focus("#place")
    page.keyboard.type("Barpe")
    page.wait_for_selector("#place-list li")
    page.keyboard.press("ArrowDown")
    assert page.get_attribute("#place", "aria-activedescendant") == "opt-0"
    page.keyboard.press("Enter")
    picked = page.inner_text("#place-picked")
    assert "Barpeta" in picked, picked
    page.focus("input[name=mode][value=two]")
    page.keyboard.press("Space")
    assert page.is_visible("#d2")
    page.fill("#d1", "2024-06-05")
    page.fill("#d2", "2024-07-11")
    page.focus("#q")
    page.keyboard.press("Control+Enter")
    page.wait_for_selector("#card:not(.hidden)", timeout=240_000)
    page.wait_for_timeout(300)
    assert page.evaluate("document.activeElement.id") == "card", "focus should move to the card"
    print("understood:", page.inner_text("#understood-text"))
    print("card:", page.inner_text("#answer"))
    print("keyboard walkthrough OK")
    sys.exit(0)
