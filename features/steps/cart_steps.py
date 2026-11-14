
from behave import when, then

from src.pages.inventory_page import InventoryPage
from src.pages.cart_page import CartPage


@when('the user adds "{product_name}" to the cart')
def step_add_product_to_cart(context, product_name):

    context.inventory_page.add_product_to_cart(
        product_name
    )


@then('the cart badge should display "{expected_count}"')
def step_verify_cart_badge(context, expected_count):

    actual_count = context.inventory_page.get_cart_count()

    assert actual_count == int(expected_count), (
        f"Expected cart badge count: {expected_count}, "
        f"but found: {actual_count}"
    )


@when("the user opens the shopping cart")
def step_open_shopping_cart(context):

    context.inventory_page.open_cart()

    context.cart_page = CartPage(
        context.page
    )


@then("the cart page should be displayed")
def step_verify_cart_page(context):

    assert context.cart_page.is_cart_displayed()


@then("{expected_count:d} products should be displayed in the cart")
def step_verify_cart_product_count(context, expected_count):

    actual_count = context.cart_page.get_product_count()

    assert actual_count == expected_count, (
        f"Expected {expected_count} products in cart, "
        f"but found {actual_count}"
    )


@when('the user removes "{product_name}" from the cart')
def step_remove_product(context, product_name):

    context.cart_page.remove_product(
        product_name
    )


@then("{expected_count:d} product should remain in the cart")
def step_verify_remaining_products(context, expected_count):

    actual_count = context.cart_page.get_product_count()

    assert actual_count == expected_count, (
        f"Expected {expected_count} products remaining, "
        f"but found {actual_count}"
    )


@when("the user continues shopping")
def step_continue_shopping(context):

    context.cart_page.continue_shopping()

