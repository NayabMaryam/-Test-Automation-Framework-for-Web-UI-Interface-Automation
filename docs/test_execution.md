# Test Execution Guide

## 1. Introduction

This document explains how to execute and verify automated UI tests using Python, Playwright, Pytest, and Behave.

The application under test is SauceDemo:

https://www.saucedemo.com/

The framework supports two testing approaches:

- **Pytest:** Conventional automated UI testing with fixtures and Excel-based test data.
- **Behave:** BDD testing using Gherkin feature files and step definitions.

## 2. Test Framework

The framework uses:

- **Pytest:** Test discovery, execution, parameterization, and fixtures.
- **Playwright:** Browser automation.
- **Behave:** BDD testing using Gherkin.
- **Page Object Model:** Separation of page interactions from test logic.
- **YAML:** Centralized configuration.
- **OpenPyXL:** Excel-based test data reading.
- **SQLite:** Database-based test data storage, retrieval, and management.
- **sqlite3:** Python's built-in SQLite database interface.

The framework supports reusable test data readers and centralized mechanisms for accessing external test data.

## 3. Test Directory

Automated Pytest test cases are located in the `tests/` directory.

The current Pytest suite covers:

- Framework setup.
- Configuration validation.
- Browser management.
- Base page functionality.
- Excel reader functionality and validation.
- SQLite database reader functionality.
- Login functionality and login scenarios.
- Inventory page functionality and product listing.
- Checkout scenarios using Excel-based test data.

BDD feature files and their step definitions are located in the `features/` directory.

The BDD implementation covers:

- **Login:** Valid and invalid login scenarios.
- **Inventory:** Product listing, product count, product names, and sorting.
- **Product Details:** Individual product information, product selection, and cart interactions.
- **Shopping Cart:** Cart contents, product removal, and cart badge validation.
- **Checkout:** Checkout information validation, checkout overview, price calculations, order completion, and empty-cart checkout behavior.

## 4. Execute All Pytest Tests

Activate the virtual environment and execute:

```bash
pytest -v
```

The `-v` option displays individual test names and execution results.

For more detailed output:

```bash
pytest -v -s
```

The `-s` option displays print statements during execution.

## 5. Execute Individual Pytest Files

To execute a specific test file:

```bash
pytest tests/test_login.py -v
```

Other examples:

```bash
pytest tests/test_browser_manager.py -v
pytest tests/test_config_validation.py -v
pytest tests/test_inventory.py -v
pytest tests/test_base_page.py -v
pytest tests/test_framework_setup.py -v
pytest tests/test_excel_reader.py -v
pytest tests/test_checkout.py -v
```

## 6. Excel-Based Test Execution

The framework uses OpenPyXL to read external test data from:

`test_data/test_data.xlsx`

The reusable Excel reader is implemented in:

`src/data/excel_reader.py`

The reader retrieves worksheet records as dictionaries using the first row as column headers.

### Login tests

The `LoginData` worksheet supplies login test records to:

`tests/test_login.py`

Execute:

```bash
pytest tests/test_login.py -v
```

### Checkout tests

The `CheckoutData` worksheet supplies checkout test records to:

`tests/test_checkout.py`

Execute:

```bash
pytest tests/test_checkout.py -v
```

### Excel reader validation

Execute:

```bash
pytest tests/test_excel_reader.py -v
```

The reader tests cover:

- Reading login data.
- Reading all login records.
- Missing Excel file handling.
- Missing worksheet handling.
- Duplicate header validation.

### Important distinction

Excel-based test data integration is currently implemented in the Pytest login and checkout modules.

The Behave implementation uses its existing step definitions and test values. It is not currently integrated with the Excel reader.

## 7. SQLite Database Integration

The framework includes SQLite-based test data management using Python's built-in `sqlite3` module.

The reusable database reader is implemented in:

`src/data/database_reader.py`

### Database Configuration

The database location is defined in:

`config/config.yaml`

Example:

```yaml
database:
  path: "database/test_data.db"
```

The configuration reader validates that the database path is present and contains a non-empty string.

### Database Initialization

The `DatabaseReader` provides an initialization mechanism that creates the `test_data` table if it does not already exist.

The table stores:

- `id`: Unique record identifier.
- `test_case`: Test case identifier.
- `username`: Login username.
- `password`: Login password.
- `expected`: Expected test outcome.

### Supported Database Operations

The database reader currently provides:

