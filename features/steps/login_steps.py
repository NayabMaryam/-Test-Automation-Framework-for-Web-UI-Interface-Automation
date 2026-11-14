from behave import given, when, then

from src.pages.login_page import LoginPage


@given("the user is on the SauceDemo login page")
def step_open_login_page(context):

    base_url = context.config_reader.get(
        "application",
        "base_url"
    )

    context.login_page = LoginPage(
        context.page,
        base_url
    )

    context.login_page.open()


@when('the user logs in with username "{username}" and password "{password}"')
def step_login_with_credentials(context, username, password):

    if username == "EMPTY":
        username = ""

    if password == "EMPTY":
        password = ""

    context.login_page.login(username, password)


@then("the inventory page should be displayed")
def step_verify_inventory_page(context):

    assert context.page.url.endswith("/inventory.html")

    assert context.page.locator(".title").inner_text() == "Products"


@then('the login error message should contain "{error_message}"')
def step_verify_login_error(context, error_message):

    actual_message = context.login_page.get_error_message()

    assert error_message in actual_message, (
        f"Expected error containing '{error_message}', "
        f"but received '{actual_message}'"
    )
