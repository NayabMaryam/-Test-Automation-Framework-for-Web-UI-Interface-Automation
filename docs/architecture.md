# System Architecture: UI Test Automation Framework

## 1. Introduction

The UI Test Automation Framework is a Python-based automated testing solution developed using Playwright, Pytest, and Behave.

The framework automates functional testing of the [SauceDemo](https://www.saucedemo.com/) web application.

It follows the Page Object Model (POM) architectural pattern, separating test logic, browser interactions, configuration management, test data operations, and reporting into modular components.

The framework supports:

- Conventional automated testing using Pytest.
- Behavior-Driven Development (BDD) using Behave and Gherkin.
- Browser automation using Playwright.
- External test data integration through Excel.
- Relational database operations using SQLite.
- In-memory test data storage using Redis.
- Automated test reporting using Allure.
- Automated cross-browser testing through GitHub Actions.
- HTML report generation and artifact storage through CI.

## 2. Architectural Design

The framework follows a layered architecture consisting of the following components:

1. Test Execution Layer
2. Page Object Layer
3. Core Framework Layer
4. Test Data Management Layer
5. Configuration Layer
6. Reporting Layer
7. Continuous Integration Layer

Each layer has a defined responsibility and interacts with other layers through reusable interfaces.

## 3. High-Level Architecture

```text
                 UI TEST AUTOMATION FRAMEWORK
                              |
          +-------------------+-------------------+
          |                   |                   |
    Test Execution       Configuration       Reporting
          |                   |                   |
     +----+----+         config.yaml          Allure
     |         |               |                  |
   Pytest    Behave       ConfigReader       Allure Pytest
     |         |               |               Adapter
     +----+----+               |                  |
          |                    |             allure-results/
          |                    |                  |
          |                    |             Allure CLI
          |                    |                  |
          |                    |             allure-report/
          |                    |                  |
          +--------------------+             HTML Report
          |
    Page Object Layer
          |
    +-----+--------------------------------+
    |                 |                    |
 LoginPage        InventoryPage          CartPage
    |                 |                    |
    +-----------------+--------------------+
                      |
                 ProductPage
                      |
                 CheckoutPage
                      |
                   BasePage
                      |
                  Playwright
                      |
                   SauceDemo


             TEST DATA MANAGEMENT LAYER
                      |
        +-------------+-------------+
        |             |             |
      Excel         SQLite        Redis
        |             |             |
   ExcelReader  DatabaseReader  RedisReader
        |             |             |
        +-------------+-------------+
                      |
                 Test Execution


             CONTINUOUS INTEGRATION
                      |
                 GitHub Actions
                      |
          +-----------+------------+
          |           |            |
       Browser     Redis       Allure
        Matrix    Service     Reporting
          |           |            |
       Chromium    Redis 7     HTML Report
       Chrome      Container   Generation
       Edge                     |
                                |
                         Artifact Upload
                                |
                      +---------+---------+
                      |         |         |
                   Chromium   Chrome     Edge
                   Reports    Reports    Reports
```

The reporting component is integrated with Pytest and GitHub Actions. Allure collects test execution data, generates HTML reports, and makes the generated reports available as CI artifacts.

## 4. Test Execution Layer

The test execution layer manages test scenarios and their execution.

### 4.1 Pytest

Pytest provides:

- Test discovery and execution.
- Parameterized test cases.
- Reusable fixtures.
- Test setup and teardown.
- Assertions and failure reporting.
- Integration with Allure reporting.

Test modules are located in the `tests/` directory.

### 4.2 Behave

Behave provides BDD support through Gherkin feature files and Python step definitions.

It separates business-readable test scenarios from their implementation.

Feature files are stored in `features/`, with corresponding step definitions in `features/steps/`.

## 5. Page Object Layer

The Page Object Model encapsulates application-specific interactions into reusable classes.

Each page object represents a particular page or functional component of SauceDemo.

### Main Components

| Component | Responsibility |
|---|---|
| BasePage | Common browser interaction methods |
| LoginPage | Login operations and authentication messages |
| InventoryPage | Product listing and inventory operations |
| ProductPage | Product details and interactions |
| CartPage | Shopping cart operations |
| CheckoutPage | Checkout information and order completion |

Page objects interact with the application through Playwright.

This approach reduces code duplication and improves maintainability.

## 6. Core Framework Layer

The core layer provides shared framework functionality.

### 6.1 BrowserManager

Implemented in:

`src/core/browser_manager.py`

Responsibilities:

- Browser initialization.
- Browser selection.
- Browser lifecycle management.
- Browser closure.

Supported browsers:

- Chromium
- Google Chrome
- Microsoft Edge

### 6.2 ConfigReader

Implemented in:

`src/core/config_reader.py`

Responsibilities:

- Reading YAML configuration.
- Providing centralized configuration access.
- Validating required configuration settings.
- Applying environment variable overrides.

Configuration is maintained in:

`config/config.yaml`

Browser settings can be overridden using `BROWSER` and `CI` environment variables.

Redis connection settings can be overridden using:

- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_DB`

## 7. Test Data Management Layer

The test data management layer provides multiple mechanisms for storing and retrieving test data.

### 7.1 Excel Integration

Implemented in:

`src/data/excel_reader.py`

Library: OpenPyXL

Test data is maintained in:

`test_data/test_data.xlsx`

The workbook contains:

- LoginData: Login scenarios and credentials.
- CheckoutData: Checkout scenarios and customer information.

ExcelReader retrieves records from individual worksheets and makes them available to automated tests.

### 7.2 SQLite Integration

Implemented in:

`src/data/database_reader.py`

SQLite provides relational database functionality.

The database location is configured in `config/config.yaml`.

Default configuration:

```yaml
database:
  path: "database/test_data.db"
```

Supported operations:

- Database connection management.
- Database initialization.
- Table creation.
- SQL query execution.
- Test data insertion.
- Retrieval of all test records.
- Retrieval by test case.
- Updating existing records.
- Deleting records.

### 7.3 Redis Integration

Implemented in:

`src/data/redis_reader.py`

Library: redis-py

Redis provides in-memory storage and retrieval of structured test data.

The integration supports:

- Redis connection management.
- Connection reuse.
- Connection closure.
- Reconnection after closure.
- Storing structured test data.
- Retrieving structured test data.
- Deleting individual records.
- Retrieving all test records.
- Deleting test records.

Redis configuration is maintained in `config/config.yaml`.

Example:

```yaml
redis:
  host: "localhost"
  port: 6379
  db: 0
```

Environment variables can override the default settings.

#### Redis Test Data Organization

The framework uses separate key prefixes to distinguish login and checkout records.

| Test Data | Redis Key |
|---|---|
| Standard user login | `login_standard_user` |
| Locked-out user login | `login_locked_out_user` |
| Invalid user login | `login_invalid_user` |
| Problem user login | `login_problem_user` |
| Valid checkout | `checkout_valid_checkout` |
| Problem user checkout | `checkout_valid_checkout_problem_user` |

#### Redis Test Data Seeding

Redis-dependent UI tests use a session-scoped Pytest fixture named `seed_redis_test_data`, implemented in `tests/conftest.py`.

The fixture:

1. Reads login records from the LoginData Excel worksheet.
2. Reads checkout records from the CheckoutData Excel worksheet.
3. Stores the records in Redis using their respective key prefixes.
4. Keeps track of the keys created during setup.
5. Deletes only those keys during teardown.
6. Closes the Redis connection after cleanup.

This ensures that Redis test data is available during test execution without requiring manual data insertion.

## 8. Test Fixtures and Resource Management

Pytest fixtures are maintained in:

`tests/conftest.py`

The framework provides reusable fixtures for:

| Fixture | Scope | Responsibility |
|---|---|---|
| config | Session | Configuration initialization |
| browser | Function | Browser lifecycle management |
| page | Function | New browser page for each test |
| database | Function | Temporary SQLite database setup |
| redis | Function | Redis connection management |
| seed_redis_test_data | Session | Redis test data initialization and cleanup |

The session-scoped Redis fixture prepares test data before dependent tests execute.

The function-scoped Redis fixture provides a RedisReader instance and closes its connection after each test.

## 9. Reporting Architecture: Allure

The framework integrates Allure reporting with Pytest to provide structured test execution results and HTML reports.

Allure reporting consists of two main components:

1. Allure Pytest adapter.
2. Allure Command-Line Interface (CLI).

### 9.1 Allure Pytest Integration

The Python integration is provided by:

`allure-pytest==2.16.2`

The dependency is maintained in:

`requirements.txt`

The Pytest configuration in `pytest.ini` includes:

```ini
addopts = --alluredir=allure-results
```

During Pytest execution, the Allure adapter collects test execution information and generates result files in:

`allure-results/`

These files contain structured test execution data used for report generation.

### 9.2 Allure CLI Integration

The Allure CLI is provided through the npm package:

`allure`

The package dependency is maintained in:

`package.json`

The CLI processes the raw result files generated by Pytest and creates an HTML report.

The generated report is stored in:

`allure-report/`

The reporting workflow consists of:

1. Execute Pytest tests.
2. Generate Allure result files.
3. Process the result files using the Allure CLI.
4. Generate the HTML report.
5. Open the generated report for inspection.

### 9.3 Reporting Workflow

```text
        Pytest Test Execution
                  |
                  |
          Allure Pytest Adapter
                  |
                  |
           allure-results/
                  |
                  |
              Allure CLI
                  |
                  |
           allure-report/
                  |
                  |
             HTML Report
                  |
                  |
          Report Visualization
```

The Python adapter is responsible for collecting test results, while the Allure CLI generates the visual HTML report.

### 9.4 Local Report Generation

Execute the Pytest suite:

```bash
pytest -v
```

Generate the Allure HTML report:

```bash
npx allure generate allure-results --clean -o allure-report
```

Open the generated report:

```bash
npx allure open allure-report
```

The report provides a graphical representation of test execution results, including test statuses and execution details.

### 9.5 Allure Reporting in GitHub Actions

Allure reporting is also integrated into the GitHub Actions workflow.

For each browser matrix execution, the workflow:

1. Executes the automated Pytest suite.
2. Collects Allure result files.
3. Generates the corresponding HTML report.
4. Uploads the raw results as a GitHub Actions artifact.
5. Uploads the generated HTML report as a separate artifact.

The workflow produces browser-specific artifacts.

| Browser | Allure Results Artifact | HTML Report Artifact |
|---|---|---|
| Chromium | `allure-results-chromium` | `allure-report-chromium` |
| Chrome | `allure-results-chrome` | `allure-report-chrome` |
| Edge | `allure-results-edge` | `allure-report-edge` |

These artifacts can be downloaded from the corresponding GitHub Actions workflow execution.

This allows test results and generated HTML reports to be inspected independently for each browser.

### 9.6 Generated File Management

The following generated directories are excluded from version control:

- `allure-results/`
- `allure-report/`
- `node_modules/`

They are maintained in `.gitignore`.

Generated Allure reports are stored as GitHub Actions artifacts rather than committed to the project repository.

## 10. Continuous Integration Architecture

GitHub Actions is used for automated test execution.

Workflow configuration:

`.github/workflows/automation.yml`

The workflow supports:

- Automated execution on pushes to configured branches.
- Pull request validation targeting the main branch.
- Python environment setup.
- Dependency installation.
- Playwright browser installation.
- Redis service container initialization.
- Redis health checks.
- Pytest execution.
- Cross-browser execution.
- Allure result collection.
- HTML report generation.
- Artifact upload.

### Redis Service in CI

The workflow provisions a Redis 7 service container.

Redis is exposed through port 6379 and configured with a health check to ensure that the service is ready before tests execute.

Environment variables configure the connection:

```yaml
REDIS_HOST: localhost
REDIS_PORT: 6379
REDIS_DB: 0
```

The Redis test data fixture seeds the required records during Pytest execution.

### Cross-Browser Execution

The workflow uses a browser matrix:

- Chromium
- Chrome
- Edge

Tests execute in headless mode in the CI environment.

Each browser execution generates its own Allure results and HTML report artifacts.

### CI Reporting and Artifact Storage

GitHub Actions stores the generated Allure reports and raw results as downloadable workflow artifacts.

The artifacts allow developers to:

- Inspect browser-specific test execution results.
- View generated HTML reports.
- Download raw Allure result files.
- Review test outcomes without rerunning the workflow locally.

## 11. Architectural Benefits

The architecture provides:

- Separation of concerns through layered design.
- Reusable browser interaction components.
- Maintainable test cases through POM.
- Multiple test data storage mechanisms.
- Centralized configuration and validation.
- Automated test data initialization and cleanup.
- Cross-browser testing support.
- Continuous integration through GitHub Actions.
- Support for both Pytest and BDD testing.
- Structured test execution reporting through Allure.
- Graphical HTML report generation.
- Browser-specific CI reporting artifacts.
- Separation of generated reports from source code.

## 12. Current Limitations

- Redis-dependent tests require an available Redis service.
- Excel test data integration is implemented in selected Pytest modules rather than universally across all test suites.
- SQLite and Redis serve different data management purposes and are not interchangeable.
- Behave scenarios are not currently integrated with the Allure Pytest reporting workflow.
- SauceDemo's `problem_user` account exhibits known unexpected behavior during checkout information entry.
- Automatic screenshot capture on test failure has not been independently verified.

## 13. Conclusion

The framework uses a modular, layered architecture to support maintainable and reusable UI automation.

Integration of Playwright, Pytest, Behave, Excel, SQLite, and Redis provides multiple testing and data management capabilities.

The Redis integration extends the framework with in-memory test data storage, structured record retrieval, automated seeding, and cleanup.

Allure reporting further enhances the framework by collecting Pytest execution results, generating HTML reports, and supporting browser-specific report artifacts through GitHub Actions.

GitHub Actions provides automated execution through a Redis service container and a cross-browser testing matrix, while preserving generated reports as downloadable CI artifacts.git status