
from playwright.sync_api import expect
import pytest

from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage


@pytest.mark.parametrize(
    "test_case",
    [
        "valid_checkout",
        "valid_checkout_problem_user"
    ]
)
def test_checkout_with_redis_data(
    page,
    config,
    redis,
    test_case,
    seed_redis_test_data
):

    # -------------------------------
    # 1. Retrieve checkout data from Redis
    # -------------------------------
    test_data = redis.get_test_data(
        f"checkout_{test_case}"
    )

    assert test_data is not None, (
        f"Redis checkout data not found for {test_case}"
    )

    # -------------------------------
    # 2. Login
    # -------------------------------
    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)
    login_page.open()

    login_page.login(
        test_data["username"],
        test_data["password"]
    )

    # -------------------------------
    # 3. Add product to cart
    # -------------------------------
    inventory_page = InventoryPage(page)

    assert inventory_page.is_inventory_displayed()

    inventory_page.add_product_to_cart(
        "Sauce Labs Backpack"
    )

    assert inventory_page.get_cart_count() == 1

    # -------------------------------
    # 4. Open shopping cart
    # -------------------------------
    inventory_page.open_cart()

    cart_page = CartPage(page)

    expect(page.locator(".cart_item")).to_have_count(
        1,
        timeout=10000
    )

    # -------------------------------
    # 5. Proceed to checkout
    # -------------------------------
    cart_page.checkout()

    checkout_page = CheckoutPage(page)

    assert checkout_page.is_checkout_information_displayed()

    # -------------------------------
    # 6. Enter checkout information
    # -------------------------------
    checkout_page.enter_checkout_information(
        test_data["first_name"],
        test_data["last_name"],
        str(test_data["postal_code"])
    )

    checkout_page.continue_checkout()

    # -------------------------------
    # 7. Verify problem_user defect
    # -------------------------------
    if test_data["username"] == "problem_user":

        assert "checkout-step-one.html" in page.url

        assert "Last Name is required" in (
            checkout_page.get_error_message()
        )

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
    # 8. Verify checkout overview
    # -------------------------------
    assert checkout_page.is_checkout_overview_displayed()

    assert checkout_page.get_product_count() == 1

    assert (
        "Sauce Labs Backpack"
        in checkout_page.get_product_names()
    )

    # -------------------------------
    # 9. Finish checkout
    # -------------------------------
    checkout_page.finish_checkout()

    # -------------------------------
    # 10. Verify order confirmation
    # -------------------------------
    assert checkout_page.is_checkout_complete_displayed()

    actual_message = checkout_page.get_confirmation_message()

    assert (
        test_data["expected_confirmation_text"]
        in actual_message
    )
