# UI Test Automation Framework

## 1. Project Overview

The UI Test Automation Framework is a Python-based web UI testing solution developed using Playwright, Pytest, and Behave.

The framework automates testing of the [SauceDemo](https://www.saucedemo.com/) web application.

It follows the Page Object Model (POM) design pattern to improve code reusability, maintainability, and separation of test logic from browser interactions.

The framework supports conventional automated testing using Pytest and Behavior-Driven Development (BDD) using Behave and Gherkin.

It also provides centralized configuration management, external test data integration, database operations, and cross-browser execution through GitHub Actions.

## 2. Implemented Features

### Core Framework
- Browser management using Playwright.
- Support for Chromium, Google Chrome, and Microsoft Edge.
- Centralized YAML-based configuration.
- Environment variable overrides for browser selection and CI execution.
- Configuration validation.
- Reusable Pytest fixtures for configuration, browser, page, and database management.
- Page Object Model (POM).

### UI Automation
- Login automation.
- Inventory page validation.
- Product details and product selection.
- Shopping cart operations.
- Checkout information and order completion.
- Data-driven UI test execution.

### Test Data Integration
- Excel-based test data reading using OpenPyXL.
- Separate Excel worksheets for login and checkout scenarios.
- SQLite database connectivity.
- Database initialization and table creation.
- Test data insertion, retrieval, updating, and deletion.
- Parameterized tests using external test data.

### BDD Testing
- Gherkin-based feature files.
- Behave step definitions.
- Login, inventory, product, shopping cart, and checkout scenarios.
- Browser lifecycle management through Behave environment hooks.

### Continuous Integration
- GitHub Actions workflow integration.
- Automated test execution on pushes and pull requests targeting the main branch.
- Browser matrix configuration for cross-browser testing.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Primary programming language |
| Playwright | Browser automation |
| Pytest | Test execution, fixtures, and parameterization |
| Behave | BDD test execution |
| Gherkin | BDD scenario specification |
| OpenPyXL | Excel test data reading |
| SQLite | Database-based test data management |
| PyYAML | YAML configuration handling |
| Git and GitHub | Version control and collaboration |
| GitHub Actions | Continuous Integration |

## 4. Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── automation.yml
│
├── config/
│   └── config.yaml
│
├── database/
│   └── test_data.db
│
├── docs/
│   ├── architecture.md
│   ├── setup_guide.md
│   └── test_execution.md
│
├── src/
│   ├── core/
│   │   ├── browser_manager.py
│   │   └── config_reader.py
│   │
│   ├── data/
│   │   ├── excel_reader.py
│   │   └── database_reader.py
│   │
│   ├── pages/
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   ├── product_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   │
│   └── utilities/
│
├── test_data/
│   └── test_data.xlsx
│
├── tests/
│   ├── test_framework_setup.py
│   ├── test_browser_manager.py
│   ├── test_config_validation.py
│   ├── test_base_page.py
│   ├── test_excel_reader.py
│   ├── test_database_reader.py
│   ├── test_login.py
│   ├── test_inventory.py
│   └── test_checkout.py
│
├── features/
│   ├── steps/
│   ├── login.feature
│   ├── inventory.feature
│   ├── product.feature
│   ├── cart.feature
│   └── checkout.feature
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

The structure represents the main framework components. Additional supporting files may exist within individual directories.

## 5. Application Under Test

**Application:** SauceDemo

**URL:** https://www.saucedemo.com/

The framework validates different application functionalities, including authentication, product browsing, shopping cart operations, and checkout workflows.

## 6. Cross-Browser Testing

The framework supports three browser options:

- Chromium
- Google Chrome
- Microsoft Edge

Browser selection is managed through the `BROWSER` environment variable.

Examples:

```powershell
$env:BROWSER = "chromium"
pytest -v
```

```powershell
$env:BROWSER = "chrome"
pytest -v
```

```powershell
$env:BROWSER = "edge"
pytest -v
```

GitHub Actions is configured with a browser matrix to execute the automated test suite across the supported browser options.

## 7. Test Execution

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
python -m playwright install
```

### Execute all Pytest tests

```bash
pytest -v
```

### Execute individual test modules

```bash
pytest tests/test_login.py -v
pytest tests/test_inventory.py -v
pytest tests/test_checkout.py -v
pytest tests/test_excel_reader.py -v
pytest tests/test_database_reader.py -v
pytest tests/test_config_validation.py -v
```

### Execute BDD tests

Run all Behave features:

```bash
behave
```

Run an individual feature:

```bash
behave features/login.feature
```

### Headless execution

```powershell
$env:CI = "true"
pytest -v
```

For additional commands and instructions, refer to `docs/test_execution.md`.

## 8. Test Data Management

The framework supports two implemented test data sources.

### Excel Integration

Excel test data is stored in:

`test_data/test_data.xlsx`

The workbook contains:

- `LoginData`: Login test scenarios.
- `CheckoutData`: Checkout test scenarios.

The reusable Excel reader is implemented in:

`src/data/excel_reader.py`

### SQLite Database Integration

SQLite database functionality is implemented in:

`src/data/database_reader.py`

The database path is configured in:

`config/config.yaml`

Current database configuration:

```yaml
database:
  path: "database/test_data.db"
```

The database reader supports:

- Database connection management.
- SQL query execution.
- Database initialization.
- Test data insertion.
- Retrieving all test records.
- Retrieving records by test case.
- Updating existing test records.
- Deleting test records.

Database functionality is validated through:

`tests/test_database_reader.py`

The database integration provides reusable operations for managing test data during framework execution.

**Note:** Redis integration is not currently implemented.

## 9. Continuous Integration

GitHub Actions is configured to execute automated tests when:

- Code is pushed to the `main` branch.
- A pull request targets the `main` branch.

Workflow configuration:

`.github/workflows/automation.yml`

The workflow uses a browser matrix for cross-browser test execution.

Workflow results and individual job logs can be inspected through the Actions tab of the GitHub repository.

## 10. Current Test Results

**Latest verified local Pytest execution:**

| Metric | Result |
|---|---:|
| Tests collected | 28 |
| Passed | 28 |
| Failed | 0 |
| Execution time | 34.61 seconds |

The passing tests cover:

- Browser management.
- Configuration validation.
- Base page functionality.
- Framework setup.
- Excel reader functionality.
- SQLite database operations.
- Login automation.
- Inventory and product listing.
- Checkout scenarios.

These results represent the latest reported local execution and do not independently establish the status of GitHub Actions or the complete Behave suite.

## 11. Current Limitations

- Redis-based test data integration is not implemented.
- Excel-based test data integration is currently implemented in the Pytest login and checkout modules, not throughout Behave.
- The SauceDemo `problem_user` account exhibits unexpected behavior during checkout information entry.
- Allure reporting is not currently verified.
- Automatic screenshot capture on test failure is not currently verified.

## 12. Team Responsibilities

**Member 1: Framework and UI Automation**
- Browser management.
- Configuration management.
- Pytest fixtures.
- Base Page and Page Object Model.
- Login and Inventory automation.
- GitHub Actions and cross-browser testing.

**Member 2: Framework Extensions and Data Integration**
- BDD and Gherkin integration.
- Additional page objects.
- Excel-based test data integration.
- SQLite database integration.
- Database test coverage.
- Additional test scenarios and framework documentation.

## 13. Project Status

The framework currently provides modular UI automation, Pytest and Behave testing, centralized configuration, Excel-based test data reading, SQLite database operations, and GitHub Actions integration.

The latest reported local Pytest execution completed successfully with 28 passing tests.

Redis integration and other planned extensions remain outside the current verified implementation.