import pytest
from playwright.sync_api import sync_playwright
from src.core.config_reader import ConfigReader
from src.core.browser_manager import BrowserManager
# provide configeration settings
# Fixture runs only once in whole test session
@pytest.fixture(scope="session")
def config():
    return ConfigReader()
# Launch and close the browser everytime(on each test case)
# Fresh Setup for every Test function
@pytest.fixture(scope="function")
def browser(config):

    with sync_playwright() as playwright:

        manager = BrowserManager(playwright, config)

        browser = manager.launch_browser()

        yield browser

        manager.close_browser()

# Provide new tab in browser for evry test
@pytest.fixture(scope="function")
def page(browser, config):

    page = browser.new_page()

    page.set_default_timeout(
        config.get("timeouts", "default")
    )

    page.set_default_navigation_timeout(
        config.get("timeouts", "navigation")
    )

    yield page

    page.close()
