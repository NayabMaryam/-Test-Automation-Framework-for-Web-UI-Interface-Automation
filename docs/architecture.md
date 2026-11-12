# Framework Architecture

## 1. Introduction

The UI Test Automation Framework follows a modular architecture using Python, Playwright, and Pytest.

The main objective of this architecture is to separate browser management, configuration, page interactions, and test execution. This makes the framework easier to maintain, extend, and reuse.

The framework uses the Page Object Model (POM) design pattern.

## 2. Architectural Components

### 2.1 Core Layer

The core layer manages framework configuration and browser initialization.

**ConfigReader (`src/core/config_reader.py`)**

Responsibilities:
- Loads configuration settings from `config/config.yaml`.
- Validates configuration values.
- Reads environment variables to override browser settings.
- Enables headless execution in CI environments.

**BrowserManager (`src/core/browser_manager.py`)**

Responsibilities:
- Initializes the selected browser.
- Supports Chromium, Chrome, and Edge.
- Provides browser launch and closing functionality.

### 2.2 Page Object Layer

Location: `src/pages/`

This layer contains page classes that represent the application's web pages.

**BasePage**
- Provides reusable page interaction functionality.
- Acts as a base class for other page objects.

**LoginPage**
- Represents the SauceDemo login page.
- Contains login-related page interactions.

**InventoryPage**
- Represents the inventory page.
- Contains inventory-related page interactions.

Using POM keeps page interaction logic separate from test cases.

### 2.3 Test Layer

Location: `tests/`

The test layer contains automated test cases.

Responsibilities:
- Tests framework components.
- Tests browser management.
- Validates configuration.
- Tests login functionality.
- Tests inventory-related functionality.
- Executes automated test scenarios using Pytest.

### 2.4 Fixture Management

File: `tests/conftest.py`

Pytest fixtures provide shared resources to test cases.

The current framework uses three main fixtures:

**Config Fixture**
- Scope: Session.
- Creates a ConfigReader instance.
- Reuses configuration throughout the test session.

**Browser Fixture**
- Scope: Function.
- Initializes Playwright.
- Launches the configured browser.
- Closes the browser after each test.

**Page Fixture**
- Scope: Function.
- Creates a new browser page for each test.
- Applies default and navigation timeouts.
- Closes the page after test execution.

### 2.5 Configuration Layer

Location: `config/config.yaml`

The YAML configuration file stores:

- Application name.
- Application URL.
- Browser selection.
- Headless execution setting.
- Slow motion setting.
- Default timeout.
- Navigation timeout.
- Screenshot-on-failure configuration flag.

Environment variables can override browser selection and headless execution for CI.

### 2.6 Continuous Integration Layer

Location: `.github/workflows/automation.yml`

GitHub Actions provides automated test execution.

The workflow:
1. Checks out the repository.
2. Sets up Python 3.13.
3. Installs project dependencies.
4. Installs the required Playwright browsers.
5. Executes the Pytest test suite.

A browser matrix runs the tests using:
- Chromium
- Chrome
- Microsoft Edge

The workflow is triggered by pushes and pull requests targeting the `main` branch.

## 3. Framework Execution Flow

The following diagram illustrates the current execution flow.

```text
Developer
    |
    v
Pytest Test Execution
    |
    v
Pytest Fixtures (conftest.py)
    |
    +------------------+
    |                  |
    v                  v
ConfigReader      BrowserManager
    |                  |
    v                  v
config.yaml       Playwright Browser
                       |
                       v
                  Browser Page
                       |
                       v
                  Page Objects
                  (BasePage,
                   LoginPage,
                   InventoryPage)
                       |
                       v
                  SauceDemo
                       |
                       v
                  Test Results
```

## 4. Design Principles

The framework follows these design principles:

**Modularity:** Different responsibilities are separated into individual modules.

**Reusability:** Common browser and page operations can be reused.

**Maintainability:** Changes to page interactions can be handled within page objects instead of modifying every test case.

**Separation of Concerns:** Configuration, browser management, page interactions, and test logic are maintained separately.

**Scalability:** Additional page objects, test cases, and integrations can be added as the framework develops.

**Cross-Browser Compatibility:** The same test suite can execute on multiple supported browsers.

## 5. Current Architecture Limitations

The following components are reserved for future extensions but are not implemented in the current verified version:

- BDD/Gherkin execution.
- Excel, MySQL, and Redis data integrations.
- Logging and helper utilities.
- Allure reporting.
- Automatic screenshot capture on test failure.

The architecture documentation describes the implemented core framework and does not treat these planned extensions as completed components.

## 6. Conclusion

The current architecture provides a modular foundation for web UI automation. It combines Pytest fixtures, Playwright browser management, centralized configuration, and Page Object Model design.

The framework has successfully executed its 13-test local suite and its three-browser GitHub Actions workflow.
