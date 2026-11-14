
from src.pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # Cart page locators
        self.cart_items = ".cart_item"
        self.product_names = ".inventory_item_name"
        self.product_prices = ".inventory_item_price"
        self.cart_quantity = ".cart_quantity"
        self.page_title = ".title"
        self.remove_buttons = ".cart_button"
        self.continue_shopping_button = "#continue-shopping"
        self.checkout_button = "#checkout"

    def is_cart_displayed(self):
        self.page.locator(
            self.page_title
        ).wait_for(
            state="visible",
            timeout=15000
        )

        return self.get_text(self.page_title) == "Your Cart"


    def get_product_names(self):
        return self.page.locator(
            self.product_names
        ).all_inner_texts()

    def get_product_count(self):
        return self.page.locator(
            self.cart_items
        ).count()

    def get_product_prices(self):

        prices = self.page.locator(
            self.product_prices
        ).all_inner_texts()

        return [
            float(price.replace("$", ""))
            for price in prices
        ]

    def get_product_quantities(self):

        quantities = self.page.locator(
            self.cart_quantity
        ).all_inner_texts()

        return [
            int(quantity)
            for quantity in quantities
        ]

    def remove_product(self, product_name):

        product = self.page.locator(
            self.cart_items
        ).filter(
            has_text=product_name
        )

        product.locator("button").click()

    def continue_shopping(self):
        self.page.locator(
            self.continue_shopping_button
        ).click()

    def checkout(self):
        self.page.locator(
            self.checkout_button
        ).click()
