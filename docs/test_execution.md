# Test Execution Guide

## 1. Introduction

This document explains how to execute and verify automated UI tests using Python, Playwright, Pytest, and Behave.

The application under test is SauceDemo:

https://www.saucedemo.com/

The framework supports two testing approaches:

- **Pytest:** Conventional automated UI testing using fixtures, parameterization, and external test data.
- **Behave:** Behavior-Driven Development (BDD) testing using Gherkin feature files and step definitions.

The framework also supports multiple test data sources, including Excel, SQLite, and Redis.

Additionally, the framework integrates Allure for interactive test reporting, failure diagnostics, and report generation. Allure reports are generated locally and through GitHub Actions.

## 2. Test Framework

The framework uses:

- **Pytest:** Test discovery, execution, parameterization, and fixtures.
- **Playwright:** Browser automation.
- **Behave:** BDD testing using Gherkin.
- **Page Object Model:** Separation of page interactions from test logic.
- **YAML:** Centralized configuration.
- **OpenPyXL:** Excel-based test data reading.
- **SQLite:** Database-based test data storage and management.
- **Redis:** In-memory test data storage and retrieval.
- **redis-py:** Python client for Redis.
- **sqlite3:** Python's built-in SQLite database interface.
- **Allure:** Test reporting and failure diagnostics.
- **GitHub Actions:** Continuous Integration and automated cross-browser testing.

## 3. Test Directory

Automated Pytest test cases are located in the `tests/` directory.

The current Pytest suite covers:

- Framework setup.
- Configuration validation.
- Browser management.
- Base page functionality.
- Excel reader functionality and validation.
- SQLite database reader functionality.
- Redis reader functionality.
- Login functionality using Excel and Redis test data.
- Inventory page functionality and product listing.
- Checkout scenarios using Excel and Redis test data.

BDD feature files and their step definitions are located in the `features/` directory.

The BDD implementation covers:

- **Login:** Valid and invalid login scenarios.
- **Inventory:** Product listing, product count, product names, and sorting.
- **Product Details:** Individual product information, product selection, and cart interactions.
- **Shopping Cart:** Cart contents, product removal, and cart badge validation.
- **Checkout:** Checkout information validation, checkout overview, price calculations, order completion, and empty-cart checkout behavior.

## 4. Execute All Pytest Tests

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Execute the complete test suite:

```bash
pytest -v
```

The `-v` option displays individual test names and execution results.

For more detailed output:

```bash
pytest -v -s
```

The `-s` option displays print statements during execution, including Redis seeding messages.

**Allure Integration:** The Pytest configuration automatically generates raw Allure results in the `allure-results/` directory whenever the test suite is executed.

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
pytest tests/test_database_reader.py -v
pytest tests/test_redis_reader.py -v
pytest tests/test_login_redis.py -v
pytest tests/test_checkout_redis.py -v
```

Individual Pytest executions also generate Allure results.

## 6. Excel-Based Test Execution

The framework uses OpenPyXL to read external test data from:

`test_data/test_data.xlsx`

The reusable Excel reader is implemented in:

`src/data/excel_reader.py`

The reader retrieves worksheet records as dictionaries using the first row as column headers.

### Login Tests

The `LoginData` worksheet supplies login test records to:

`tests/test_login.py`

Execute:

```bash
pytest tests/test_login.py -v
```

### Checkout Tests

The `CheckoutData` worksheet supplies checkout test records to:

`tests/test_checkout.py`

Execute:

```bash
pytest tests/test_checkout.py -v
```

### Excel Reader Validation

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

### Important Distinction

Excel-based test data integration is implemented in the Pytest login and checkout modules.

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

### Database Initialization

The `DatabaseReader` provides an initialization mechanism that creates the `test_data` table if it does not already exist.

The table stores:

- `id`: Unique record identifier.
- `test_case`: Test case identifier.
- `username`: Login username.
- `password`: Login password.
- `expected`: Expected test outcome.

### Supported Database Operations

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

Execute:

```bash
pytest tests/test_database_reader.py -v
```

### Database Test Fixture

A reusable Pytest fixture named `database` is defined in `tests/conftest.py`.

It:

1. Creates an isolated temporary database for each test.
2. Initializes the database table.
3. Provides a `DatabaseReader` instance.
4. Uses Pytest temporary directory management to isolate test data.

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

SQLite connection management and CRUD operations have been implemented and independently tested.

The existing login and checkout UI tests use Excel and Redis as their respective test data sources. Database-driven execution of these UI test cases has not been implemented.

## 8. Redis Integration

The framework supports Redis-based test data storage and retrieval using the Python Redis client.

Redis is used as an additional external test data source for login and checkout automation.

### Redis Configuration

Redis configuration is maintained in:

`config/config.yaml`

Example:

```yaml
redis:
  host: "localhost"
  port: 6379
  db: 0
