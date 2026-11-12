import pytest
from src.pages.login_page import LoginPage


def test_valid_login(page, config):

    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    login_page.open()

    login_page.login("standard_user", "secret_sauce")

    assert page.url.endswith("/inventory.html")

    print("Valid login test passed!")


def test_invalid_username(page, config):

    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    login_page.open()

    login_page.login("invalid_user", "secret_sauce")

    error = login_page.get_error_message()

    assert "Username and password do not match" in error

    print("Invalid username test passed!")

def test_empty_username(page, config):

    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    login_page.open()

    login_page.login("", "secret_sauce")

    error = login_page.get_error_message()

    assert "Username is required" in error

    print("Empty username test passed!")

def test_empty_password(page, config):

    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    login_page.open()

    login_page.login("standard_user", "")

    error = login_page.get_error_message()

    assert "Password is required" in error

    print("Empty password test passed!")

def test_locked_out_user(page, config):

    base_url = config.get("application", "base_url")

    login_page = LoginPage(page, base_url)

    login_page.open()

    login_page.login("locked_out_user", "secret_sauce")

    error = login_page.get_error_message()

    assert "Sorry, this user has been locked out" in error

    print("Locked-out user test passed!")