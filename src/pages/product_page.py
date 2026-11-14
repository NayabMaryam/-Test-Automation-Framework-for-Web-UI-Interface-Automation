from src.pages.base_page import BasePage


class ProductPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # Product details page locators
        self.product_container = ".inventory_details_container"
        self.product_name = ".inventory_details_name"
        self.product_description = ".inventory_details_desc"
        self.product_price = ".inventory_details_price"
        self.product_button = ".inventory_details_container button"
        self.back_to_products_button = "#back-to-products"

    def is_product_displayed(self):
        return self.is_visible(self.product_container)

    def get_product_name(self):
        return self.get_text(self.product_name)

    def get_product_description(self):
        return self.get_text(self.product_description)

    def get_product_price(self):
        price = self.get_text(self.product_price)

        return float(price.replace("$", ""))

    def add_to_cart(self):
        button = self.page.locator(self.product_button)

        if button.inner_text() == "Add to cart":
            button.click()

    def remove_from_cart(self):
        button = self.page.locator(self.product_button)

        if button.inner_text() == "Remove":
            button.click()

    def get_cart_count(self):
        cart_badge = self.page.locator(".shopping_cart_badge")

        if cart_badge.count() == 0:
            return 0

        return int(cart_badge.inner_text())

    def back_to_products(self):
        self.click(self.back_to_products_button)