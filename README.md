# UI Test Automation Framework

## 1. Project Overview

The UI Test Automation Framework is a Python-based web UI testing solution developed using Playwright, Pytest, and Behave.

The framework automates testing of the [SauceDemo](https://www.saucedemo.com/) web application.

It follows the Page Object Model (POM) design pattern to improve code reusability, maintainability, and separation of test logic from browser interactions.

The framework supports conventional automated testing using Pytest and Behavior-Driven Development (BDD) using Behave and Gherkin.

It also provides centralized configuration management, external test data integration, database operations, Redis-based test data management, and cross-browser execution through GitHub Actions.

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

### Continuous Integration
- GitHub Actions workflow integration.
- Automated test execution on pushes and pull requests targeting the main branch.
- Browser matrix configuration for cross-browser testing.
- Redis service container for CI execution.
- Environment-based configuration for Redis and browser selection.

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
│   └── load_redis_data.py (optional standalone seeding utility, if present)
│
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

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
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
pytest tests/test_redis_reader.py -v
pytest tests/test_login_redis.py -v
pytest tests/test_checkout_redis.py -v
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

The database path is configured in:

`config/config.yaml`

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

## 9. Continuous Integration

GitHub Actions is configured through:

`.github/workflows/automation.yml`

The workflow supports:

- Execution on pushes to configured branches.
- Execution on pull requests targeting `main`.
- Chromium, Chrome, and Edge browser matrix testing.
- Python environment setup and dependency installation.
- Playwright browser installation.
- Redis service container initialization.
- Environment-based Redis connection configuration.
- Automated Pytest execution.

Redis runs as a service container during CI execution. Its connection settings are provided through environment variables.

The `seed_redis_test_data` fixture automatically populates Redis when the Redis-backed tests execute.

Workflow results and individual job logs can be inspected through the Actions tab of the GitHub repository.

## 10. Current Test Results

**Latest reported successful local Pytest execution:**

| Metric | Result |
|---|---:|
| Tests collected | 50 |
| Passed | 50 |
| Failed | 0 |
| Execution time | 47.96 seconds |

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

These results represent a reported local execution and do not independently establish the status of the GitHub Actions workflow or the complete Behave suite.

## 11. Current Limitations

- Redis-backed tests require an accessible Redis server.
- Excel-based test data integration is implemented in the Pytest login and checkout modules, not throughout Behave.
- The SauceDemo `problem_user` account exhibits unexpected behavior during checkout information entry. The framework detects and validates this behavior as an expected application defect.
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
- Redis-based test data integration.
- Redis reader and integration test coverage.
- Additional test scenarios and framework documentation.

## 13. Project Status

The framework provides modular UI automation, Pytest and Behave testing, centralized configuration, Excel-based test data reading, SQLite database operations, Redis-based test data management, and GitHub Actions integration.

The latest reported successful local Pytest execution completed with 50 passing tests and no failures.

Redis integration includes connection management, configuration validation, structured test data storage and retrieval, automatic test data seeding, cleanup, and Redis-backed login and checkout scenarios.