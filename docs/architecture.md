# Framework Architecture

## 1. Introduction

This document describes the architecture of the automated web UI testing framework developed using Python, Playwright, Pytest, and Behave.

The application under test is SauceDemo:

https://www.saucedemo.com/

The framework follows a modular design and uses the Page Object Model (POM) to separate browser interactions from test logic.

It supports two testing approaches:

- **Pytest:** Conventional automated UI testing with fixtures, parameterization, and Excel-based test data.
- **Behave:** Behavior-Driven Development (BDD) using Gherkin feature files and step definitions.

## 2. Architectural Overview

The framework is organized into the following logical layers:

1. Test Layer
2. Page Object Layer
3. Core Framework Layer
4. Data Management Layer
5. Configuration Layer

### 2.1 Test Layer

The test layer contains automated test cases and BDD scenarios.

**Pytest tests:**
- `tests/test_framework_setup.py`
- `tests/test_browser_manager.py`
- `tests/test_config_validation.py`
- `tests/test_base_page.py`
- `tests/test_excel_reader.py`
- `tests/test_login.py`
- `tests/test_inventory.py`
- `tests/test_checkout.py`

These tests validate framework functionality and application behavior.

**BDD tests:**

The `features/` directory contains Gherkin feature files for:

- Login
- Inventory
- Product Details
- Shopping Cart
- Checkout

Their corresponding step definitions are maintained in `features/steps/`.

### 2.2 Page Object Layer

The `src/pages/` directory implements the Page Object Model.

Each page class encapsulates its page-specific locators and interactions.

Current page objects include:

- `base_page.py`
- `login_page.py`
- `inventory_page.py`
- `product_page.py`
- `cart_page.py`
- `checkout_page.py`

The `BasePage` class provides reusable browser interaction methods that can be used by other page objects.

This approach reduces duplicated code and keeps test cases independent of low-level locator implementation.

### 2.3 Core Framework Layer

The `src/core/` directory contains the framework's browser and configuration management components.

**BrowserManager**

Responsible for launching and closing the selected browser.

Supported browser options:

- Chromium
- Google Chrome
- Microsoft Edge

**ConfigReader**

Reads centralized configuration settings from the YAML configuration file.

These settings include:

- Application base URL
- Browser selection
- Headless execution
- Default timeout
- Navigation timeout

**Configuration and fixtures**

The `conftest.py` file provides reusable Pytest fixtures.

The fixtures manage:

- Configuration initialization
- Browser lifecycle
- Page creation
- Default timeout configuration
- Browser and page cleanup

### 2.4 Data Management Layer

The `src/data/` directory contains reusable test data utilities.

#### ExcelReader

The `excel_reader.py` module implements reusable Excel-based test data reading using OpenPyXL.

The Excel workbook is stored at:

`test_data/test_data.xlsx`

The reader:

1. Opens the specified Excel workbook.
2. Retrieves the requested worksheet.
3. Reads the first row as column headers.
4. Validates missing or duplicate headers.
5. Reads subsequent rows.
6. Skips completely empty records.
7. Converts each record into a dictionary using the column headers as keys.
8. Closes the workbook after reading.

Example data structure:

```python
{
    "username": "standard_user",
    "password": "secret_sauce",
    "expected": "success"
}
```

This allows test cases to access test data using meaningful column names instead of hardcoded row positions.

#### Excel Test Data

The workbook contains dedicated worksheets for different test modules.

| Worksheet | Purpose |
|---|---|
| LoginData | Login test scenarios |
| CheckoutData | Checkout test scenarios |

The login and checkout Pytest modules retrieve their respective records using `ExcelReader`.

### 2.5 Configuration Layer

The `config/` directory contains centralized YAML configuration.

The configuration file controls application and browser settings without requiring changes to individual test cases.

### 2.6 Test Data Layer

The `test_data/` directory stores external test data files.

Current implementation:

- `test_data.xlsx`

Separating test data from test logic makes it easier to add, modify, and maintain test scenarios.

## 3. High-Level Execution Flow

### 3.1 Pytest Execution

1. Pytest discovers test cases.
2. Fixtures initialize configuration and browser resources.
3. Test data is retrieved from Excel where applicable.
4. Page Object classes perform browser interactions.
5. Assertions validate application behavior.
6. Fixtures close the browser and release resources.

### 3.2 Behave Execution

1. Behave loads Gherkin feature files.
2. Matching step definitions are executed.
3. Page Object classes perform browser interactions.
4. Assertions validate expected behavior.
5. Environment hooks manage browser and page lifecycle.

## 4. Design Principles

The framework follows these principles:

- **Modularity:** Responsibilities are separated into dedicated components.
- **Reusability:** Common browser operations and page interactions are implemented once.
- **Maintainability:** Page-specific changes are isolated within page objects.
- **Data-driven testing:** Pytest test scenarios can consume external Excel records.
- **Configuration management:** Browser and application settings are centralized.
- **Separation of concerns:** Test logic, browser interactions, configuration, and test data remain independent.

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Primary programming language |
| Playwright | Browser automation |
| Pytest | Test execution and fixtures |
| Behave | BDD testing |
| Gherkin | BDD scenario specification |
| OpenPyXL | Excel test data reading |
| PyYAML | YAML configuration management |
| Git and GitHub | Version control |
| GitHub Actions | Continuous integration |

## 6. Current Implementation Scope

The framework currently provides:

- Modular browser management.
- Page Object Model implementation.
- YAML-based configuration.
- Pytest fixtures.
- Login and inventory automation.
- Product details and shopping cart automation.
- Checkout automation.
- Excel-based test data reading.
- Pytest parameterization using Excel records.
- Excel reader validation tests.
- BDD automation using Behave.
- Cross-browser configuration.
- GitHub Actions workflow integration.

## 7. Known Limitations

- Excel-based data integration is currently implemented in the Pytest login and checkout modules. The Behave checkout steps still use directly defined test values.
- SauceDemo's `problem_user` account exhibits unexpected checkout information field behavior.
- Allure reporting and automated failure screenshots are not currently verified.
- Database-based test data integration and Redis integration are not implemented.