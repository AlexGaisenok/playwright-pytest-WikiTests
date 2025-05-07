'''
 * The test doing the following:
 * 1. Navigate to Wikipedia's homepage
 * 2. Assert there are less than 7,000,000 articles in English
 * 3. Assert the page's text gets smaller when the 'Small' text size option is selected
 * 4. Assert the page's text gets larger when the 'Large' text size option is selected
 * 5. Assert the page's text goes back to the default size when the 'Standard' text size option is selected
 * 6. Assert the page goes dark when the 'Dark' color option is selected
 * 7. Assert the page goes light when the 'Light' color option is selected
 '''

import os
import re
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.skipif(
    not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "login.json")),
    reason="login.json not found in the root folder"
)

def test_wikipedia_article_count_and_ui_preferences():
    # Use the correct path to access the login.json file in the root folder
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of the test file
    storage_path = os.path.join(root_dir, "..", "login.json")  # Construct the path to the root folder login.json

    print(f"Using login.json from: {storage_path}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state=storage_path)  # Pass
        page = context.new_page()

        # STEP 1: Go to Wikipedia main page
        page.goto("https://en.wikipedia.org/wiki/Main_Page")

        # STEP 2: Get article count
        total_text = page.locator('a[href="/wiki/Special:Statistics"]').nth(1).inner_text()
        print("Raw text:", total_text)
        match = re.search(r"([\d,]+)", total_text)
        count = int(match.group(1).replace(",", "")) if match else 0
        print("Parsed article count:", count)

        # STEP 3: Assert under 7 million
        assert count < 7_000_000

        # STEP 4: Capture default font size
        headline = page.locator("#mp-welcome")
        body = page.locator("body")
        default_font_size = headline.evaluate("el => window.getComputedStyle(el).fontSize")

        # STEP 5: Select 'Small' text size
        page.get_by_role("radio", name="Small").click()
        page.wait_for_timeout(200)
        small_font_size = headline.evaluate("el => window.getComputedStyle(el).fontSize")

        # STEP 6: Select 'Large' text size
        page.get_by_role("radio", name="Large").click()
        page.wait_for_timeout(200)
        large_font_size = headline.evaluate("el => window.getComputedStyle(el).fontSize")

        # STEP 7: Font size assertions
        assert float(small_font_size.replace("px", "")) < float(default_font_size.replace("px", ""))
        assert float(large_font_size.replace("px", "")) > float(small_font_size.replace("px", ""))

        # STEP 8: Reset to 'Standard'
        page.get_by_label("Standard").first.click()
        page.wait_for_timeout(200)
        restored_font_size = headline.evaluate("el => window.getComputedStyle(el).fontSize")
        assert restored_font_size == default_font_size

        # STEP 9: Theme: Dark
        page.get_by_role("radio", name="Dark").click()
        page.wait_for_timeout(200)
        dark_bg = body.evaluate("el => window.getComputedStyle(el).backgroundColor")
        assert dark_bg != "rgb(255, 255, 255)"

        # STEP 10: Theme: Light
        page.get_by_role("radio", name="Light").click()
        page.wait_for_timeout(200)
        light_bg = body.evaluate("el => window.getComputedStyle(el).backgroundColor")
        assert re.match(r"rgb\(24\d, 24\d, 25\d\)", light_bg)

        context.close()
        browser.close()
