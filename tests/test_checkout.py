
import pytest
from pathlib import Path

from src.data.excel_reader import ExcelReader
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / "test_data" / "test_data.xlsx"

reader = ExcelReader(EXCEL_FILE)
checkout_data = reader.read_data("CheckoutData")


@pytest.mark.parametrize(
    "test_data",
    checkout_data,
    ids=[record["test_case"] for record in checkout_data]
)
def test_checkout_with_excel_data(page, config, test_data):

    # Login
    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    login_page.open()

    login_page.login(
        test_data["username"],
        test_data["password"]
    )

    # Add product to cart
    inventory_page = InventoryPage(page)

    assert inventory_page.is_inventory_displayed()

    inventory_page.add_product_to_cart(
        "Sauce Labs Backpack"
    )

    assert inventory_page.get_cart_count() == 1

    # Open shopping cart
    inventory_page.open_cart()

    cart_page = CartPage(page)

    assert cart_page.get_product_count() == 1

    # Proceed to checkout
    cart_page.checkout()

    checkout_page = CheckoutPage(page)

    assert checkout_page.is_checkout_information_displayed()

    # Enter Excel-based checkout information
    checkout_page.enter_checkout_information(
        test_data["first_name"],
        test_data["last_name"],
        str(test_data["postal_code"])
    )

    checkout_page.continue_checkout()

    # Verify checkout overview
    assert checkout_page.is_checkout_overview_displayed()

    assert checkout_page.get_product_count() == 1

    assert "Sauce Labs Backpack" in checkout_page.get_product_names()

    # Finish checkout
    checkout_page.finish_checkout()

    # Verify order confirmation
    assert checkout_page.is_checkout_complete_displayed()

    actual_message = checkout_page.get_confirmation_message()

    assert test_data["expected_confirmation_text"] in actual_message
