# System Architecture: UI Test Automation Framework

## 1. Introduction

The UI Test Automation Framework is a Python-based automated testing solution developed using Playwright, Pytest, and Behave.

The framework automates functional testing of the [SauceDemo](https://www.saucedemo.com/) web application.

It follows the Page Object Model (POM) architectural pattern, separating test logic, browser interactions, configuration management, and test data operations into modular components.

The framework supports:

- Conventional automated testing using Pytest.
- Behavior-Driven Development (BDD) using Behave and Gherkin.
- Browser automation using Playwright.
- External test data integration through Excel.
- Relational database operations using SQLite.
- In-memory test data storage using Redis.
- Automated cross-browser testing through GitHub Actions.

## 2. Architectural Design

The framework follows a layered architecture consisting of the following components:

1. Test Execution Layer
2. Page Object Layer
3. Core Framework Layer
4. Test Data Management Layer
5. Configuration Layer
6. Continuous Integration Layer

Each layer has a defined responsibility and interacts with other layers through reusable interfaces.

## 3. High-Level Architecture

```text
                 UI TEST AUTOMATION FRAMEWORK
                            |
          +-----------------+-----------------+
          |                                   |
     Test Execution                      Configuration
          |                                   |
    +-----+------+                       config.yaml
    |            |                           |
  Pytest       Behave                   ConfigReader
    |            |                           |
    +-----+------+                           |
          |                                   |
     Page Object Layer <----------------------+
          |
    +-----+----------------------------------+
    |                  |                     |
 LoginPage        InventoryPage          CartPage
    |                  |                     |
    +------------------+---------------------+
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
        +--------------+--------------+
        |              |              |
      Excel          SQLite          Redis
        |              |              |
   ExcelReader   DatabaseReader   RedisReader
        |              |              |
        +--------------+--------------+
                       |
                 Test Execution

              CONTINUOUS INTEGRATION
                       |
                  GitHub Actions
                       |
              +--------+--------+
              |                 |
          Redis Service     Browser Matrix
              |                 |
          Pytest Suite     Playwright Browsers
```

## 4. Test Execution Layer

The test execution layer manages test scenarios and their execution.

### 4.1 Pytest

Pytest provides:

- Test discovery and execution.
- Parameterized test cases.
- Reusable fixtures.
- Test setup and teardown.
- Assertions and failure reporting.

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
| Standard user login | login_standard_user |
| Locked-out user login | login_locked_out_user |
| Invalid user login | login_invalid_user |
| Problem user login | login_problem_user |
| Valid checkout | checkout_valid_checkout |
| Problem user checkout | checkout_valid_checkout_problem_user |

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

## 9. Continuous Integration Architecture

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

## 10. Architectural Benefits

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

## 11. Current Limitations

- Redis-dependent tests require an available Redis service.
- Excel test data integration is implemented in selected Pytest modules rather than universally across all test suites.
- SQLite and Redis serve different data management purposes and are not interchangeable.
- SauceDemo's problem_user account exhibits known unexpected behavior during checkout information entry.
- Allure reporting and automatic screenshot capture require separate verification.

## 12. Conclusion

The framework uses a modular, layered architecture to support maintainable and reusable UI automation.

Integration of Playwright, Pytest, Behave, Excel, SQLite, and Redis provides multiple testing and data management capabilities.

The Redis integration extends the framework with in-memory test data storage, structured record retrieval, automated seeding, and cleanup.

GitHub Actions further supports automated execution through a Redis service container and a cross-browser testing matrix.