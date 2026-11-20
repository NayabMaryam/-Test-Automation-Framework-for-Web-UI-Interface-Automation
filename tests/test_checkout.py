
from playwright.sync_api import expect
import pytest
from pathlib import Path

from src.data.excel_reader import ExcelReader
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage


# Excel file path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / "test_data" / "test_data.xlsx"

# Read checkout data from Excel
reader = ExcelReader(EXCEL_FILE)
checkout_data = reader.read_data("CheckoutData")


@pytest.mark.parametrize(
    "test_data",
    checkout_data,
    ids=[record["test_case"] for record in checkout_data]
)
def test_checkout_with_excel_data(page, config, test_data):

    # -------------------------------
    # 1. Login
    # -------------------------------
    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)
    login_page.open()

    login_page.login(
        test_data["username"],
        test_data["password"]
    )

    # -------------------------------
    # 2. Add product to cart
    # -------------------------------
    inventory_page = InventoryPage(page)

    assert inventory_page.is_inventory_displayed()

    inventory_page.add_product_to_cart(
        "Sauce Labs Backpack"
    )

    assert inventory_page.get_cart_count() == 1

    # -------------------------------
    # 3. Open shopping cart
    # -------------------------------
    inventory_page.open_cart()

    cart_page = CartPage(page)

    expect(page.locator(".cart_item")).to_have_count(
        1,
        timeout=10000
    )

    # -------------------------------
    # 4. Proceed to checkout
    # -------------------------------
    cart_page.checkout()

    checkout_page = CheckoutPage(page)

    assert checkout_page.is_checkout_information_displayed()

    # -------------------------------
    # 5. Enter checkout information
    # -------------------------------
    checkout_page.enter_checkout_information(
        test_data["first_name"],
        test_data["last_name"],
        str(test_data["postal_code"])
    )

    # IMPORTANT: Click Continue before checking overview
    checkout_page.continue_checkout()

    # -------------------------------
    # 6. Verify problem_user defect
    # -------------------------------
    if test_data["username"] == "problem_user":

        # Verify that the application displays the observed defect
        assert "checkout-step-one.html" in page.url

        assert "Last Name is required" in (
            checkout_page.get_error_message()
        )

        # Verify incorrect field population
        first_name = page.locator("#first-name").input_value()
        last_name = page.locator("#last-name").input_value()

        assert first_name == test_data["last_name"]
        assert last_name == ""

        print(
            "\nEXPECTED DEFECT DETECTED: "
            "problem_user checkout form is not working correctly."
        )

        return

    # -------------------------------
    # 7. Verify checkout overview
    # -------------------------------
    assert checkout_page.is_checkout_overview_displayed()

    assert checkout_page.get_product_count() == 1

    assert (
        "Sauce Labs Backpack"
        in checkout_page.get_product_names()
    )

    # -------------------------------
    # 8. Finish checkout
    # -------------------------------
    checkout_page.finish_checkout()

    # -------------------------------
    # 9. Verify order confirmation
    # -------------------------------
    assert checkout_page.is_checkout_complete_displayed()

    actual_message = checkout_page.get_confirmation_message()

    assert (
        test_data["expected_confirmation_text"]
        in actual_message
    )
