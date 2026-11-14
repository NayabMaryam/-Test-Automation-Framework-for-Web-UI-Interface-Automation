
import pytest

from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage


def start_checkout(page, config):
    base_url = config.get("application", "base_url")

    # Login
    login_page = LoginPage(page, base_url)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    # Add product to cart
    inventory_page = InventoryPage(page)
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    inventory_page.open_cart()

    # Open checkout
    cart_page = CartPage(page)
    assert cart_page.is_cart_displayed()

    cart_page.checkout()

    checkout_page = CheckoutPage(page)

    return checkout_page


def test_checkout_information_display(page, config):
    checkout_page = start_checkout(page, config)

    assert checkout_page.is_checkout_information_displayed()


@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_error",
    [
        (
            "",
            "Maryam",
            "38000",
            "First Name is required"
        ),
        (
            "Maryam",
            "",
            "38000",
            "Last Name is required"
        ),
        (
            "Maryam",
            "Khan",
            "",
            "Postal Code is required"
        )
    ]
)
def test_checkout_required_fields(
    page,
    config,
    first_name,
    last_name,
    postal_code,
    expected_error
):
    checkout_page = start_checkout(page, config)

    checkout_page.enter_checkout_information(
        first_name,
        last_name,
        postal_code
    )

    checkout_page.continue_checkout()

    actual_error = checkout_page.get_error_message()

    assert expected_error in actual_error


def test_checkout_overview(page, config):
    checkout_page = start_checkout(page, config)

    checkout_page.enter_checkout_information(
        "Maryam",
        "Khan",
        "38000"
    )

    checkout_page.continue_checkout()

    assert checkout_page.is_checkout_overview_displayed()

    assert checkout_page.get_product_count() == 1

    assert "Sauce Labs Backpack" in checkout_page.get_product_names()

    assert checkout_page.get_product_quantities() == [1]


def test_checkout_price_calculation(page, config):
    checkout_page = start_checkout(page, config)

    checkout_page.enter_checkout_information(
        "Maryam",
        "Khan",
        "38000"
    )

    checkout_page.continue_checkout()

    item_total = checkout_page.get_item_total()
    tax = checkout_page.get_tax()
    total = checkout_page.get_total()

    assert total == pytest.approx(item_total + tax, abs=0.01)


def test_successful_checkout(page, config):
    checkout_page = start_checkout(page, config)

    checkout_page.enter_checkout_information(
        "Maryam",
        "Khan",
        "38000"
    )

    checkout_page.continue_checkout()

    assert checkout_page.is_checkout_overview_displayed()

    checkout_page.finish_checkout()

    assert checkout_page.is_checkout_complete_displayed()

    confirmation = checkout_page.get_confirmation_message()

    assert confirmation != ""


def test_back_home_after_checkout(page, config):
    checkout_page = start_checkout(page, config)

    checkout_page.enter_checkout_information(
        "Maryam",
        "Khan",
        "38000"
    )

    checkout_page.continue_checkout()
    checkout_page.finish_checkout()

    assert checkout_page.is_checkout_complete_displayed()

    checkout_page.back_home()

    assert page.url.endswith("/inventory.html")
