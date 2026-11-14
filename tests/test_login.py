
import pytest

from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage


def test_valid_login(page, config):
    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)
    login_page.open()

    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(page)

    assert page.url.endswith("/inventory.html")
    assert inventory_page.is_inventory_displayed()
    assert inventory_page.get_page_title() == "Products"


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        (
            "invalid_user",
            "secret_sauce",
            "Username and password do not match"
        ),
        (
            "standard_user",
            "wrong_password",
            "Username and password do not match"
        ),
        (
            "",
            "secret_sauce",
            "Username is required"
        ),
        (
            "standard_user",
            "",
            "Password is required"
        ),
        (
            "locked_out_user",
            "secret_sauce",
            "Sorry, this user has been locked out"
        )
    ]
)
def test_invalid_login(
    page, config, username, password, expected_error
):
    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)
    login_page.open()

    login_page.login(username, password)

    actual_error = login_page.get_error_message()

    assert expected_error in actual_error
