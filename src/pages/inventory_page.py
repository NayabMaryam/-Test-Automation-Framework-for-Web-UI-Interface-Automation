
from src.pages.base_page import BasePage


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # Inventory page locators
        self.inventory_container = ".inventory_list"
        self.product_items = ".inventory_item"
        self.product_names = ".inventory_item_name"
        self.product_prices = ".inventory_item_price"
        self.page_title = ".title"
        self.sort_dropdown = ".product_sort_container"
        self.cart_badge = ".shopping_cart_badge"
        self.cart_link = ".shopping_cart_link"

    def is_inventory_displayed(self):
        return self.is_visible(self.inventory_container)

    def get_product_names(self):
        self.page.locator(self.product_names).first.wait_for(
            state="visible",
            timeout=15000
        )

        return self.page.locator(self.product_names).all_inner_texts()

    def get_product_count(self):
        return self.page.locator(
            self.product_items
        ).count()

    def get_page_title(self):
        return self.get_text(self.page_title)

    def get_product_prices(self):
        prices = self.page.locator(
            self.product_prices
        ).all_inner_texts()

        return [
            float(price.replace("$", ""))
            for price in prices
        ]

    def sort_products(self, option):
        self.page.locator(
            self.sort_dropdown
        ).select_option(label=option)

    def add_product_to_cart(self, product_name):

        product = self.page.locator(
            ".inventory_item"
        ).filter(
            has_text=product_name
        )

        product.locator("button").click()

    def get_cart_count(self):

        if self.page.locator(self.cart_badge).count() == 0:
            return 0

        return int(
            self.page.locator(self.cart_badge).inner_text()
        )

    def open_cart(self):
        self.page.locator(
            self.cart_link
        ).click()

    def open_product(self, product_name):
        product = self.page.locator(
            self.product_names
        ).filter(
            has_text=product_name
        )

        product.click()