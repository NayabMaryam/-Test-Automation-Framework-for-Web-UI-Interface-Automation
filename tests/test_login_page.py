from src.pages.login_page import LoginPage


def test_login_page_methods(page, config):

    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    # Test opening login page
    login_page.open()

    # Verify login page URL
    assert page.url == base_url + "/"

    # Verify login elements are visible
    assert login_page.is_visible(login_page.username_input)
    assert login_page.is_visible(login_page.password_input)
    assert login_page.is_visible(login_page.login_button)

    # Test login with invalid credentials
    login_page.login("invalid_user", "wrong_password")

    # Verify error message
    error = login_page.get_error_message()
    assert "Username and password do not match" in error

    print("LoginPage methods are working successfully!")