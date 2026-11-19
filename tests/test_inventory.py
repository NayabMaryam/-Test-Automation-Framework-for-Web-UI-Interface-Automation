
import pytest
from pathlib import Path

from src.data.excel_reader import ExcelReader
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / "test_data" / "test_data.xlsx"

reader = ExcelReader(EXCEL_FILE)
inventory_data = reader.read_data("InventoryData")


@pytest.mark.parametrize(
    "test_data",
    inventory_data,
    ids=[record["test_case"] for record in inventory_data]
)
def test_inventory_page_display(page, config, test_data):

    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    login_page.open()

    login_page.login(
        test_data["username"],
        test_data["password"]
    )

    inventory_page = InventoryPage(page)

    assert inventory_page.is_inventory_displayed()

    assert inventory_page.get_page_title() == test_data["expected_title"]


@pytest.mark.parametrize(
    "test_data",
    inventory_data,
    ids=[record["test_case"] for record in inventory_data]
)
def test_product_listing(page, config, test_data):

    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    login_page.open()

    login_page.login(
        test_data["username"],
        test_data["password"]
    )

    inventory_page = InventoryPage(page)

    products = inventory_page.get_product_names()

    count = inventory_page.get_product_count()

    assert count == int(test_data["expected_product_count"])

    assert len(products) == count
