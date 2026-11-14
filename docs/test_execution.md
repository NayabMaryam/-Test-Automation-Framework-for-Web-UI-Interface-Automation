# Test Execution Guide

## 1. Introduction

This document explains how to execute and verify automated UI tests using the Python Playwright, Pytest, and Behave frameworks.

The application under test is SauceDemo:

https://www.saucedemo.com/

The framework supports two testing approaches:

- **Pytest:** Conventional automated UI tests.
- **Behave:** BDD testing using Gherkin feature files and step definitions.

## 2. Test Framework

The framework uses:

- **Pytest:** Test discovery, execution, and fixtures.
- **Playwright:** Browser automation.
- **Behave:** BDD test execution using Gherkin.
- **Page Object Model:** Separation of page interactions from test logic.
- **YAML:** Centralized configuration.

## 3. Test Directory

Automated Pytest test cases are located in the `tests/` directory.

The current Pytest suite covers:

- Framework setup.
- Configuration validation.
- Browser management.
- Base page functionality.
- Login page functionality and login scenarios.
- Inventory page functionality and product listing.

BDD feature files and their step definitions are located in the `features/` directory.

The current BDD implementation covers:

- **Login:** Valid and invalid login scenarios.
- **Inventory:** Product listing, product count, product names, and sorting.
- **Product Details:** Individual product information, product selection, and cart interactions from the product details page.
- **Shopping Cart:** Cart contents, product removal, and cart badge validation.
- **Checkout:** Checkout information validation, checkout overview, price calculations, order completion, and empty-cart checkout behavior.

## 4. Execute All Pytest Tests

Activate the virtual environment and execute:

```bash
pytest -v
```

The `-v` option displays individual test names and their execution results.

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
```

## 6. Execute BDD Tests Using Behave

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

To execute a feature with formatted output:

```bash
behave features/checkout.feature --format=pretty
```

### Dry-run validation

To check whether step definitions match the steps in a feature without executing the scenarios:

```bash
behave --dry-run
```

For an individual feature:

```bash
behave --dry-run features/checkout.feature
```

**Note:** A dry run checks step matching but does not execute the actual browser interactions or test assertions.

## 7. Cross-Browser Test Execution

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

## 8. Headless Execution

Headless execution runs browser tests without displaying the browser window.

To enable CI headless execution:

```powershell
$env:CI = "true"
pytest -v
```

The configuration reader detects `CI=true` and enables headless mode, as configured in the framework.

## 9. Continuous Integration Execution

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

## 10. Current Verified Results

The following results were obtained during local test execution.

### Pytest

| Metric | Result |
|---|---|
| Tests collected | 12 |
| Passed | 12 |
| Failed | 0 |
| Execution time | 23.49 seconds |

### Previously Verified Behave Suite

| Metric | Result |
|---|---|
| Features passed | 3 |
| Scenarios passed | 16 |
| Steps passed | 65 |
| Failed features | 0 |
| Failed scenarios | 0 |
| Execution time | 16.643 seconds |

### Independently Verified BDD Features

The following additional features were independently executed after the previously recorded BDD results.

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

Previously verified independent execution:

| Metric | Result |
|---|---|
| Features passed | 1 |
| Scenarios passed | 5 |
| Steps passed | 29 |
| Failed scenarios | 0 |
| Execution time | 6.034 seconds |

These results represent individual and previously recorded local executions. They should not be combined into a single aggregate result because the complete updated BDD suite has not yet been re-executed.

GitHub Actions results should be reported separately after verifying the corresponding workflow runs.

## 11. Understanding Test Results

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

## 12. Troubleshooting

### No Pytest tests are collected

Check the test naming conventions and `pytest.ini` configuration.

The standard discovery conventions include:

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

### Tests fail due to application loading or timeouts

Check the SauceDemo URL and the timeout settings in `config/config.yaml`.

## 13. Current Limitations

The following capabilities are not yet part of the verified implementation:

- Allure report generation.
- Automatic screenshot capture on test failure.
- Excel-based test data integration.
- Database-based test data integration.
- Redis integration.

These capabilities should not be considered part of the current test execution process until implemented and verified.