| Operation | Method |
|---|---|
| Establish database connection | `get_connection()` |
| Execute SQL queries | `execute_query()` |
| Initialize database table | `initialize_database()` |
| Insert test records | `insert_test_data()` |
| Retrieve all records | `get_all_test_data()` |
| Retrieve records by test case | `get_test_data_by_case()` |
| Update existing records | `update_test_data()` |
| Delete records | `delete_test_data()` |

### Database Testing

Database reader functionality is tested in:

`tests/test_database_reader.py`

The tests cover database connection, query execution, initialization, insertion, retrieval, updating, and deletion.

Execute the database tests using:

```bash
pytest tests/test_database_reader.py -v
```

### Database Test Fixture

A reusable Pytest fixture named `database` is defined in `conftest.py`.

It:

1. Creates an isolated temporary database for each test.
2. Initializes the database table.
3. Provides a `DatabaseReader` instance to the test.
4. Uses Pytest's temporary directory management to isolate test data.

Example:

```python
def test_insert_test_data(database):

    record_id = database.insert_test_data(
        "valid_login",
        "standard_user",
        "secret_sauce",
        "success"
    )

    assert record_id == 1
```

### Current Integration Scope

SQLite database connection and CRUD operations have been implemented and independently tested.

However, the existing login and checkout test modules currently use Excel-based test data. Database-driven execution of these UI test cases and Redis integration remain separate implementation tasks.

## 8. Execute BDD Tests Using Behave

BDD scenarios are written in Gherkin syntax and stored in the `features/` directory.

### Execute all BDD features

```bash
behave
```

### Execute an individual feature

Login:

```bash
behave features/login.feature
```

Inventory:

```bash
behave features/inventory.feature
```

Product Details:

```bash
behave features/product.feature
```

Shopping Cart:

```bash
behave features/cart.feature
```

Checkout:

```bash
behave features/checkout.feature
```

### Formatted execution output

```bash
behave features/checkout.feature --format=pretty
```

### Dry-run validation

To check whether step definitions match the steps in a feature without executing browser interactions:

```bash
behave --dry-run
```

For an individual feature:

```bash
behave --dry-run features/checkout.feature
```

**Note:** A dry run checks step matching but does not execute browser interactions or test assertions.

## 9. Cross-Browser Test Execution

The Pytest framework supports three browser options.

### Chromium

```powershell
$env:BROWSER = "chromium"
pytest -v
```

### Google Chrome

```powershell
$env:BROWSER = "chrome"
pytest -v
```

### Microsoft Edge

```powershell
$env:BROWSER = "edge"
pytest -v
```

The browser selection is read through the environment variable and applied by the configuration and browser management components.

## 10. Headless Execution

Headless execution runs browser tests without displaying the browser window.

To enable CI headless execution:

```powershell
$env:CI = "true"
pytest -v
```

The configuration reader detects `CI=true` and enables headless mode, as configured in the framework.

## 11. Continuous Integration Execution

The project uses GitHub Actions for automated testing.

Workflow file:

`.github/workflows/automation.yml`

According to the workflow configuration, execution is triggered when:

- Code is pushed to the `main` branch.
- A pull request targets the `main` branch.

The configured browser matrix includes:

1. Chromium
2. Google Chrome
3. Microsoft Edge

Each browser job runs the Pytest test suite independently.

To inspect workflow results:

1. Open the project repository on GitHub.
2. Select the **Actions** tab.
3. Open the relevant workflow execution.
4. Inspect the individual browser jobs.
5. Review the test execution results and logs.

## 12. Current Verified Results

The following results were obtained during local test execution.

### Pytest: Latest Full Suite Execution

| Metric | Result |
|---|---|
| Tests collected | 28 |
| Passed | 28 |
| Failed | 0 |
| Execution time | 34.61 seconds |

The passing tests include:

- Framework setup.
- Browser manager.
- Configuration validation.
- Base page functionality.
- Excel reader tests.
- Login scenarios.
- Inventory scenarios.
- Standard user checkout.

The one failing test is:

`test_checkout_with_excel_data[valid_checkout_problem_user]`

The failure occurs because the checkout information page does not retain the expected last-name value when using `problem_user`.

### Additional Checkout Verification

The standard user checkout scenario was independently executed:

```bash
pytest tests/test_checkout.py -v -s -k "valid_checkout and not problem_user"
```

Result:

| Metric | Result |
|---|---|
| Passed | 1 |
| Failed | 0 |
| Deselected | 1 |

The `problem_user` checkout scenario was also independently investigated. The application displayed the error:

`Error: Last Name is required`

This indicates that the expected checkout information was not successfully retained by the application.

