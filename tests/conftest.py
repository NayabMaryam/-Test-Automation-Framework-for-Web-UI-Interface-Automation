import pytest
from playwright.sync_api import sync_playwright
from src.core.config_reader import ConfigReader
from src.core.browser_manager import BrowserManager
from src.data.database_reader import DatabaseReader
from src.data.redis_reader import RedisReader
from pathlib import Path
from src.data.excel_reader import ExcelReader

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

@pytest.fixture(scope="function")
def database(tmp_path):

    database_path = tmp_path / "test_database.db"

    reader = DatabaseReader(database_path)

    reader.initialize_database()

    yield reader

@pytest.fixture(scope="function")
def redis(config):

    host = config.get("redis", "host")
    port = config.get("redis", "port")
    db = config.get("redis", "db")

    reader = RedisReader(host, port, db)

    yield reader

    reader.close_connection()

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