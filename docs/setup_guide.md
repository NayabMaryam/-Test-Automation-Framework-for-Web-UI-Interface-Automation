# Setup Guide

## 1. Introduction

This document provides instructions for setting up and configuring the UI Test Automation Framework.

The framework is developed using Python, Playwright, Pytest, and Behave. It supports automated web UI testing of the SauceDemo application using the Page Object Model (POM) design pattern.

The framework also integrates multiple test data sources, including Excel, SQLite, and Redis, along with centralized configuration management, Allure test reporting, and continuous integration through GitHub Actions.

## 2. Prerequisites

Ensure the following software and tools are installed before setting up the framework.

| Software / Tool | Purpose |
|---|---|
| Python 3.12 | Primary programming language |
| pip | Python package management |
| Node.js | JavaScript runtime required for Allure CLI |
| npm | Node.js package management and Allure CLI installation |
| Git | Version control |
| GitHub | Repository hosting |
| Visual Studio Code | Recommended development environment |
| Docker Desktop | Running Redis locally |
| Playwright | Browser automation |
| Redis Server | Redis-based test data management |

**Recommended:** Python 3.12 is used by the GitHub Actions workflow and is recommended for local development.

Node.js and npm are required to install and execute the Allure CLI.

Verify the installations:

```bash
python --version
pip --version
node --version
npm --version
git --version
```

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

### 5.1 Python Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The requirements file includes dependencies for:

- Playwright browser automation.
- Pytest test execution and fixtures.
- Behave BDD testing.
- Excel test data reading.
- YAML configuration management.
- Redis connectivity.
- Allure Pytest integration.

### 5.2 Install Playwright Browsers

Install the required Playwright browser binaries:

```bash
python -m playwright install
```

For Linux-based environments, including GitHub Actions, install browser system dependencies when required:

```bash
python -m playwright install --with-deps
```

### 5.3 Install Allure CLI

Allure reporting uses two components:

- **allure-pytest:** Python integration that collects test execution results and generates Allure-compatible result files.
- **Allure CLI:** Node.js-based command-line tool that generates and serves the HTML report.

The Python integration is included in `requirements.txt`:

```text
allure-pytest==2.16.2
```

The Allure CLI is managed through npm.

The project contains:

- `package.json`
- `package-lock.json`

Install the Node.js dependencies from the project root:

```bash
npm ci
```

This installs the exact dependency versions recorded in `package-lock.json`.

Verify the Allure CLI installation:

```bash
npx allure --version
```

The verified project version is:

```text
3.33.0
```

**Note:** `npm ci` should be used when setting up an existing cloned project because it installs dependencies according to the committed lock file.

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

**Important:** Keep Docker Desktop and the Redis container running while executing Redis-dependent tests locally.

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

## 9. Allure Test Reporting

The framework integrates Allure reporting to generate detailed, interactive HTML reports from Pytest execution results.

Allure reporting provides a visual representation of test execution, including:

- Overall test execution summary.
- Passed, failed, skipped, and broken test results.
- Individual test case details.
- Execution durations.
- Test execution history and report statistics where supported by the generated data.

### 9.1 Allure Integration Components

The implementation uses the following components:

| Component | Version | Purpose |
|---|---|---|
| allure-pytest | 2.16.2 | Pytest integration and result collection |
| Allure CLI | 3.33.0 | HTML report generation and viewing |
| Node.js | 26.13.1 (verified locally) | Runtime for Allure CLI |
| npm | 11.20.0 (verified locally) | Node.js package management |

The Python integration is maintained in:

```text
requirements.txt
```

The Allure CLI dependency is maintained in:

```text
package.json
package-lock.json
```

### 9.2 Pytest Configuration

Allure result collection is configured through:

```text
pytest.ini
```

The following configuration enables automatic Allure result generation:

```ini
addopts = --alluredir=allure-results
```

Whenever Pytest is executed, the Allure integration automatically generates result files in:

```text
allure-results/
```

The generated result directory contains the test execution data consumed by the Allure CLI.

