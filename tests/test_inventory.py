from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage


def test_inventory_page_display(page, config):

    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    login_page.open()

    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(page)

    assert inventory_page.is_inventory_displayed()

    assert page.locator(".title").inner_text() == "Products"

    print("Inventory page display test passed!")


def test_product_listing(page, config):

    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    login_page.open()

    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(page)

    products = inventory_page.get_product_names()

    count = inventory_page.get_product_count()

    assert count > 0

    assert len(products) == count

    print("Total products:", count)
    print("Product listing test passed!")