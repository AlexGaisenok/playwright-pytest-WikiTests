'''
 *  The test is supposed to:
 * 1. Navigate to Wikipedia
 * 2. Go to the "Artificial intelligence" page
 * 3. Switch the language to Spanish and confirm the page was updated
 * 4. Switch the language to French and confirm the page was updated
 * 5. Click "View history"
 * 6. Assert that the latest edit was made by the user "Vega"
'''

import os
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.skipif(
    not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "login.json")),
    reason="login.json not found in the root folder"
)
def test_language_switch_and_history():
    # Use the correct path to access the login.json file in the root folder
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of the test file
    storage_path = os.path.join(root_dir, "..", "login.json")  # Construct the path to the root folder login.json

    print(f"Using login.json from: {storage_path}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state=storage_path)  # Pass
        page = context.new_page()

        # STEP 1: Navigate to Wikipedia
        page.goto("https://www.wikipedia.org/")

        # STEP 2: Search for "Artificial Intelligence"
        search_input = page.get_by_role("searchbox", name="Search Wikipedia")
        search_input.fill("artificial")

        page.locator("h3.suggestion-title").first.wait_for()
        page.locator("h3.suggestion-title", has_text="Artificial intelligence").first.click()

        # STEP 3: Switch to Spanish
        lang_button = page.locator('label[for="p-lang-btn-checkbox"]')
        lang_button.wait_for(state="visible", timeout=5000)
        lang_button.scroll_into_view_if_needed()
        try:
            lang_button.click(timeout=3000)
        except:
            lang_button.click(force=True)

        lang_search = page.get_by_role("textbox", name="Search for a language")
        lang_search.fill("espanol")

        spanish_link = page.locator('a[hreflang="es"].autonym').nth(1)
        spanish_link.wait_for(state="visible", timeout=5000)
        spanish_link.click()

        # STEP 4: Confirm it's in Spanish
        expect(page.locator("h1 span")).to_have_text("Inteligencia artificial")

        # STEP 5: Switch to French
        lang_button.wait_for(state="visible", timeout=5000)
        lang_button.scroll_into_view_if_needed()
        try:
            lang_button.click(timeout=3000)
        except:
            lang_button.click(force=True)

        french_search = page.get_by_role("textbox", name="Buscar un idioma")
        french_search.fill("francais")

        french_link = page.locator('a[hreflang="fr"].autonym').nth(1)
        french_link.wait_for(state="visible", timeout=5000)
        french_link.click()

        # STEP 6: Confirm it's in French
        expect(page.locator("h1 span")).to_have_text("Intelligence artificielle")

        # STEP 7: Click "View history"
        page.locator("#ca-history a").click()

        # STEP 8: Assert last edit was by Vega
        expect(
            page.locator("ul.mw-contributions-list > li")
            .first.locator("a.mw-userlink")
        ).to_have_text("Vega")

        print("✅ All steps passed.")
        browser.close()