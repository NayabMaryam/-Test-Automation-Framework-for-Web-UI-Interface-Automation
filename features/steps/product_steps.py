
from behave import when, then

from src.pages.product_page import ProductPage


@when('the user opens product "{product_name}"')
def step_open_product(context, product_name):

    context.inventory_page.open_product(product_name)

    context.product_page = ProductPage(
        context.page
    )


@then("the product details page should be displayed")
def step_verify_product_page(context):

    assert context.product_page.is_product_displayed()


@then('the product name should be "{expected_name}"')
def step_verify_product_name(context, expected_name):

    actual_name = context.product_page.get_product_name()

    assert actual_name == expected_name, (
        f"Expected product name: {expected_name}, "
        f"but found: {actual_name}"
    )


@then('the product description should contain "{expected_text}"')
def step_verify_product_description(context, expected_text):

    actual_description = (
        context.product_page.get_product_description()
    )

    assert expected_text in actual_description


@then("the product price should be {expected_price:f}")
def step_verify_product_price(context, expected_price):

    actual_price = context.product_page.get_product_price()

    assert actual_price == expected_price, (
        f"Expected price: {expected_price}, "
        f"but found: {actual_price}"
    )


@when("the user adds the product to the cart")
def step_add_product_to_cart(context):

    context.product_page.add_to_cart()


@when("the user removes the product from the cart")
def step_remove_product_from_cart(context):

    context.product_page.remove_from_cart()


@then("the product should be added to the cart")
def step_verify_product_added(context):

    assert context.product_page.get_cart_count() == 1


@then("the product should be removed from the cart")
def step_verify_product_removed(context):

    assert context.product_page.get_cart_count() == 0
    

@then("the cart should be empty")
def step_verify_cart_empty(context):

    assert context.product_page.get_cart_count() == 0