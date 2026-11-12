from src.pages.base_page import BasePage


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # Inventory page locators
        self.inventory_container = ".inventory_list"
        self.product_items = ".inventory_item"
        self.product_names = ".inventory_item_name"
        self.page_title = ".title"

    def is_inventory_displayed(self):
        return self.is_visible(self.inventory_container)

    def get_product_names(self):
        return self.page.locator(
            self.product_names
        ).all_inner_texts()

    def get_product_count(self):
        return self.page.locator(
            self.product_items
        ).count()