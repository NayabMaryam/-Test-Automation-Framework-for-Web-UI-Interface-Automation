
from playwright.sync_api import sync_playwright
from src.core.config_reader import ConfigReader
from src.core.browser_manager import BrowserManager


def test_browser_manager_launch_and_close():

    config = ConfigReader()   # loads Browser configuration

    with sync_playwright() as playwright:  # starts Playwrite

        manager = BrowserManager(playwright, config)  # Creates browser manager object

        browser = manager.launch_browser()  # Launches configured browser

        assert browser is not None
        assert browser.is_connected()  # Checks browser is running

        manager.close_browser() # Closes teh browser

        assert manager.browser is None      # Confirms browser refrence was cleared