```

The framework uses the following settings:

| Setting | Description |
|---|---|
| `host` | Redis server hostname |
| `port` | Redis server port |
| `db` | Redis database index |

### Redis Server Requirement

A running Redis server is required before executing Redis integration tests.

For local execution, Redis must be accessible at the configured host and port.

The default configuration uses:

- Host: `localhost`
- Port: `6379`
- Database: `0`

### Redis Environment Variables

The configuration reader supports environment variable overrides:

| Environment Variable | Purpose |
|---|---|
| `REDIS_HOST` | Overrides Redis hostname |
| `REDIS_PORT` | Overrides Redis port |
| `REDIS_DB` | Overrides Redis database index |

Example PowerShell configuration:

```powershell
$env:REDIS_HOST = "localhost"
$env:REDIS_PORT = "6379"
$env:REDIS_DB = "0"
```

To verify the configured values:

```powershell
$env:REDIS_HOST
$env:REDIS_PORT
$env:REDIS_DB
```

### Redis Reader

The reusable Redis reader is implemented in:

`src/data/redis_reader.py`

It provides:

- Redis connection management.
- Connection reuse.
- Connection closing.
- Reconnection after closing.
- Data storage and retrieval.
- Data deletion.
- Structured test data storage and retrieval.
- Retrieving all test data.
- Handling nonexistent keys.

### Redis Key Structure

The framework uses separate Redis keys for login and checkout scenarios.

| Test Data | Redis Key |
|---|---|
| Standard user login | `login_standard_user` |
| Locked-out user login | `login_locked_out_user` |
| Invalid user login | `login_invalid_user` |
| Problem user login | `login_problem_user` |
| Standard checkout | `checkout_valid_checkout` |
| Problem user checkout | `checkout_valid_checkout_problem_user` |

### Automatic Redis Test Data Seeding

Redis test data is automatically populated through a session-scoped Pytest fixture:

`seed_redis_test_data`

The fixture is defined in:

`tests/conftest.py`

It performs the following operations:

1. Reads login records from the `LoginData` worksheet in `test_data/test_data.xlsx`.
2. Stores login records in Redis using the `login_<username>` key structure.
3. Reads checkout records from the `CheckoutData` worksheet.
4. Stores checkout records using the `checkout_<test_case>` key structure.
5. Keeps track of the keys created by the fixture.
6. Deletes only those seeded keys after the test session finishes.
7. Closes its Redis connection.

The fixture is session-scoped, meaning that test data is seeded once per Pytest session rather than before every individual test.

The Redis login and checkout test modules explicitly request this fixture.

**Important:** Redis test data does not need to be manually inserted before running the complete Pytest suite. However, the Redis server must be running and accessible.

### Redis-Based Login Tests

The Redis login tests are implemented in:

`tests/test_login_redis.py`

Execute:

```bash
pytest tests/test_login_redis.py -v -s
```

The tests retrieve login records from Redis and execute the corresponding login scenarios.

### Redis-Based Checkout Tests

The Redis checkout tests are implemented in:

`tests/test_checkout_redis.py`

Execute:

```bash
pytest tests/test_checkout_redis.py -v -s
```

The tests retrieve checkout records from Redis and execute the checkout workflow.

The `problem_user` scenario also verifies the previously observed checkout form defect.

### Redis Reader Tests

Redis reader functionality is independently tested in:

`tests/test_redis_reader.py`

Execute:

```bash
pytest tests/test_redis_reader.py -v
```

The tests validate connection handling, data storage, retrieval, deletion, and structured test data operations.

### Redis Test Data Cleanup

The `seed_redis_test_data` fixture uses a `finally` block to clean up the keys created during the test session.

This prevents the fixture's test records from remaining in Redis after a normal test-session teardown.

Only keys recorded by the fixture are deleted.

### Redis Troubleshooting

**Redis connection refused**

Verify that the Redis server is running and accessible at the configured host and port.

**Redis test data not found**

If the tests report:

```text
Redis test data not found for standard_user
```

or:

```text
Redis checkout data not found for valid_checkout
```

Check the following:

1. Verify that the Redis server is running.
2. Verify the Redis configuration in `config/config.yaml`.
3. Ensure the Redis test modules request `seed_redis_test_data` in their function parameters.
4. Ensure `test_data/test_data.xlsx` exists.
5. Verify that the `LoginData` and `CheckoutData` worksheets exist.
6. Run the tests using Pytest so that the fixture executes.

For detailed output, execute:

```bash
pytest tests/test_login_redis.py tests/test_checkout_redis.py -v -s
```

Expected seeding messages include:

```text
Seeded Redis: login_standard_user
Seeded Redis: login_locked_out_user
Seeded Redis: login_invalid_user
Seeded Redis: login_problem_user
Seeded Redis: checkout_valid_checkout
Seeded Redis: checkout_valid_checkout_problem_user
```

**Redis CLI is not recognized**

The `redis-cli` command is not included with the Python virtual environment.

Its availability depends on the Redis installation and whether the Redis command-line tools are included in the system PATH.

The framework itself communicates with Redis through the Python Redis client, so `redis-cli` is not required to execute the Pytest integration tests.

## 9. Execute BDD Tests Using Behave

BDD scenarios are written in Gherkin syntax and stored in the `features/` directory.

### Execute All BDD Features

```bash
behave
```

### Execute an Individual Feature

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

### Formatted Execution Output

```bash
behave features/checkout.feature --format=pretty
```

### Dry-Run Validation

To check whether step definitions match the steps in a feature without executing browser interactions:

```bash
behave --dry-run
```

For an individual feature:

```bash
behave --dry-run features/checkout.feature
```

**Note:** A dry run checks step matching but does not execute browser interactions or test assertions.

## 10. Cross-Browser Test Execution

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

Each execution generates Allure results in the configured `allure-results/` directory.

For independent reports, clear the previous results before switching browsers and executing another test run.

## 11. Headless Execution

Headless execution runs browser tests without displaying the browser window.

To enable CI headless execution:

```powershell
$env:CI = "true"
pytest -v
```

The configuration reader detects `CI=true` and enables headless mode.

## 12. Allure Test Reporting

The framework integrates Allure with Pytest to generate interactive HTML reports containing test execution information and failure diagnostics.

Allure reporting is supported both locally and through GitHub Actions.

### Technologies Used

| Technology | Purpose |
|---|---|
| `allure-pytest` | Pytest integration for Allure |
| Allure Commandline | HTML report generation and viewing |
| `allure` npm package | Local Allure CLI dependency |
| GitHub Actions | Automated report generation and artifact storage |

### Installation

The Python integration is included in `requirements.txt`.

The Allure CLI is managed through the project's `package.json` and `package-lock.json`.

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install Node.js dependencies:

```bash
npm install
```

Verify the Allure CLI:

```bash
npx allure --version
```

Verify the Python integration:

```bash
pip show allure-pytest
```

### Pytest Configuration

Allure result generation is configured in `pytest.ini`:

```ini
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = --alluredir=allure-results
```

The `--alluredir=allure-results` option instructs the Allure Pytest plugin to save test execution results in the `allure-results/` directory.

Consequently, running the normal Pytest command automatically produces Allure result files.

### Generating Allure Results

Execute the test suite:

```bash
pytest -v
```

The generated results are stored in:

```text
allure-results/
```

This directory contains:

- Test result JSON files.
- Fixture and step container JSON files.
- Generated attachments.
- Additional Allure execution metadata where available.

**Important:** Allure appends new result files to an existing results directory. Previous results may therefore appear in subsequent reports if the directory is not cleared.

For an independent report of a fresh execution, clear the previous results first.

Windows CMD:

```cmd
if exist allure-results rmdir /s /q allure-results
```

Then execute:

```bash
pytest -v
```

The configured Pytest option automatically recreates the results directory.

### Generating the HTML Report

After the tests finish, generate the HTML report:

```bash
npx allure generate allure-results --clean -o allure-report
```

This command:

- Reads the raw test results from `allure-results/`.
- Generates the interactive HTML report.
- Removes the previous generated report before creating a new one.
- Stores the generated report in `allure-report/`.

### Viewing the Report

To open the generated report:

```bash
npx allure open allure-report
```

Allure starts a local server and opens the report in the default browser.

### Failure Screenshots and Browser Logs

The framework implements automatic failure reporting through a Pytest hook in:

`tests/conftest.py`

When a test fails during its execution phase, the reporting hook attempts to capture and attach the following information:

| Attachment | Description |
|---|---|
| Failure Screenshot | Full-page screenshot of the browser |
| Browser Page Details | Current page URL and title |
| Browser Console Logs | Captured browser console messages and JavaScript errors |
| Test Failure Details | Pytest failure traceback and assertion information |

These attachments help identify UI failures, JavaScript errors, and unexpected browser behavior.

Screenshot and page-detail capture are attempted only when the page fixture is available and the page is still open.

The framework also handles screenshot capture errors by attaching the corresponding error information when possible.

**Note:** The current implementation captures screenshots for failures during the test call phase. It does not automatically capture screenshots for every setup or teardown failure.

### Downloading and Sharing the HTML Report

The generated HTML report can be packaged and shared independently of the development environment.

To create a ZIP archive in Windows CMD:

```cmd
powershell -Command "Compress-Archive -Path allure-report -DestinationPath Allure-Example-Report.zip -Force"
```

The resulting file is:

```text
Allure-Example-Report.zip
```

The recipient can:

1. Download the ZIP archive.
2. Extract its contents.
3. Open a terminal inside the extracted `allure-report` directory.
4. Execute:

```bash
python -m http.server 8000
```

5. Open the following address in a browser:

```text
http://localhost:8000
```

The complete generated HTML report can then be viewed locally without installing the Allure CLI or rerunning the test suite.

### Generated Files and Version Control

The following directories contain generated runtime artifacts:

| Directory | Purpose |
|---|---|
| `allure-results/` | Raw test execution results and attachments |
| `allure-report/` | Generated HTML report |

These directories are excluded from Git version control through `.gitignore`.

The `package.json` and `package-lock.json` files are maintained in the repository to preserve the Allure CLI dependency configuration.

The example report ZIP can be included separately with the project submission.

## 13. Continuous Integration Execution

The project uses GitHub Actions for automated testing.

Workflow file:

`.github/workflows/automation.yml`

The workflow includes:

- Automated execution on configured pushes.
- Pull request execution targeting `main`.
- A Redis 7 service container.
- Redis health checks.
- Python 3.12 setup.
- Playwright browser installation.
- Environment variable configuration for Redis.
- Pytest execution across the configured browser matrix.
- Allure report generation and artifact upload.

### Redis in GitHub Actions

GitHub Actions starts a Redis 7 service container for the test job.

The Redis service is exposed through port `6379`.

The workflow configures:

```yaml
REDIS_HOST: localhost
REDIS_PORT: 6379
REDIS_DB: 0
```

The Pytest fixture automatically seeds the required Redis records from the Excel workbook during test execution.

### Inspecting Workflow Results

1. Open the project repository on GitHub.
2. Select the **Actions** tab.
3. Open the relevant workflow execution.
4. Inspect the individual browser jobs.
5. Review the test execution results and logs.

Local test results and GitHub Actions results should be reported separately.

### Downloading Allure Reports from GitHub Actions

The CI workflow generates browser-specific Allure reports and uploads them as GitHub Actions artifacts.

The following artifacts are produced for the configured browser matrix:

| Artifact | Description |
|---|---|
| `allure-report-chromium` | Generated HTML report for Chromium |
| `allure-report-chrome` | Generated HTML report for Google Chrome |
| `allure-report-edge` | Generated HTML report for Microsoft Edge |
| `allure-results-chromium` | Raw Allure results for Chromium |
| `allure-results-chrome` | Raw Allure results for Google Chrome |
| `allure-results-edge` | Raw Allure results for Microsoft Edge |

To download a report:

1. Open the relevant GitHub Actions workflow run.
2. Scroll to the **Artifacts** section.
3. Select the desired browser-specific `allure-report` artifact.
4. Download and extract the ZIP file.
5. Open a terminal inside the extracted `allure-report` directory.
6. Start a local HTTP server:

```bash
python -m http.server 8000
```

7. Open the following address in a browser:

```text
http://localhost:8000
```

The generated Allure dashboard displays the test execution results, test details, and available attachments.

The raw `allure-results` artifacts can also be downloaded for report regeneration or further analysis.

### Redis in GitHub Actions

The Redis service runs as a container during the CI test job.

The workflow exposes port `6379` and provides the Redis connection settings through environment variables.

The `seed_redis_test_data` fixture automatically populates Redis when the Redis-backed tests execute.

A separate Redis seeding script is therefore not required when the fixture is correctly included in the test modules.

## 14. Understanding Test Results

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

### Allure

Allure presents test execution information through an interactive dashboard.

The report provides:

- Overall test execution statistics.
- Passed, failed, broken, and skipped test information.
- Individual test case details.
- Execution duration.
- Failure messages and tracebacks.
- Available screenshots and other attachments.
- Test grouping and metadata where configured.

## 15. Current Verified Results

### Latest Successful Local Pytest Execution

The latest reported successful local execution completed with:

| Metric | Result |
|---|---:|
| Tests collected | 50 |
| Passed | 50 |
| Failed | 0 |
| Execution time | 67.76 seconds |

The execution also generated Allure result files successfully.

### Allure Reporting Verification

The following reporting operations have been successfully verified locally:

| Operation | Status |
|---|---|
| Allure Pytest plugin installation | Verified |
| Allure plugin loading | Verified |
| Raw result generation | Verified |
| HTML report generation | Verified |
| Local report viewing | Verified |
| Report ZIP creation | Verified |
| Viewing an extracted report through a local HTTP server | Verified |
| Failure screenshot and diagnostic attachment implementation | Implemented |

### GitHub Actions Allure Integration

Allure reporting has also been integrated into the GitHub Actions workflow.

The workflow produces browser-specific report and raw result artifacts for:

- Chromium
- Google Chrome
- Microsoft Edge

The generated artifacts can be downloaded from the corresponding workflow execution.

The reported successful CI execution produced the following six artifacts:

- `allure-report-chromium`
- `allure-report-chrome`
- `allure-report-edge`
- `allure-results-chromium`
- `allure-results-chrome`
- `allure-results-edge`

The individual browser jobs should be evaluated separately rather than combining their results with local execution statistics.

### Important: Keeping Test Results Current

The results above represent specific successful executions.

Before reporting final project results, execute the complete test suite again and verify the latest GitHub Actions run.

## 16. Troubleshooting

### No Pytest Tests Are Collected

Check the test naming conventions and `pytest.ini` configuration.

Standard discovery conventions include:

- Files named `test_*.py`.
- Functions named `test_*`.
- Tests located in the configured test directory.

### Browser Launch Failure

Install the required Playwright browsers:

```bash
python -m playwright install
```

### Incorrect Browser Selection

Verify the environment variable:

```powershell
$env:BROWSER
```

Supported values:

- `chromium`
- `chrome`
- `edge`

### Behave Command Is Not Recognized

Ensure the virtual environment is activated and install the project dependencies:

```bash
pip install -r requirements.txt
```

### Undefined Behave Steps

Check that:

- The feature file is located in `features/`.
- Its step definitions are located in `features/steps/`.
- The wording of each Gherkin step matches its corresponding step definition.

### Ambiguous Behave Steps

Check whether the same step definition has been declared in multiple step-definition files.

Remove duplicate definitions or reuse the existing shared definition.

### Excel Workbook Not Found

Verify that:

`test_data/test_data.xlsx`

exists at the expected location.

### Excel Worksheet Not Found

Check the exact worksheet names:

- `LoginData`
- `CheckoutData`

### Excel Reader Validation Failures

Check that:

- Headers are present in the first row.
- Headers are not duplicated.
- Required column names match the test modules.

### Redis Connection Failure

Check the Redis server status and configuration.

Verify:

- Redis hostname.
- Redis port.
- Redis database index.
- Redis service availability.

### Redis Test Data Missing

Check that the Redis login and checkout test functions include the `seed_redis_test_data` fixture dependency.

Execute:

```bash
pytest tests/test_login_redis.py tests/test_checkout_redis.py -v -s
```

### Tests Fail Due to Application Loading or Timeouts

Check the SauceDemo URL and timeout settings in `config/config.yaml`.

### Allure Results Directory Not Generated

Verify that:

- `allure-pytest` is installed.
- The Allure Pytest plugin is loaded.
- `pytest.ini` contains `addopts = --alluredir=allure-results`.

Verify the plugin installation:

```bash
pip show allure-pytest
```

### Allure Command Not Working

Verify that Node.js and npm are installed.

Install the project dependencies:

```bash
npm install
```

Check the Allure CLI:

```bash
npx allure --version
```

### Report Does Not Display the Latest Test Results

Clear the existing results directory before executing the tests again.

Windows CMD:

```cmd
if exist allure-results rmdir /s /q allure-results
```

Then regenerate the report:

```bash
pytest -v
npx allure generate allure-results --clean -o allure-report
```

### Allure Report Does Not Open

Generate the report again:

```bash
npx allure generate allure-results --clean -o allure-report
```

Then open it:

```bash
npx allure open allure-report
```

Alternatively, serve the extracted report directory using:

```bash
python -m http.server 8000
```

### Failure Screenshot Is Missing

Verify that:

- The test failed during the execution phase.
- The test uses the `page` fixture.
- The page is still open when the failure hook executes.
- The screenshot attachment was successfully generated.

The current implementation captures screenshots for test-call failures, not every possible setup or teardown failure.

## 17. Current Limitations

The following capabilities are not currently part of the verified implementation:

- Database-driven execution of existing login and checkout UI tests.
- Excel-based test data integration for Behave scenarios.
- Redis-based test data integration for Behave scenarios.

### Implemented Reporting Capabilities

The following reporting capabilities have been implemented:

- Allure integration with Pytest.
- Automatic raw result generation.
- Interactive HTML report generation.
- Local report viewing.
- Failure screenshot capture.
- Browser console log collection.
- JavaScript error collection.
- Browser URL and page title attachments.
- Pytest failure detail attachments.
- Browser-specific Allure report generation in GitHub Actions.
- GitHub Actions artifact upload and download.
- Packaging and sharing generated HTML reports.

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

This limitation should be revalidated if the application changes.