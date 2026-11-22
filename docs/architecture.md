# Framework Architecture

## 1. Introduction

This document describes the architecture of the automated web UI testing framework developed using Python, Playwright, Pytest, and Behave.

The application under test is SauceDemo:

[https://www.saucedemo.com/](https://www.saucedemo.com/)

The framework follows a modular design and uses the Page Object Model (POM) to separate browser interactions from test logic.

It supports two testing approaches:

- **Pytest:** Conventional automated UI testing with fixtures, parameterization, and external test data sources.
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
- `tests/test_database_reader.py`
- `tests/test_login.py`
- `tests/test_inventory.py`
- `tests/test_checkout.py`

These tests validate framework functionality, data management operations, and application behavior.

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
- Database file path

It also validates required configuration sections and settings before test execution.

Environment variables can override browser selection and enable headless execution in CI environments.

**Configuration and fixtures**

The `conftest.py` file provides reusable Pytest fixtures.

The fixtures manage:

- Configuration initialization.
- Browser lifecycle.
- Page creation.
- Default timeout configuration.
- Browser and page cleanup.
- SQLite database initialization for individual database tests.

The database fixture uses Pytest's `tmp_path` fixture to create an isolated temporary database for each test function.

### 2.4 Data Management Layer

The `src/data/` directory contains reusable test data utilities.

The framework currently supports Excel-based and SQLite-based test data management.

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

#### DatabaseReader

The `database_reader.py` module implements SQLite-based test data management.

The database reader provides reusable functionality for connecting to the SQLite database and performing database operations.

The implementation supports:

1. Establishing SQLite database connections.
2. Executing SQL queries with parameterized values.
3. Initializing the database and creating the required `test_data` table.
4. Inserting test data records.
5. Retrieving all stored test data records.
6. Retrieving records using their test case names.
7. Updating existing test data records.
8. Deleting records using their record IDs.

Database configuration is maintained in:

`config/config.yaml`

The configured database path is:

`database/test_data.db`

The database reader uses the configured database path when initialized by the framework.

**Database Test Data Structure**

The `test_data` table stores test records with the following information:

- Record ID
- Test case name
- Username
- Password
- Expected result

**Database Fixture**

A reusable `database` fixture is defined in `conftest.py`.

It:

1. Creates a temporary database path using Pytest's `tmp_path`.
2. Initializes a `DatabaseReader` instance.
3. Creates the required database table.
4. Provides the initialized reader to database tests.

Using an isolated temporary database prevents database test cases from interfering with one another.

**Database Validation**

The `tests/test_database_reader.py` module validates:

- Database connection.
- SQL query execution.
- Database initialization.
- Test data insertion.
- Retrieval of all test data.
- Retrieval by test case.
- Test data updating.
- Test data deletion.
- Deletion of nonexistent records.

The database reader tests use temporary databases to maintain test isolation.

### 2.5 Configuration Layer

The `config/` directory contains centralized YAML configuration.

The configuration file controls application and browser settings as well as database configuration.

Example:

```yaml
application:
  name: "UI Test Automation Framework"
  base_url: "https://www.saucedemo.com"

browser:
  name: "chromium"
  headless: false
  slow_mo: 0

timeouts:
  default: 30000
  navigation: 60000

database:
  path: "database/test_data.db"

test:
  screenshot_on_failure: true
```

The database path is configurable, allowing the database location to be changed without modifying the database reader implementation.

The `ConfigReader` validates that the database path is present, is a string, and is not empty.

### 2.6 Test Data Layer

The `test_data/` and `database/` directories store external test data resources.

Current implementation:

- `test_data/test_data.xlsx` - Excel-based test data.
- `database/test_data.db` - SQLite database file configured for framework use.

Excel and SQLite provide separate mechanisms for storing and retrieving test data.

Separating test data from test logic makes it easier to maintain, update, and reuse test scenarios.

## 3. High-Level Execution Flow

### 3.1 Pytest Execution

1. Pytest discovers test cases.
2. Fixtures initialize configuration and browser resources where required.
3. Test data is retrieved from Excel or SQLite, depending on the test module.
4. Page Object classes perform browser interactions.
5. Assertions validate application behavior.
6. Fixtures close the browser and release resources.

**Database-specific execution:**

1. Pytest requests the `database` fixture.
2. The fixture creates an isolated temporary database.
3. `DatabaseReader` establishes the connection.
4. The required database table is initialized.
5. Test cases perform insertion, retrieval, updating, or deletion operations.
6. Assertions validate the results.

### 3.2 Behave Execution

1. Behave loads Gherkin feature files.
2. Matching step definitions are executed.
3. Page Object classes perform browser interactions.
4. Assertions validate expected behavior.
5. Environment hooks manage browser and page lifecycle.

## 4. Design Principles

The framework follows these principles:

- **Modularity:** Responsibilities are separated into dedicated components.
- **Reusability:** Common browser operations and data management operations are implemented once.
- **Maintainability:** Page-specific changes are isolated within page objects.
- **Data-driven testing:** Pytest test scenarios can consume external Excel and SQLite test data.
- **Configuration management:** Browser, application, and database settings are centralized.
- **Separation of concerns:** Test logic, browser interactions, configuration, and test data remain independent.
- **Test isolation:** Database tests use separate temporary databases to avoid interference between test cases.

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Primary programming language |
| Playwright | Browser automation |
| Pytest | Test execution and fixtures |
| Behave | BDD testing |
| Gherkin | BDD scenario specification |
| OpenPyXL | Excel test data reading |
| SQLite | Database-based test data management |
| PyYAML | YAML configuration management |
| Git and GitHub | Version control |
| GitHub Actions | Continuous integration |

SQLite is provided through Python's built-in `sqlite3` module and does not require a separate database server.

## 6. Current Implementation Scope

The framework currently provides:

- Modular browser management.
- Page Object Model implementation.
- YAML-based configuration and validation.
- Reusable Pytest fixtures.
- Login and inventory automation.
- Product details and shopping cart automation.
- Checkout automation.
- Excel-based test data reading.
- Pytest parameterization using Excel records.
- Excel reader validation tests.
- SQLite database connection and query execution.
- SQLite database initialization.
- Test data insertion and retrieval.
- Test data updating and deletion.
- Database path configuration and validation.
- Isolated database testing using Pytest fixtures.
- Database reader validation tests.
- BDD automation using Behave.
- Cross-browser configuration.
- GitHub Actions workflow integration.

## 7. Known Limitations

- Excel-based data integration is currently implemented in the Pytest login and checkout modules. The Behave checkout steps still use directly defined test values.
- SQLite database operations are implemented and tested independently. The existing login and checkout Pytest modules still primarily use Excel as their test data source.
- Redis-based test data integration is not implemented.
- SauceDemo's `problem_user` account exhibits unexpected checkout information field behavior.
- Allure reporting and automated failure screenshots are not currently verified.