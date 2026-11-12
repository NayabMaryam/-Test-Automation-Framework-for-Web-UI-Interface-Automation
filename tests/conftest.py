import pytest
from playwright.sync_api import sync_playwright
from src.core.config_reader import ConfigReader
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
        browser_name = config.get("browser", "name")
        headless = config.get("browser", "headless")
        slow_mo = config.get("browser", "slow_mo")

        browser_type = getattr(playwright, browser_name)

        browser = browser_type.launch(
            headless=headless,
            slow_mo=slow_mo
        )

        yield browser   #(Test ko browser provide karta hai)

        browser.close()   #(Test complete hone ke baad browser close karta hai)

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
