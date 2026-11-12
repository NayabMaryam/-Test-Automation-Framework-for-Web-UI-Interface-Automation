# Test Execution Guide

## 1. Introduction

This document explains how to execute and verify automated UI tests using the Python Playwright and Pytest framework.

The application under test is SauceDemo:

https://www.saucedemo.com/

## 2. Test Framework

The framework uses:

- **Pytest:** Test discovery, execution, and fixtures.
- **Playwright:** Browser automation.
- **Page Object Model:** Separation of page interactions from test logic.
- **YAML:** Centralized configuration.

## 3. Test Directory

Automated test cases are located in the `tests/` directory.

The current test suite covers:

- Framework setup.
- Configuration validation.
- Browser management.
- Base page functionality.
- Login page functionality.
- Login scenarios.
- Inventory page functionality.
- Inventory scenarios.
- Checkout and search-related test modules.

## 4. Execute All Tests

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

## 5. Execute Individual Test Files

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

## 6. Cross-Browser Test Execution

The framework supports three browser options.

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

## 7. Headless Execution

Headless execution runs browser tests without displaying the browser window.

To enable CI headless execution:

```powershell
$env:CI = "true"
pytest -v
```

The configuration reader detects `CI=true` and enables headless mode.

## 8. Continuous Integration Execution

The project uses GitHub Actions for automated cross-browser testing.

Workflow file:

`.github/workflows/automation.yml`

The workflow executes when:

- Code is pushed to the `main` branch.
- A pull request targets the `main` branch.

The browser matrix includes:

1. Chromium
2. Google Chrome
3. Microsoft Edge

Each browser runs the Pytest test suite independently.

To inspect results:

1. Open the project repository on GitHub.
2. Select the **Actions** tab.
3. Open the latest workflow execution.
4. Inspect the individual browser jobs.
5. Review the test execution results.

## 9. Current Verified Results

The current implementation has achieved:

| Execution Environment | Result |
|---|---|
| Local test execution | 13 tests passed |
| GitHub Actions — Chromium | Passed |
| GitHub Actions — Chrome | Passed |
| GitHub Actions — Edge | Passed |

These results represent the verified test suite at the time this documentation was prepared.

## 10. Understanding Test Results

Pytest displays the following common result indicators:

| Result | Meaning |
|---|---|
| PASSED | Test executed successfully |
| FAILED | Test executed but an assertion or operation failed |
| ERROR | An error occurred during test setup or execution |
| SKIPPED | Test was intentionally not executed |

## 11. Troubleshooting

**No tests are collected**

Check the test naming conventions and `pytest.ini` configuration.

The current configuration discovers:

- Files named `test_*.py`.
- Functions named `test_*`.
- Tests inside the `tests/` directory.

**Browser launch failure**

Install the required Playwright browsers:

```bash
python -m playwright install
```

**Incorrect browser selection**

Verify the environment variable:

```powershell
$env:BROWSER
```

Supported values:

- `chromium`
- `chrome`
- `edge`

**Tests fail due to application loading or timeouts**

Check the SauceDemo URL and the timeout settings in `config/config.yaml`.

## 12. Current Limitations

The current verified implementation does not include:

- Allure report generation.
- Automatic screenshot capture on test failure.
- BDD/Gherkin test execution.
- Excel, database, or Redis test data integration.

These capabilities should not be considered part of the current test execution process until implemented and verified.
