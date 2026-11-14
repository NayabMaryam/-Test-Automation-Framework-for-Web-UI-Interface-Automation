
from behave import given, when, then

from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage


@given("the user is logged in to SauceDemo")
def step_user_logged_in(context):

    base_url = context.config_reader.get(
        "application",
        "base_url"
    )

    context.login_page = LoginPage(
        context.page,
        base_url
    )

    context.login_page.open()

    context.login_page.login(
        "standard_user",
        "secret_sauce"
    )

    assert context.page.url.endswith("/inventory.html")


@given("the user is on the inventory page")
def step_user_on_inventory_page(context):

    context.inventory_page = InventoryPage(
        context.page
    )

    assert context.inventory_page.is_inventory_displayed()


@then('the inventory page title should be "{expected_title}"')
def step_verify_inventory_title(context, expected_title):

    actual_title = context.inventory_page.get_page_title()

    assert actual_title == expected_title


@then("the inventory container should be visible")
def step_verify_inventory_container(context):

    assert context.inventory_page.is_inventory_displayed()


@then("{expected_count:d} products should be displayed")
def step_verify_product_count(context, expected_count):

    actual_count = context.inventory_page.get_product_count()

    assert actual_count == expected_count, (
        f"Expected {expected_count} products, "
        f"but found {actual_count}"
    )


@then("the following products should be displayed")
def step_verify_product_names(context):

    expected_names = [
        row["product_name"]
        for row in context.table
    ]

    actual_names = context.inventory_page.get_product_names()

    assert actual_names == expected_names, (
        f"Expected products: {expected_names}\n"
        f"Actual products: {actual_names}"
    )


@when('the user sorts products by "{option}"')
def step_sort_products(context, option):

    context.inventory_page.sort_products(option)


@then("products should be sorted alphabetically")
def step_verify_alphabetical_sort(context):

    actual_names = context.inventory_page.get_product_names()

    expected_names = sorted(
        actual_names,
        key=str.lower
    )

    assert actual_names == expected_names


@then("products should be sorted by price in ascending order")
def step_verify_price_sort(context):

    actual_prices = context.inventory_page.get_product_prices()

    expected_prices = sorted(actual_prices)

    assert actual_prices == expected_prices

@then("the following products should be displayed:")
def step_verify_product_names(context):

    expected_products = [
        row["product_name"]
        for row in context.table
    ]

    actual_products = context.inventory_page.get_product_names()

    assert actual_products == expected_products, (
        f"Expected products: {expected_products}\n"
        f"Actual products: {actual_products}"
    )