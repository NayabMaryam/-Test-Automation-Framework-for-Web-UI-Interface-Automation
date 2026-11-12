from src.pages.base_page import BasePage


def test_base_page_methods(page):

    base_page = BasePage(page)

    # Test navigation
    base_page.navigate("https://example.com")

    # Test page title
    assert page.title() == "Example Domain"

    # Test visibility
    assert base_page.is_visible('p[lang="en"]')

    # Test getting text
    paragraph = base_page.get_text('p[lang="en"]')
    assert "This domain is for use" in paragraph

    print("BasePage methods are working successfully!")