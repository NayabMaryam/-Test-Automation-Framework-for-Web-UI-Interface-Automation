# Setup Guide

## 1. Introduction

This document provides instructions for setting up and configuring the UI Test Automation Framework.

The framework is developed using Python, Playwright, Pytest, and Behave. It supports automated web UI testing of the SauceDemo application using the Page Object Model (POM) design pattern.

The framework also integrates multiple test data sources, including Excel, SQLite, and Redis, along with centralized configuration management and continuous integration through GitHub Actions.

## 2. Prerequisites

Ensure the following software and tools are installed before setting up the framework.

| Software / Tool | Purpose |
|---|---|
| Python 3.12 | Primary programming language |
| pip | Python package management |
| Git | Version control |
| GitHub | Repository hosting |
| Visual Studio Code | Recommended development environment |
| Redis Server | Redis-based test data management |
| Playwright | Browser automation |

**Recommended:** Python 3.12 is used by the GitHub Actions workflow and is recommended for local development.

## 3. Clone the Repository

Clone the project repository:

```bash
git clone https://github.com/NayabMaryam/-Test-Automation-Framework-for-Web-UI-Interface-Automation.git
```

Navigate to the project directory:

```bash
cd -Test-Automation-Framework-for-Web-UI-Interface-Automation
```

## 4. Create and Activate a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Verify the Python version:

```bash
python --version
```

## 5. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The requirements file includes the dependencies needed for:

- Playwright browser automation.
- Pytest test execution.
- Behave BDD testing.
- Excel test data reading.
- YAML configuration management.
- Redis connectivity.

Install the Playwright browser binaries:

```bash
python -m playwright install
```

For Linux-based environments, including GitHub Actions, install browser system dependencies when required:

```bash
python -m playwright install --with-deps
```

## 6. Configure the Framework

The framework uses centralized YAML-based configuration.

Configuration file:

```text
config/config.yaml
```

The configuration file defines the application URL, browser settings, timeouts, database location, and Redis connection settings.

Example configuration:

```yaml
application:
  base_url: "https://www.saucedemo.com/"

browser:
  name: "chromium"
  headless: false
  slow_mo: 0

timeouts:
  default: 10000
  navigation: 30000

test:
  screenshot_on_failure: true

database:
  path: "database/test_data.db"

redis:
  host: "localhost"
  port: 6379
  db: 0
```

The `ConfigReader` class, implemented in:

```text
src/core/config_reader.py
```

loads the YAML configuration and validates the required settings.

### Environment Variable Overrides

Browser and Redis configuration can be overridden using environment variables.

| Variable | Description | Default |
|---|---|---|
| BROWSER | Browser selection | chromium |
| CI | Enables headless browser execution | false |
| REDIS_HOST | Redis server hostname | localhost |
| REDIS_PORT | Redis server port | 6379 |
| REDIS_DB | Redis database index | 0 |

For Windows Command Prompt:

```cmd
set BROWSER=chromium
set REDIS_HOST=localhost
set REDIS_PORT=6379
set REDIS_DB=0
```

For Windows PowerShell:

```powershell
$env:BROWSER = "chromium"
$env:REDIS_HOST = "localhost"
$env:REDIS_PORT = "6379"
$env:REDIS_DB = "0"
```

When `CI=true`, the browser automatically runs in headless mode.

## 7. Redis Server Setup

Redis integration provides an additional mechanism for storing and retrieving structured test data.

Unlike Excel and SQLite, Redis stores test data as key-value records and allows fast retrieval during automated test execution.

### 7.1 Install and Start Redis

Redis must be installed and running before executing Redis-dependent tests locally.

Redis is not bundled with the Python project dependencies.

For Windows development environments, Redis can be run through:

- Docker Desktop.
- Windows Subsystem for Linux (WSL).
- A compatible Redis server installation.

For Docker Desktop, start a Redis 7 container:

```cmd
docker run -d --name ui-automation-redis -p 6379:6379 redis:7
```

Verify that the container is running:

```cmd
docker ps
```

Check the Redis server response:

```cmd
docker exec -it ui-automation-redis redis-cli ping
```

