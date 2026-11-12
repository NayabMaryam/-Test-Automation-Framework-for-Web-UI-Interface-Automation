
def test_browser_setup(page, config):
    # Open a test website
    page.goto("https://example.com")

    # Verify page title
    assert page.title() == "Example Domain"

    # Verify configuration
    assert config.get("browser", "name") == "chromium"

    print("Browser and configuration fixtures are working!")
