
import pytest

from src.pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username",
    [
        "standard_user",
        "locked_out_user",
        "invalid_user",
        "problem_user"
    ]
)
def test_login_with_redis_data(page, config, redis, username):

    test_data = redis.get_test_data(f"login_{username}")

    assert test_data is not None, (
        f"Redis test data not found for {username}"
    )

    login_page = LoginPage(
        page,
        config.get("application", "base_url")
    )

    login_page.open()

    login_page.login(
        test_data["username"],
        test_data["password"]
    )

    if test_data["expected"] == "success":

        assert page.url.endswith("/inventory.html")

    else:

        assert login_page.get_error_message()
