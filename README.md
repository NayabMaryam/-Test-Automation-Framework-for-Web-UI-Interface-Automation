# UI Test Automation Framework

## 1. Project Overview

The UI Test Automation Framework is a Python-based web UI testing solution developed using Playwright, Pytest, and Behave.

The framework automates testing of the [SauceDemo](https://www.saucedemo.com/) web application.

It follows the Page Object Model (POM) design pattern to improve code reusability, maintainability, and separation of test logic from browser interactions.

The framework supports conventional automated testing using Pytest and Behavior-Driven Development (BDD) using Behave and Gherkin.

It also provides centralized configuration management, external test data integration, database operations, Redis-based test data management, cross-browser execution through GitHub Actions, and Allure test reporting.

## 2. Implemented Features

### Core Framework

- Browser management using Playwright.
- Support for Chromium, Google Chrome, and Microsoft Edge.
- Centralized YAML-based configuration.
- Environment variable overrides for browser selection, Redis connection settings, and CI execution.
- Configuration validation.
- Reusable Pytest fixtures for configuration, browser, page, database, and Redis management.
- Page Object Model (POM).

### UI Automation

- Login automation.
- Inventory page validation.
- Product details and product selection.
- Shopping cart operations.
- Checkout information and order completion.
- Data-driven UI test execution.

### Test Data Integration

**Excel Integration**

- Excel-based test data reading using OpenPyXL.
- Separate Excel worksheets for login and checkout scenarios.
- Parameterized tests using external test data.

**SQLite Integration**

- SQLite database connectivity.
- Database initialization and table creation.
- Test data insertion, retrieval, updating, and deletion.

**Redis Integration**

- Redis connectivity using the Python Redis client.
- Centralized Redis connection configuration.
- Environment variable overrides for Redis host, port, and database.
- Storage and retrieval of structured test data.
- Separate Redis keys for login and checkout test scenarios.
- Redis-backed login and checkout automation.
- Session-scoped Pytest fixture for automatic test data seeding.
- Automatic cleanup of keys seeded by the fixture.
- Redis connection reuse and reconnection handling.
- Redis reader unit and integration tests.

### BDD Testing

- Gherkin-based feature files.
- Behave step definitions.
- Login, inventory, product, shopping cart, and checkout scenarios.
- Browser lifecycle management through Behave environment hooks.

### Allure Test Reporting

- Allure reporting integration with Pytest using `allure-pytest`.
- Test execution results generated in the `allure-results/` directory.
- Test metadata and descriptions, including epic, feature, story, severity, and tags, for the annotated login tests.
- Dynamic test titles for data-driven login scenarios.
- Test steps displayed in the Allure report.
- Failure diagnostics attached to failed test executions, including:
  - Full-page screenshots.
  - Current page URL and title.
  - Browser console logs.
  - Test failure details.
- HTML report generation using the Allure 3 command-line interface.
- Local report viewing through the Allure CLI.
- GitHub Actions integration for generating and uploading browser-specific Allure reports and raw results.

Allure result and report directories are generated during execution and are excluded from Git using `.gitignore`.

### Continuous Integration

- GitHub Actions workflow integration.
- Automated test execution on configured pushes and pull requests targeting the main branch.
- Browser matrix configuration for cross-browser testing.
- Redis service container for CI execution.
- Environment-based configuration for Redis and browser selection.
- Allure report generation after test execution.
- Separate downloadable Allure report and result artifacts for Chromium, Chrome, and Edge.

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
| Redis | In-memory test data storage |
| redis-py | Python Redis client |
| PyYAML | YAML configuration handling |
| Allure Pytest | Pytest reporting integration |
| Allure 3 | HTML report generation |
| Node.js and npm | Allure CLI dependency management |
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
│   │   ├── database_reader.py
│   │   └── redis_reader.py
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
│   ├── test_redis_reader.py
│   ├── test_login.py
│   ├── test_login_redis.py
│   ├── test_inventory.py
│   ├── test_checkout.py
│   ├── test_checkout_redis.py
│   └── conftest.py
│
├── features/
│   ├── steps/
│   ├── login.feature
│   ├── inventory.feature
│   ├── product.feature
│   ├── cart.feature
│   └── checkout.feature
│
├── scripts/
│   └── load_redis_data.py
│
├── package.json
├── package-lock.json
├── pytest.ini
├── requirements.txt
└── README.md
```

The structure represents the main framework components. Additional supporting files may exist within individual directories.

The `allure-results/` and `allure-report/` directories are generated during test execution and report generation. They are excluded from version control.

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

Examples using PowerShell:

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

GitHub Actions uses a browser matrix to execute the automated test suite across the supported browser options.

## 7. Test Execution

### Environment Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Install Python dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
python -m playwright install
```

### Execute All Pytest Tests

```bash
pytest -v
```

### Execute Individual Test Modules

```bash
pytest tests/test_login.py -v
pytest tests/test_inventory.py -v
pytest tests/test_checkout.py -v
pytest tests/test_excel_reader.py -v
pytest tests/test_database_reader.py -v
pytest tests/test_redis_reader.py -v
pytest tests/test_login_redis.py -v
pytest tests/test_checkout_redis.py -v
pytest tests/test_config_validation.py -v
```

### Execute BDD Tests

Run all Behave features:

```bash
behave
```

Run an individual feature:

```bash
behave features/login.feature
```

### Headless Execution

```powershell
$env:CI = "true"
pytest -v
```

For additional commands and instructions, refer to `docs/test_execution.md`.

## 8. Test Data Management

The framework supports three test data sources.

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

The database path is configured in `config/config.yaml`.

Example:

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

### Redis Integration

Redis is used as an additional test data storage mechanism alongside Excel and SQLite.

The implementation is available in:

- `src/data/redis_reader.py`
- `tests/test_redis_reader.py`
- `tests/test_login_redis.py`
- `tests/test_checkout_redis.py`

**Redis Configuration**

Redis connection settings are defined in `config/config.yaml`.

Example:

```yaml
redis:
  host: "localhost"
  port: 6379
  db: 0
```

The framework also supports environment variable overrides:

| Environment Variable | Purpose | Default |
|---|---|---|
| `REDIS_HOST` | Redis server hostname | localhost |
| `REDIS_PORT` | Redis server port | 6379 |
| `REDIS_DB` | Redis database index | 0 |

PowerShell configuration:

```powershell
$env:REDIS_HOST = "localhost"
$env:REDIS_PORT = "6379"
$env:REDIS_DB = "0"
```

**Redis Test Data Structure**

Test data is stored using separate keys:

| Key Pattern | Description |
|---|---|
| `login_<username>` | Login test data |
| `checkout_<test_case>` | Checkout test data |

Examples:

```text
login_standard_user
login_locked_out_user
login_invalid_user
login_problem_user

checkout_valid_checkout
checkout_valid_checkout_problem_user
```

The values contain structured test data retrieved from the corresponding Excel worksheets.

**Automatic Test Data Seeding and Cleanup**

Redis test data is managed through the session-scoped `seed_redis_test_data` fixture in `tests/conftest.py`.

The fixture:

1. Reads login records from the `LoginData` worksheet.
2. Reads checkout records from the `CheckoutData` worksheet.
3. Stores login records using `login_<username>` keys.
4. Stores checkout records using `checkout_<test_case>` keys.
5. Makes the seeded data available to Redis-backed tests.
6. Deletes only the keys seeded by the fixture after the test session finishes.
7. Closes its Redis connection.

Both Redis-backed UI test modules depend on this fixture, ensuring that test data is available before execution.

**Redis Requirements**

A running Redis server is required for local Redis-backed tests.

The Python Redis client is installed through:

```bash
pip install redis==8.1.0
```

The dependency is also included in `requirements.txt`.

Redis integration is validated through the Redis reader tests and the Redis-backed login and checkout tests.

## 9. Allure Test Reporting

Allure is integrated with Pytest to provide detailed and structured test execution reports.

### Allure Configuration

The Pytest integration is provided by `allure-pytest`, which is included in `requirements.txt`.

The Allure CLI is managed through npm using:

- `package.json`
- `package-lock.json`

The following configuration is present in `pytest.ini`:

```ini
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = --alluredir=allure-results
```

This configuration automatically generates raw Allure result files in the `allure-results/` directory whenever Pytest executes.

### Generating an Allure Report Locally

Install the Allure CLI dependencies using:

```bash
npm ci
```

Run the Pytest suite:

```bash
pytest -v
```

Generate the HTML report:

```bash
npx allure generate allure-results --clean -o allure-report
```

Open the generated report:

```bash
npx allure open allure-report
```

The generated HTML report provides an interactive view of test execution results.

### Allure Test Metadata and Steps

Allure annotations are implemented in the login test module.

The integration includes:

- Epics.
- Features.
- Stories.
- Severity levels.
- Tags.
- Dynamic test titles.
- Named test execution steps.

These annotations help organize test results and make individual test scenarios easier to identify.

### Failure Diagnostics

The Pytest reporting hook in `tests/conftest.py` collects additional information when a test fails during its execution phase.

The available attachments include:

- Full-page screenshot of the browser.
- Current page URL and title.
- Browser console messages.
- Test failure details.

These attachments are included in the corresponding Allure test result when available.

### Allure Reporting in GitHub Actions

The GitHub Actions workflow also generates Allure reports after test execution.

For each browser in the configured matrix, the workflow:

1. Executes the Pytest suite.
2. Generates Allure result files.
3. Generates the HTML Allure report.
4. Uploads the raw Allure results as a workflow artifact.
5. Uploads the generated HTML report as a separate workflow artifact.

The workflow produces browser-specific artifacts:

| Browser | Allure HTML Report | Raw Allure Results |
|---|---|---|
| Chromium | `allure-report-chromium` | `allure-results-chromium` |
| Chrome | `allure-report-chrome` | `allure-results-chrome` |
| Edge | `allure-report-edge` | `allure-results-edge` |

Artifacts can be downloaded from the corresponding GitHub Actions workflow run.

To view a downloaded HTML report, extract the report ZIP file, open a terminal in the extracted report directory, and run:

```bash
python -m http.server 8000
```

Then open the following address in a browser:

`http://localhost:8000`

This serves the generated report locally.

## 10. Continuous Integration

GitHub Actions is configured through:

`.github/workflows/automation.yml`

The workflow supports:

- Execution on pushes to configured branches.
- Execution on pull requests targeting `main`.
- Chromium, Chrome, and Edge browser matrix testing.
- Python environment setup and dependency installation.
- Node.js setup and Allure CLI installation.
- Playwright browser installation.
- Redis service container initialization.
- Environment-based Redis connection configuration.
- Automated Pytest execution.
- Allure report generation after test execution.
- Uploading browser-specific Allure reports and raw results as downloadable artifacts.

Redis runs as a service container during CI execution. Its connection settings are provided through environment variables.

The `seed_redis_test_data` fixture automatically populates Redis when the Redis-backed tests execute.

Workflow results, job statuses, logs, and downloadable artifacts can be inspected through the Actions tab of the GitHub repository.

## 11. Current Test Results

**Recorded successful local Pytest execution:**

| Metric | Result |
|---|---:|
| Tests collected | 50 |
| Passed | 50 |
| Failed | 0 |

The passing tests cover:

- Browser management.
- Configuration validation.
- Base page functionality.
- Framework setup.
- Excel reader functionality.
- SQLite database operations.
- Redis reader operations.
- Redis-backed login automation.
- Redis-backed checkout automation.
- Inventory and product listing.
- Checkout scenarios.

These results represent a recorded local execution and do not independently establish the status of every GitHub Actions browser job or the complete Behave suite.

Allure HTML reports and raw result artifacts have also been generated and uploaded through GitHub Actions for the configured browser matrix.

## 12. Current Limitations

- Redis-backed tests require an accessible Redis server.
- Excel-based test data integration is implemented in the Pytest login and checkout modules, not throughout Behave.
- The SauceDemo `problem_user` account exhibits unexpected behavior during checkout information entry. The framework detects and validates this behavior as an expected application defect.
- Allure metadata annotations are currently demonstrated in the login test module and have not been applied uniformly across every test module.
- Failure diagnostic attachments are implemented for test execution-phase failures. Their behavior should also be checked using a deliberately failing test before considering failure reporting fully validated.

## 13. Team Responsibilities

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
- Redis-based test data integration.
- Redis reader and integration test coverage.
- Additional test scenarios and framework documentation.

## 14. Project Status

The framework provides modular UI automation, Pytest and Behave testing, centralized configuration, Excel-based test data reading, SQLite database operations, Redis-based test data management, GitHub Actions integration, and Allure test reporting.

The recorded local Pytest execution completed with 50 passing tests and no failures.

Redis integration includes connection management, configuration validation, structured test data storage and retrieval, automatic test data seeding, cleanup, and Redis-backed login and checkout scenarios.

Allure reporting is integrated locally and into the GitHub Actions workflow. The framework generates interactive HTML reports, stores raw test results, and provides browser-specific downloadable reporting artifacts.