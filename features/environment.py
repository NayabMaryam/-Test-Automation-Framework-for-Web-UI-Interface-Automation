

from pathlib import Path

from playwright.sync_api import sync_playwright

from src.core.config_reader import ConfigReader
from src.core.browser_manager import BrowserManager


def before_all(context):
    """
    Runs once before all Behave scenarios.
    Loads configuration and launches the browser.
    """

    context.config_reader = ConfigReader()

    context.playwright = sync_playwright().start()

    context.browser_manager = BrowserManager(
        context.playwright,
        context.config_reader
    )

    context.browser = context.browser_manager.launch_browser()


def before_scenario(context, scenario):
    """
    Runs before every scenario.
    Creates a fresh browser page.
    """

    context.page = context.browser.new_page()

    context.page.set_default_timeout(
        context.config_reader.get("timeouts", "default")
    )

    context.page.set_default_navigation_timeout(
        context.config_reader.get("timeouts", "navigation")
    )


def after_scenario(context, scenario):
    """
    Runs after every scenario.
    Captures a screenshot if the scenario fails.
    Closes the browser page.
    """

    if scenario.status == "failed":

        screenshot_enabled = context.config_reader.get(
            "test",
            "screenshot_on_failure"
        )

        if screenshot_enabled:
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            safe_name = "".join(
                char if char.isalnum() or char in "-_" else "_"
                for char in scenario.name
            )

            screenshot_path = screenshot_dir / f"{safe_name}.png"

            context.page.screenshot(
                path=str(screenshot_path),
                full_page=True
            )

            print(f"Screenshot saved: {screenshot_path}")

    context.page.close()


def after_all(context):
    """
    Runs once after all Behave scenarios.
    Closes the browser and Playwright.
    """

    if hasattr(context, "browser_manager"):
        context.browser_manager.close_browser()

    if hasattr(context, "playwright"):
        context.playwright.stop()
