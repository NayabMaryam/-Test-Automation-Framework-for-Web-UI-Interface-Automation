
class BrowserManager:

    def __init__(self, playwright, config):
        self.playwright = playwright
        self.config = config
        self.browser = None

    def launch_browser(self):

        browser_name = self.config.get("browser", "name")
        headless = self.config.get("browser", "headless")
        slow_mo = self.config.get("browser", "slow_mo")

        if browser_name == "chromium":
            browser_type = self.playwright.chromium

        elif browser_name == "chrome":
            browser_type = self.playwright.chromium
            browser = browser_type.launch(
                channel="chrome",
                headless=headless,
                slow_mo=slow_mo
            )
            self.browser = browser
            return self.browser

        elif browser_name == "edge":
            browser_type = self.playwright.chromium
            browser = browser_type.launch(
                channel="msedge",
                headless=headless,
                slow_mo=slow_mo
            )
            self.browser = browser
            return self.browser

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        self.browser = browser_type.launch(
            headless=headless,
            slow_mo=slow_mo
        )

        return self.browser

    def close_browser(self):
        if self.browser:
            self.browser.close()
            self.browser = None