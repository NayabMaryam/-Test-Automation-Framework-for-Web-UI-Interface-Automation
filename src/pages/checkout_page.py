from src.pages.base_page import BasePage


class CheckoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # Checkout information page locators
        self.first_name_input = "#first-name"
        self.last_name_input = "#last-name"
        self.postal_code_input = "#postal-code"
        self.continue_button = "#continue"
        self.cancel_button = "#cancel"

        # Error message locator
        self.error_message = ".error-message-container"

        # Checkout overview locators
        self.cart_items = ".cart_item"
        self.product_names = ".inventory_item_name"
        self.product_prices = ".inventory_item_price"
        self.cart_quantities = ".cart_quantity"

        self.item_total = ".summary_subtotal_label"
        self.tax = ".summary_tax_label"
        self.total = ".summary_total_label"

        self.finish_button = "#finish"

        # Checkout complete locators
        self.complete_header = ".complete-header"
        self.complete_text = ".complete-text"
        self.back_home_button = "#back-to-products"

        # Common page locator
        self.page_title = ".title"

    # Checkout Information

    def is_checkout_information_displayed(self):
        title = self.page.locator(self.page_title)

        title.wait_for(
            state="visible",
            timeout=15000
        )

        return (
            title.inner_text().strip()
            == "Checkout: Your Information"
        )

    def enter_checkout_information(
        self,
        first_name,
        last_name,
        postal_code
    ):
        self.fill(self.first_name_input, first_name)
        self.fill(self.last_name_input, last_name)
        self.fill(self.postal_code_input, str(postal_code))
    
    def continue_checkout(self):
        self.click(self.continue_button)

    def get_error_message(self):
        return self.get_text(self.error_message)

    # Checkout Overview

    def is_checkout_overview_displayed(self):
        return (
            self.is_visible(self.page_title)
            and self.get_text(self.page_title)
            == "Checkout: Overview"
        )

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
            self.cart_quantities
        ).all_inner_texts()

        return [
            int(quantity)
            for quantity in quantities
        ]

    def get_item_total(self):
        text = self.get_text(self.item_total)

        return float(text.split("$")[-1])

    def get_tax(self):
        text = self.get_text(self.tax)

        return float(text.split("$")[-1])

    def get_total(self):
        text = self.get_text(self.total)

        return float(text.split("$")[-1])

    def finish_checkout(self):
        self.click(self.finish_button)

    # Checkout Complete

    def is_checkout_complete_displayed(self):
        return (
            self.is_visible(self.complete_header)
            and self.get_text(self.complete_header)
            == "Thank you for your order!"
        )

    def get_confirmation_message(self):
        return self.get_text(self.complete_text)

    def back_home(self):
        self.click(self.back_home_button)