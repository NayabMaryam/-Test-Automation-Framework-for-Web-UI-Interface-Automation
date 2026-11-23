
import pytest
import allure

from playwright.sync_api import sync_playwright
from pathlib import Path

from src.core.config_reader import ConfigReader
from src.core.browser_manager import BrowserManager
from src.data.database_reader import DatabaseReader
from src.data.redis_reader import RedisReader
from src.data.excel_reader import ExcelReader


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

@pytest.fixture(scope="session")
def config():
    return ConfigReader()


# --------------------------------------------------
# BROWSER FIXTURE
# --------------------------------------------------

@pytest.fixture(scope="function")
def browser(config):

    with sync_playwright() as playwright:

        manager = BrowserManager(playwright, config)

        browser = manager.launch_browser()

        yield browser

        manager.close_browser()


# --------------------------------------------------
# PAGE FIXTURE
# --------------------------------------------------

@pytest.fixture(scope="function")
def page(browser, config, request):

    page = browser.new_page()

    page.set_default_timeout(
        config.get("timeouts", "default")
    )

    page.set_default_navigation_timeout(
        config.get("timeouts", "navigation")
    )

    # Store browser console logs for this test
    console_logs = []

    # Capture browser console messages
    page.on(
        "console",
        lambda message: console_logs.append(
            f"[{message.type.upper()}] {message.text}"
        )
    )

    # Capture JavaScript errors
    page.on(
        "pageerror",
        lambda error: console_logs.append(
            f"[JAVASCRIPT ERROR] {str(error)}"
        )
    )

    # Make logs accessible to the Allure reporting hook
    request.node._allure_console_logs = console_logs

    yield page

    page.close()


# --------------------------------------------------
# ALLURE FAILURE REPORTING
# --------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    # Generate attachments only when the test call fails
    if report.when == "call" and report.failed:

        page = item.funcargs.get("page")

        if page is not None and not page.is_closed():

            # Attach screenshot
            try:

                screenshot = page.screenshot(
                    full_page=True
                )

                allure.attach(
                    screenshot,
                    name=f"{item.name}_failure_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

            except Exception as error:

                allure.attach(
                    str(error),
                    name="Screenshot Capture Error",
                    attachment_type=allure.attachment_type.TEXT
                )

            # Attach browser URL and page information
            try:

                page_details = (
                    f"URL: {page.url}\n"
                    f"Title: {page.title()}"
                )

                allure.attach(
                    page_details,
                    name="Browser Page Details",
                    attachment_type=allure.attachment_type.TEXT
                )

            except Exception:
                pass

        # Attach browser console logs
        console_logs = getattr(
            item,
            "_allure_console_logs",
            []
        )

        if console_logs:

            allure.attach(
                "\n".join(console_logs),
                name="Browser Console Logs",
                attachment_type=allure.attachment_type.TEXT
            )

        # Attach pytest failure details
        allure.attach(
            str(report.longrepr),
            name="Test Failure Details",
            attachment_type=allure.attachment_type.TEXT
        )


# --------------------------------------------------
# DATABASE FIXTURE
# --------------------------------------------------

@pytest.fixture(scope="function")
def database(tmp_path):

    database_path = tmp_path / "test_database.db"

    reader = DatabaseReader(database_path)

    reader.initialize_database()

    yield reader


# --------------------------------------------------
# REDIS FIXTURE
# --------------------------------------------------

@pytest.fixture(scope="function")
def redis(config):

    host = config.get("redis", "host")
    port = config.get("redis", "port")
    db = config.get("redis", "db")

    reader = RedisReader(host, port, db)

    yield reader

    reader.close_connection()


# --------------------------------------------------
# REDIS TEST DATA SEEDING
# --------------------------------------------------

@pytest.fixture(scope="session")
def seed_redis_test_data(config):

    project_root = Path(__file__).resolve().parents[1]

    excel_reader = ExcelReader(
        project_root / "test_data" / "test_data.xlsx"
    )

    redis = RedisReader(
        config.get("redis", "host"),
        config.get("redis", "port"),
        config.get("redis", "db")
    )

    seeded_keys = []

    try:

        # Seed login data
        login_records = excel_reader.read_data("LoginData")

        for record in login_records:

            key = f"login_{record['username']}"

            redis.store_test_data(key, record)
            seeded_keys.append(key)

            print(f"Seeded Redis: {key}")

        # Seed checkout data
        checkout_records = excel_reader.read_data("CheckoutData")

        for record in checkout_records:

            key = f"checkout_{record['test_case']}"

            redis.store_test_data(key, record)
            seeded_keys.append(key)

            print(f"Seeded Redis: {key}")

        yield

    finally:

        # Clean up only the records seeded by this fixture
        for key in seeded_keys:

            redis.delete_test_data(key)

        redis.close_connection()