Expected output:

```text
PONG
```

If the container already exists but is stopped, start it:

```cmd
docker start ui-automation-redis
```

### 7.2 Configure Redis Connection

The Redis connection is configured through the `redis` section of:

```text
config/config.yaml
```

Default configuration:

```yaml
redis:
  host: "localhost"
  port: 6379
  db: 0
```

Environment variables can override these values when required.

### 7.3 Redis Reader Implementation

Redis functionality is implemented in:

```text
src/data/redis_reader.py
```

The Redis reader provides reusable operations for:

- Establishing Redis connections.
- Reusing existing connections.
- Closing Redis connections.
- Reconnecting after connection closure.
- Storing structured test data.
- Retrieving test data by key.
- Retrieving all stored test data.
- Deleting individual test records.
- Deleting test data using supported key-prefix operations.

Redis integration is validated through:

```text
tests/test_redis_reader.py
```

### 7.4 Redis Test Data Seeding

Redis-based login and checkout tests require test records to be available in Redis before execution.

The framework uses a session-scoped Pytest fixture:

```text
tests/conftest.py
```

The fixture:

```python
seed_redis_test_data
```

performs the following operations:

1. Reads login records from the `LoginData` worksheet in `test_data/test_data.xlsx`.
2. Reads checkout records from the `CheckoutData` worksheet.
3. Stores login records using the `login_<username>` key format.
4. Stores checkout records using the `checkout_<test_case>` key format.
5. Makes the seeded records available during the test session.
6. Deletes only the keys created by the fixture after the test session finishes.

The Redis-based test modules use this fixture automatically:

```text
tests/test_login_redis.py
tests/test_checkout_redis.py
```

**Note:** Redis test data is seeded automatically when the Redis-dependent Pytest tests execute. A separate manual seeding step is not required for these tests.

### 7.5 Verify Redis Test Data

After running Redis-dependent tests, the fixture cleans up its seeded records.

Therefore, an empty Redis database after test execution is expected.

To inspect Redis while test data is available, use:

```cmd
docker exec -it ui-automation-redis redis-cli
```

Then execute:

```redis
KEYS login_*
KEYS checkout_*
```

Exit the Redis CLI:

```redis
EXIT
```

The Redis test records are temporary and are removed by the fixture during teardown.

## 8. Test Data Configuration

The framework supports three test data sources.

### 8.1 Excel Integration

Excel test data is maintained in:

```text
test_data/test_data.xlsx
```

The workbook contains:

| Worksheet | Purpose |
|---|---|
| LoginData | Login test scenarios |
| CheckoutData | Checkout test scenarios |

Implementation:

```text
src/data/excel_reader.py
```

Excel-based tests are available in:

```text
tests/test_login.py
tests/test_checkout.py
tests/test_excel_reader.py
```

### 8.2 SQLite Database Integration

SQLite database functionality is implemented in:

```text
src/data/database_reader.py
```

Database configuration:

```yaml
database:
  path: "database/test_data.db"
```

The database reader supports:

- Database connection management.
- Database initialization.
- SQL query execution.
- Test data insertion.
- Retrieving all test records.
- Retrieving records by test case.
- Updating existing records.
- Deleting test records.

Database tests are available in:

```text
tests/test_database_reader.py
```

### 8.3 Redis Integration

Redis functionality is implemented in:

```text
src/data/redis_reader.py
```

Redis is used for key-value-based storage and retrieval of structured login and checkout test records.

Redis-based UI tests are available in:

```text
tests/test_login_redis.py
tests/test_checkout_redis.py
```

The test data is automatically seeded and cleaned up through the `seed_redis_test_data` fixture in `tests/conftest.py`.

## 9. Running Automated Tests

Ensure that:

- The virtual environment is activated.
- Dependencies are installed.
- Redis is running when executing Redis-dependent tests.
- The configuration file contains valid settings.
- The Excel test data workbook is available.

### 9.1 Execute All Pytest Tests

```bash
pytest -v
```

### 9.2 Execute Individual Test Modules