### Previously Verified Behave Results

The following results were obtained from earlier independent local executions.

**Previously verified BDD suite**

| Metric | Result |
|---|---|
| Features passed | 3 |
| Scenarios passed | 16 |
| Steps passed | 65 |
| Failed features | 0 |
| Failed scenarios | 0 |
| Execution time | 16.643 seconds |

**Product Details Feature**

| Metric | Result |
|---|---|
| Features passed | 1 |
| Scenarios passed | 3 |
| Steps passed | 20 |
| Failed scenarios | 0 |
| Execution time | 4.658 seconds |

**Checkout Feature**

| Metric | Result |
|---|---|
| Features passed | 1 |
| Scenarios passed | 6 |
| Steps passed | 37 |
| Failed scenarios | 0 |
| Execution time | 9.635 seconds |

**Shopping Cart Feature**

| Metric | Result |
|---|---|
| Features passed | 1 |
| Scenarios passed | 5 |
| Steps passed | 29 |
| Failed scenarios | 0 |
| Execution time | 6.034 seconds |

These are historical individual executions. They must not be combined into a single aggregate result because the complete updated BDD suite has not yet been re-executed.

GitHub Actions results should be reported separately after verifying the corresponding workflow runs.

## 13. Understanding Test Results

### Pytest

| Result | Meaning |
|---|---|
| PASSED | Test executed successfully |
| FAILED | Test executed but an assertion or operation failed |
| ERROR | An error occurred during test setup or execution |
| SKIPPED | Test was intentionally not executed |

### Behave

| Result | Meaning |
|---|---|
| passed | Feature, scenario, or step executed successfully |
| failed | An assertion or step execution failed |
| skipped | Step was skipped |
| undefined | No matching step definition was found |
| untested | Step was not executed, for example during a dry run |

## 14. Troubleshooting

### No Pytest tests are collected

Check the test naming conventions and `pytest.ini` configuration.

Standard discovery conventions include:

- Files named `test_*.py`.
- Functions named `test_*`.
- Tests located in the configured test directory.

### Browser launch failure

Install the required Playwright browsers:

```bash
python -m playwright install
```

### Incorrect browser selection

Verify the environment variable:

```powershell
$env:BROWSER
```

Supported values:

- `chromium`
- `chrome`
- `edge`

### Behave command is not recognized

Ensure the virtual environment is activated and install the project dependencies:

```bash
pip install -r requirements.txt
```

### Undefined Behave steps

Check that:

- The feature file is located in `features/`.
- Its step definitions are located in `features/steps/`.
- The wording of each Gherkin step matches its corresponding step definition.

### Ambiguous Behave steps

Check whether the same step definition has been declared in multiple step-definition files.

Remove duplicate definitions or reuse the existing shared definition.

### Excel workbook not found

Verify that:

`test_data/test_data.xlsx`

exists at the expected location.

### Excel worksheet not found

Check the exact worksheet names:

- `LoginData`
- `CheckoutData`

### Excel reader validation failures

Check that:

- Headers are present in the first row.
- Headers are not duplicated.
- Required column names match the test modules.

### Tests fail due to application loading or timeouts

Check the SauceDemo URL and timeout settings in `config/config.yaml`.

## 15. Current Limitations

The following capabilities are not currently part of the verified implementation:

- Allure report generation.
- Automatic screenshot capture on test failure.
- Redis-based test data integration.
- Database-driven test execution for existing login and checkout scenarios.
- Excel-based data integration for Behave scenarios.

### Implemented Data Source Capabilities

The following capabilities have been implemented:

- Excel-based test data reading using OpenPyXL.
- SQLite database connection and initialization.
- SQLite test data insertion, retrieval, updating, and deletion.
- Reusable database reader implementation.
- Pytest database fixture for isolated database testing.

### Known Application Limitation

**SauceDemo – problem_user Checkout Behavior**

During checkout testing, the `problem_user` account exhibited unexpected behavior on the checkout information page.

Observations:

- Login completed successfully.
- Product addition and cart navigation worked successfully.
- The checkout information page was displayed.
- The first-name field contained an unexpected value.
- The last-name field remained empty despite the automation attempting to populate it.
- The application displayed `Error: Last Name is required`.

The same checkout scenario completed successfully using `standard_user`.

**Conclusion:** The observed behavior indicates an application-side UI interaction issue associated with the `problem_user` account. The test retains its assertions to detect this behavior rather than treating unsuccessful checkout as a successful order.

This limitation was observed during testing and should be revalidated if the application changes.