Generated result and report directories are excluded from version control through `.gitignore`.

### 9.3 Execute Tests and Generate Allure Results

First, ensure the virtual environment is activated and the Redis server is running.

Execute the complete Pytest suite:

```bash
pytest -v
```

To clear previous Allure results before executing the tests:

```bash
pytest -v --clean-alluredir
```

After execution, the following directory should be available:

```text
allure-results/
```

### 9.4 Generate the HTML Report

Once test execution is complete, generate the Allure HTML report:

```bash
npx allure generate allure-results --clean
```

The generated report is stored in:

```text
allure-report/
```

The `--clean` option removes the previous generated report before creating a new one.

### 9.5 View the Allure Report Locally

To open the generated report:

```bash
npx allure open allure-report
```

The Allure CLI starts a local server and opens the report in the default browser.

The report can then be explored through its interactive dashboard.

### 9.6 Allure Directory Structure

The following directories are generated during report execution:

| Directory | Purpose |
|---|---|
| `allure-results/` | Raw test execution results |
| `allure-report/` | Generated interactive HTML report |
| `node_modules/` | Installed Node.js dependencies |

These directories are generated locally or during CI execution and are excluded from Git version control.

The dependency management files are committed:

```text
package.json
package-lock.json
```

### 9.7 Allure Reporting in GitHub Actions

The GitHub Actions workflow also generates Allure reports during automated CI execution.

The workflow executes the Pytest suite across three browser configurations:

- Chromium.
- Google Chrome.
- Microsoft Edge.

For each browser job, the workflow generates and uploads the corresponding Allure report and raw result artifacts.

The generated artifacts follow these naming conventions:

| Artifact | Purpose |
|---|---|
| `allure-report-chromium` | Generated Chromium HTML report |
| `allure-report-chrome` | Generated Chrome HTML report |
| `allure-report-edge` | Generated Edge HTML report |
| `allure-results-chromium` | Raw Chromium test results |
| `allure-results-chrome` | Raw Chrome test results |
| `allure-results-edge` | Raw Edge test results |

### 9.8 Download and View CI Allure Reports

The generated Allure reports can be downloaded directly from GitHub Actions.

Steps:

1. Open the project repository on GitHub.
2. Navigate to the **Actions** tab.
3. Open the relevant successful workflow execution.
4. Locate the **Artifacts** section.
5. Download the required `allure-report-*` artifact.
6. Extract the downloaded ZIP archive.
7. Open the extracted `allure-report` directory.
8. Open a terminal inside that directory.
9. Start a local HTTP server:

```bash
python -m http.server 8000
```

10. Open the following address in a web browser:

```text
http://localhost:8000
```

The instructor can now interact with the complete generated Allure HTML report without installing the Allure CLI or rerunning the test suite.

**Important:** Download the `allure-report-*` artifact when you want to view the interactive HTML report. The `allure-results-*` artifact contains the raw execution data rather than the generated HTML report.

## 10. Running Automated Tests

Ensure that:

- The virtual environment is activated.
- Python dependencies are installed.
- Node.js dependencies are installed using `npm ci`.
- Redis is running when executing Redis-dependent tests.
- The configuration file contains valid settings.
- The Excel test data workbook is available.

### 10.1 Execute All Pytest Tests

```bash
pytest -v
```

### 10.2 Execute Individual Test Modules

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

### 10.3 Execute Redis Integration Tests

Run both Redis-based UI test modules:

```bash
pytest tests/test_login_redis.py tests/test_checkout_redis.py -v
```

The `seed_redis_test_data` fixture automatically loads the required records before the tests execute and cleans them up afterward.

### 10.4 Execute BDD Tests

Run all Behave feature files:

```bash
behave
```

Run an individual feature:

```bash
behave features/login.feature
```

### 10.5 Headless Execution

Enable headless execution.

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

## 11. Continuous Integration Setup

The framework uses GitHub Actions for automated test execution.

Workflow configuration:

```text
.github/workflows/automation.yml
```

The workflow includes:

- Repository checkout.
- Python environment setup.
- Dependency installation.
- Node.js setup for Allure CLI.
- npm dependency installation.
- Playwright browser installation.
- Redis service container setup.
- Redis health checks.
- Automated Pytest execution.
- Cross-browser testing using a browser matrix.
- Allure result generation.
- Allure HTML report generation.
- Uploading Allure reports and raw results as workflow artifacts.

The Redis service is configured using the official Redis 7 Docker image.

The workflow uses the following environment variables:

```yaml
REDIS_HOST: localhost
REDIS_PORT: 6379
REDIS_DB: 0
```

The Redis-dependent Pytest tests seed their own test data through the session-scoped fixture.

Each browser job generates its own Allure report artifacts, allowing test results to be inspected independently for Chromium, Chrome, and Edge.

GitHub Actions execution results and downloadable reports can be inspected through the repository's Actions tab.

## 12. Troubleshooting

### Python or pip Not Recognized

Verify the Python installation:

```cmd
python --version
```

If Python is installed but not recognized, verify that it has been added to the system PATH.

### Node.js or npm Not Recognized

Verify the installation:

```bash
node --version
npm --version
```

If either command is unavailable, install Node.js and reopen the terminal.

### Allure CLI Not Recognized

Ensure Node.js dependencies are installed:

```bash
npm ci
```

Verify Allure:

```bash
npx allure --version
```

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

### Allure Results Directory Not Generated

Verify that:

- `allure-pytest` is installed.
- `pytest.ini` contains `addopts = --alluredir=allure-results`.
- Tests are executed using Pytest.

Verify the installed integration:

```bash
pip show allure-pytest
```

### Allure Report Generation Failure

Ensure that the test suite has completed and the `allure-results/` directory contains result files.

Generate the report again:

```bash
npx allure generate allure-results --clean
```

### Allure Report Does Not Display Correctly

Use the Allure CLI to serve the generated report:

```bash
npx allure open allure-report
```

For downloaded CI artifacts, use a local HTTP server from the extracted report directory:

```bash
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

### Missing Python Dependencies in GitHub Actions

Verify that the required dependencies are included in `requirements.txt`.

### Missing Allure Artifacts in GitHub Actions

Check the following:

1. The relevant workflow execution completed its report-generation steps.
2. The Allure results directory was generated.
3. The Allure HTML report was successfully generated.
4. The artifact upload step executed.
5. The relevant browser job logs do not contain report-generation errors.

## 13. Project Configuration and Dependencies

Important configuration and dependency files:

| File | Purpose |
|---|---|
| `requirements.txt` | Python package dependencies |
| `package.json` | Node.js development dependencies |
| `package-lock.json` | Locked Node.js dependency versions |
| `config/config.yaml` | Centralized framework configuration |
| `pytest.ini` | Pytest execution and Allure result configuration |
| `.github/workflows/automation.yml` | GitHub Actions workflow |
| `test_data/test_data.xlsx` | Excel-based test data |
| `database/test_data.db` | SQLite database |
| `tests/conftest.py` | Shared Pytest fixtures and Redis test data seeding |
| `.gitignore` | Excludes generated files and local dependencies |

## 14. Additional Documentation

For further information, refer to:

- `README.md` - Project overview, implemented features, and technologies.
- `docs/architecture.md` - Framework architecture and component interactions.
- `docs/setup_guide.md` - Installation and configuration instructions.
- `docs/test_execution.md` - Test execution procedures, reporting, and commands.

## 15. Conclusion

Following this setup guide provides the necessary environment and configuration to execute the UI Test Automation Framework.

The framework integrates browser automation, data-driven testing, BDD testing, Excel, SQLite, Redis, Allure test reporting, and continuous integration through GitHub Actions.

Allure reporting provides interactive HTML reports for local test executions and browser-specific CI executions. Generated reports can be inspected locally or downloaded from GitHub Actions as workflow artifacts.

The framework therefore provides a modular and reusable solution for automated web UI testing, test data management, cross-browser execution, and test reporting.