```bash
pytest tests/test_login.py -v

pytest tests/test_inventory.py -v

pytest tests/test_checkout.py -v

pytest tests/test_excel_reader.py -v

pytest tests/test_database_reader.py -v

pytest tests/test_redis_reader.py -v

pytest tests/test_login_redis.py -v

pytest tests/test_checkout_redis.py -v
```

### 9.3 Execute Redis Integration Tests

Run both Redis-based UI test modules:

```bash
pytest tests/test_login_redis.py tests/test_checkout_redis.py -v
```

The `seed_redis_test_data` fixture automatically loads the required records before the tests execute and cleans them up afterward.

### 9.4 Execute BDD Tests

Run all Behave feature files:

```bash
behave
```

Run an individual feature:

```bash
behave features/login.feature
```

### 9.5 Headless Execution

Enable headless execution:

Windows CMD:

```cmd
set CI=true
pytest -v
```

PowerShell:

```powershell
$env:CI = "true"
pytest -v
```

## 10. Continuous Integration Setup

The framework uses GitHub Actions for automated test execution.

Workflow configuration:

```text
.github/workflows/automation.yml
```

The workflow includes:

- Repository checkout.
- Python environment setup.
- Dependency installation.
- Playwright browser installation.
- Redis service container setup.
- Redis health checks.
- Automated Pytest execution.
- Cross-browser testing using a browser matrix.

The Redis service is configured using the official Redis 7 Docker image.

The workflow uses the following environment variables:

```yaml
REDIS_HOST: localhost
REDIS_PORT: 6379
REDIS_DB: 0
```

The Redis-dependent Pytest tests seed their own test data through the session-scoped fixture.

GitHub Actions executes the workflow for the configured branches and pull requests.

Workflow execution results can be inspected through the repository's Actions tab.

## 11. Troubleshooting

### Python or pip Not Recognized

Verify the Python installation:

```cmd
python --version
```

If Python is installed but not recognized, verify that it has been added to the system PATH.

### Playwright Browser Not Installed

Execute:

```bash
python -m playwright install
```

### Redis Connection Refused

Verify that the Redis container is running:

```cmd
docker ps
```

Start the container if necessary:

```cmd
docker start ui-automation-redis
```

Verify connectivity:

```cmd
docker exec -it ui-automation-redis redis-cli ping
```

Expected response:

```text
PONG
```

### Redis Test Data Not Found

Check the following:

1. Redis server is running.
2. Redis host, port, and database settings are correct.
3. The Excel workbook exists at `test_data/test_data.xlsx`.
4. The workbook contains the required `LoginData` and `CheckoutData` worksheets.
5. The Redis seeding fixture is included in the test function arguments.

Example:

```python
def test_login_with_redis_data(
    page, config, redis, username, seed_redis_test_data
):
    ...
```

### Browser Launch Failure

Verify the installed Playwright browser binaries:

```bash
python -m playwright install
```

Also verify the browser selection:

```cmd
set BROWSER=chromium
```

### Missing Python Dependencies

Reinstall project dependencies:

```bash
pip install -r requirements.txt
```

## 12. Project Configuration and Dependencies

Important configuration and dependency files:

| File | Purpose |
|---|---|
| `requirements.txt` | Python package dependencies |
| `config/config.yaml` | Centralized framework configuration |
| `pytest.ini` | Pytest execution configuration |
| `.github/workflows/automation.yml` | GitHub Actions workflow |
| `test_data/test_data.xlsx` | Excel-based test data |
| `database/test_data.db` | SQLite database |
| `tests/conftest.py` | Shared Pytest fixtures and Redis test data seeding |

## 13. Additional Documentation

For further information, refer to:

- `README.md` - Project overview, implemented features, and technologies.
- `docs/architecture.md` - Framework architecture and component interactions.
- `docs/setup_guide.md` - Installation and configuration instructions.
- `docs/test_execution.md` - Test execution procedures and commands.

## 14. Conclusion

Following this setup guide provides the necessary environment and configuration to execute the UI Test Automation Framework.

The framework integrates browser automation, data-driven testing, BDD testing, Excel, SQLite, Redis, and continuous integration to support modular and reusable web UI test automation.