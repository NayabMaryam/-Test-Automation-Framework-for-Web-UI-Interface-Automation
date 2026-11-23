
import pytest
import allure

from pathlib import Path

from src.data.excel_reader import ExcelReader
from src.pages.login_page import LoginPage


# --------------------------------------------------
# TEST DATA
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXCEL_FILE = PROJECT_ROOT / "test_data" / "test_data.xlsx"

reader = ExcelReader(EXCEL_FILE)

login_data = reader.read_data("LoginData")


# --------------------------------------------------
# ALLURE METADATA
# --------------------------------------------------

@allure.feature("Authentication")

@allure.story("Login Functionality")

@allure.severity(allure.severity_level.CRITICAL)

@allure.description(
    """
    Validates login functionality using multiple
    test cases retrieved from an Excel data source.

    Both successful and unsuccessful login scenarios
    are covered.
    """
)

@allure.tag("UI Automation", "Excel Data Driven", "Login")


# --------------------------------------------------
# LOGIN TEST
# --------------------------------------------------

@pytest.mark.parametrize("test_data", login_data)

def test_login_with_excel_data(page, config, test_data):

    allure.dynamic.title(
        f"Login Validation: {test_data['expected']}"
    )

    with allure.step("Initialize Login Page"):

        login_page = LoginPage(
            page,
            config.get("application", "base_url")
        )

    with allure.step("Navigate to Application"):

        login_page.open()

    with allure.step("Enter Credentials and Submit Login"):

        login_page.login(
            test_data["username"],
            test_data["password"]
        )

    if test_data["expected"] == "success":

        with allure.step("Verify Successful Login"):

            assert page.url.endswith("/inventory.html")

    else:

        with allure.step("Verify Login Error Message"):

            assert login_page.get_error_message()
