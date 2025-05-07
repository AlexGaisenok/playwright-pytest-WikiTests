import os
import pytest
from playwright.sync_api import sync_playwright, expect
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True to run without UI
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

def test_login_and_storage_state(page):
    username = os.getenv("WIKIPEDIA_USERNAME")
    password = os.getenv("WIKIPEDIA_PASSWORD")

    if not username or not password:
        raise ValueError("Missing WIKIPEDIA_USERNAME or WIKIPEDIA_PASSWORD in .env file")

    # Navigate to Wikipedia
    page.goto("https://en.wikipedia.org/wiki/Main_Page")

    # Click the 'Log in' link
    page.click('//li[@id="pt-login-2"]//a//span[contains(text(), "Log in")]')

    # Fill in username and password
    page.fill("#wpName1", username)
    page.fill("#wpPassword1", password)

    # Click the login button
    page.click("#wpLoginAttempt")

    # Assert user is logged in
    expect(page.locator('#pt-userpage a')).to_have_text(username)

    # Save storage state
    script_dir = os.path.dirname(os.path.abspath(__file__))
    auth_file = os.path.join(script_dir,"login.json")  # Go up one level to the root folder
    page.context.storage_state(path=auth_file)
    print(f"Saved login storage state to: {auth_file}")

    # Verify storage state file exists
    assert os.path.exists(auth_file), "Storage state file was not created."
