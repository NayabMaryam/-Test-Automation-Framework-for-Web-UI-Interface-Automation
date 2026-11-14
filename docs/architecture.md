# Framework Architecture

## 1. Introduction

The UI Test Automation Framework follows a modular architecture using Python, Playwright, Pytest, and Behave.

The main objective of this architecture is to separate browser management, configuration, page interactions, test execution, and BDD test scenarios. This makes the framework easier to maintain, extend, and reuse.

The framework uses the Page Object Model (POM) design pattern and supports both traditional Pytest-based automation and Behavior-Driven Development (BDD) using Gherkin feature files.

## 2. Architectural Components

### 2.1 Core Layer

Location: `src/core/`

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

This layer contains page classes representing different pages of the SauceDemo application.

**BasePage**
- Provides reusable page interaction functionality.
- Acts as a base class for other page objects.

**LoginPage**
- Represents the SauceDemo login page.
- Contains login-related page interactions.

**InventoryPage**
- Represents the inventory page.
- Contains inventory-related page interactions.
- Supports product listing, sorting, and product selection.

**ProductPage**
- Represents the individual product details page.
- Retrieves product names, descriptions, and prices.
- Supports adding and removing products from the cart.
- Provides access to cart badge information.

**CartPage**
- Represents the shopping cart page.
- Contains cart-related page interactions.
- Supports viewing cart products, retrieving quantities and prices, and removing products.
- Provides navigation to checkout.

**CheckoutPage**
- Represents the checkout process.
- Supports checkout information entry and validation.
- Retrieves checkout overview details, including item totals, tax, and final total.
- Supports completing checkout and verifying order confirmation.

The Page Object Model keeps page interaction logic separate from test cases and BDD step definitions.

### 2.3 Test Layer

Location: `tests/`

The test layer contains Pytest-based automated test cases.

Responsibilities:
- Tests framework components.
- Tests browser management.
- Validates configuration.
- Tests login functionality.
- Tests inventory-related functionality.
- Executes automated test cases using Pytest.

The existing Pytest suite validates the core framework and its application interactions.

### 2.4 BDD Layer

Location: `features/`

The BDD layer implements Behavior-Driven Development using Behave and Gherkin syntax.

It separates application behavior descriptions from their implementation through feature files and step definitions.

**Feature Files (`features/`)**

Responsibilities:
- Describe application functionality using Gherkin keywords.
- Define features, scenarios, and expected outcomes.
- Provide readable specifications for application behavior.

The current implementation includes:

- `login.feature`: Defines valid and invalid login scenarios.
- `inventory.feature`: Defines inventory browsing, product listing, and sorting scenarios.
- `cart.feature`: Defines shopping cart management scenarios.
- `product.feature`: Defines individual product details and cart interaction scenarios.
- `checkout.feature`: Defines checkout information validation, checkout overview, order completion, and empty-cart checkout scenarios.

**Step Definitions (`features/steps/`)**

Responsibilities:
- Implement the Given, When, and Then steps defined in feature files.
- Connect Gherkin scenarios with application page objects.
- Execute browser interactions and validate expected results.
- Handle test data provided through Gherkin data tables.

Current step definition files:

- `login_steps.py`
- `inventory_steps.py`
- `cart_steps.py`
- `product_steps.py`
- `checkout_steps.py`

**Environment Configuration (`features/environment.py`)**

Responsibilities:
- Provides Behave environment hooks.
- Manages setup and teardown required for BDD execution.
- Initializes the resources required by BDD scenarios.

Behave executes the Gherkin scenarios through its own test runner.

### 2.5 Fixture Management

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

These fixtures support the Pytest execution path.

### 2.6 Configuration Layer

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

### 2.7 Continuous Integration Layer

Location: `.github/workflows/automation.yml`

GitHub Actions provides automated test execution.

The workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs project dependencies.
4. Installs the required Playwright browsers.
5. Executes the configured Pytest test suite.

A browser matrix is configured to run tests using:

- Chromium
- Google Chrome
- Microsoft Edge

The workflow is triggered by pushes and pull requests targeting the `main` branch.

The current workflow documents the Pytest execution path. Behave-based BDD execution is performed locally unless separately configured in the CI workflow.

## 3. Framework Execution Flow

The framework supports two test execution paths: Pytest-based automation and Behave-based BDD automation.

### 3.1 Pytest Execution Flow

The following diagram illustrates the traditional Pytest execution flow.

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
                   InventoryPage,
                   CartPage,
                   ProductPage,
                   CheckoutPage)
                       |
                       v
                    SauceDemo
                       |
                       v
                  Test Results
```

### 3.2 BDD Execution Flow

The following diagram illustrates the Behave-based BDD execution flow.

```text
Developer
    |
    v
Behave Test Runner
    |
    v
Gherkin Feature Files
(login.feature,
 inventory.feature,
 cart.feature,
 product.feature,
 checkout.feature)
    |
    v
Step Definitions
(features/steps/)
    |
    v
Behave Environment Hooks
(environment.py)
    |
    v
Browser and Page Setup
                       |
                       v
                   Page Objects
                  (LoginPage,
                   InventoryPage,
                   CartPage,
                   ProductPage,
                   CheckoutPage)
                       |
                       v
                    SauceDemo
                       |
                       v
                  Scenario Results
```

The BDD layer uses Gherkin feature files to describe application behavior and step definitions to execute the corresponding browser interactions.

## 4. Design Principles

The framework follows these design principles:

**Modularity:** Different responsibilities are separated into individual modules.

**Reusability:** Common browser and page operations can be reused.

**Maintainability:** Changes to page interactions can be handled within page objects instead of modifying every test case.

**Separation of Concerns:** Configuration, browser management, page interactions, test logic, and BDD specifications are maintained separately.

**Scalability:** Additional page objects, test cases, BDD scenarios, and integrations can be added as the framework develops.

**Cross-Browser Compatibility:** The same automation framework can execute tests on multiple supported browsers.

**Readability:** Gherkin feature files provide human-readable descriptions of application behavior.

## 5. Current Architecture Limitations

The following components are planned for future extensions and have not yet been implemented and verified:

- Excel-based test data integration.
- MySQL database integration.
- Redis integration.
- Allure reporting.
- Centralized logging and helper utilities.
- Automatic screenshot capture on test failure.
- Integration of Behave BDD execution into the GitHub Actions workflow.

These components will extend the framework's data management, reporting, debugging, and continuous integration capabilities.

## 6. Current Implementation and Test Validation

The current implementation has been locally verified using both Pytest and Behave.

**Previously Recorded Pytest Results:**
- 12 tests passed.
- 0 tests failed.

**Latest Independently Verified Behave Results:**

| Feature | Scenarios Passed | Steps Passed |
|---|---:|---:|
| Product | 3 | 20 |
| Cart | 5 | 29 |
| Checkout | 6 | 37 |

The checkout feature was successfully executed with all six scenarios and 37 steps passing, including checkout validation, order completion, and empty-cart checkout behavior.

These results represent individual feature executions. An updated combined execution should be performed before reporting an overall Behave test count.

## 7. Conclusion

The current architecture provides a modular foundation for web UI automation. It combines Pytest fixtures, Playwright browser management, centralized configuration, and Page Object Model design with Behave-based BDD testing.

The framework supports both conventional automated test cases and readable Gherkin-based behavioral scenarios.

Its modular structure provides a foundation for future extensions, including external test data sources, database integrations, advanced reporting, logging, and additional application workflows.