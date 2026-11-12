from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage


def test_inventory_page_methods(page, config):

    base_url = config.get("application", "base_url")

    # Open login page
    login_page = LoginPage(page, base_url)
    login_page.open()

    # Login with valid credentials
    login_page.login("standard_user", "secret_sauce")

    # Create InventoryPage object
    inventory_page = InventoryPage(page)

    # Verify inventory page is displayed
    assert inventory_page.is_inventory_displayed()

    # Get product names
    products = inventory_page.get_product_names()

    # Get product count
    count = inventory_page.get_product_count()

    # Verify products
    assert count > 0
    assert len(products) == count

    print("Products:", products)
    print("Total products:", count)
    print("InventoryPage methods are working successfully!")