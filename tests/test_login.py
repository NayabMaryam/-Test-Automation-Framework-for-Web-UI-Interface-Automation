
import pytest
from pathlib import Path

from src.data.excel_reader import ExcelReader
from src.pages.login_page import LoginPage


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / "test_data" / "test_data.xlsx"


reader = ExcelReader(EXCEL_FILE)
login_data = reader.read_data("LoginData")


@pytest.mark.parametrize("test_data", login_data)
def test_login_with_excel_data(page, config, test_data):

    login_page = LoginPage(
        page,
        config.get("application", "base_url")
    )

    login_page.open()

    login_page.login(
        test_data["username"],
        test_data["password"]
    )

    if test_data["expected"] == "success":

        assert page.url.endswith("/inventory.html")

    else:

        assert login_page.get_error_message()
