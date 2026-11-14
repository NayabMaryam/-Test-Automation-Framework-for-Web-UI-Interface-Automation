from behave import given, when, then

from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage


def enter_valid_information(context):

    context.checkout_page = CheckoutPage(
        context.page
    )

    context.checkout_page.enter_checkout_information(
        "Tooba",
        "Nadeem",
        "38000"
    )

    context.checkout_page.continue_checkout()


@given('the user has added "{product_name}" to the cart')
def step_add_product_to_cart(context, product_name):

    context.inventory_page.add_product_to_cart(
        product_name
    )

    context.inventory_page.open_cart()

    context.cart_page = CartPage(
        context.page
    )

    context.cart_page.checkout()

    context.checkout_page = CheckoutPage(
        context.page
    )


@then("the checkout information page should be displayed")
def step_verify_checkout_information(context):

    assert context.checkout_page.is_checkout_information_displayed()


@when("the user continues checkout without entering information")
def step_continue_without_information(context):

    context.checkout_page.continue_checkout()


@then('the checkout error message should be "{expected_message}"')
def step_verify_checkout_error(context, expected_message):

    actual_message = context.checkout_page.get_error_message()

    assert actual_message == expected_message


@when("the user enters checkout information:")
def step_enter_checkout_information(context):

    data = context.table[0]

    context.checkout_page.enter_checkout_information(
        data["first_name"],
        data["last_name"],
        data["postal_code"]
    )

    context.checkout_page.continue_checkout()


@given("the user has entered valid checkout information")
def step_enter_valid_information(context):

    enter_valid_information(context)


@then("the checkout overview page should be displayed")
def step_verify_checkout_overview(context):

    assert context.checkout_page.is_checkout_overview_displayed()


@then("{expected_count:d} product should be displayed in the checkout overview")
def step_verify_checkout_product_count(context, expected_count):

    actual_count = context.checkout_page.get_product_count()

    assert actual_count == expected_count


@then('the checkout product should be "{expected_name}"')
def step_verify_checkout_product(context, expected_name):

    actual_names = context.checkout_page.get_product_names()

    assert expected_name in actual_names


@then("the checkout item total should be {expected_total:f}")
def step_verify_item_total(context, expected_total):

    actual_total = context.checkout_page.get_item_total()

    assert round(actual_total, 2) == round(expected_total, 2)


@then("the checkout tax should be {expected_tax:f}")
def step_verify_checkout_tax(context, expected_tax):

    actual_tax = context.checkout_page.get_tax()

    assert round(actual_tax, 2) == round(expected_tax, 2)


@then("the checkout total should be {expected_total:f}")
def step_verify_checkout_total(context, expected_total):

    actual_total = context.checkout_page.get_total()

    assert round(actual_total, 2) == round(expected_total, 2)


@when("the user finishes checkout")
def step_finish_checkout(context):

    context.checkout_page.finish_checkout()


@then("the checkout confirmation page should be displayed")
def step_verify_checkout_confirmation(context):

    assert context.checkout_page.is_checkout_complete_displayed()


@then('the order confirmation message should contain "{expected_text}"')
def step_verify_confirmation_message(context, expected_text):

    actual_message = context.checkout_page.get_confirmation_message()

    assert expected_text in actual_message


@given("the user has an empty cart")
def step_user_has_empty_cart(context):

    context.inventory_page.open_cart()

    context.cart_page = CartPage(
        context.page
    )

    product_names = context.cart_page.get_product_names()

    for product_name in product_names:
        context.cart_page.remove_product(product_name)

    context.cart_page.checkout()

    context.checkout_page = CheckoutPage(
        context.page
    )


@then("the checkout overview should contain 0 products")
def step_verify_empty_checkout(context):

    assert context.checkout_page.get_product_count() == 0