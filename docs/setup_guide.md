# Setup and Installation Guide

## 1. Introduction

This guide explains how to configure and run the automated web UI testing framework.

The framework uses Python, Playwright, Pytest, Behave, OpenPyXL, and SQLite to automate and validate the SauceDemo application.

Application under test:

[https://www.saucedemo.com/](https://www.saucedemo.com/)

The framework supports:
- Pytest-based automated UI testing.
- Behavior-Driven Development (BDD) using Behave and Gherkin.
- Page Object Model (POM) architecture.
- YAML-based centralized configuration.
- Excel-based external test data integration.
- SQLite database-based test data management.

## 2. Prerequisites

Install the following software before setting up the project:

- Python 3.12 or a compatible supported Python version.
- Git.
- Visual Studio Code or another Python IDE.
- Google Chrome or Microsoft Edge if using those browser options.

Check the installed Python version:

```bash
python --version
```

Check Git:

```bash
git --version
```

SQLite is included in Python's standard library through the `sqlite3` module. A separate SQLite Python package is not required.

## 3. Obtain the Project

If the repository is already available locally, open its root directory.

Otherwise, clone the repository:

```bash
git clone <repository-url>
```

Navigate into the project directory:

```bash
cd <project-directory>
```

## 4. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Alternatively, use Command Prompt:

```cmd
.venv\Scripts\activate
```

After activation, the terminal should display:

```text
(.venv)
```

## 5. Install Dependencies

Install the project dependencies:

```bash
pip install -r requirements.txt
```

The framework uses the following main dependencies:

| Package | Purpose |
|---|---|
| pytest | Test execution |
| playwright | Browser automation |
| PyYAML | YAML configuration |
| behave | BDD execution |
| openpyxl | Excel workbook reading |

SQLite database functionality uses Python's built-in `sqlite3` module. No additional database driver is required.

If OpenPyXL is not already included in the requirements file, install it using:

```bash
pip install openpyxl
```

## 6. Install Playwright Browsers

Install the required Playwright browser binaries:

```bash
python -m playwright install
```

To install Chromium specifically:

```bash
python -m playwright install chromium
```

For Google Chrome and Microsoft Edge, the corresponding browser installations must be available on the system.

## 7. Verify the Project Structure

The framework uses the following main directories and components:

```text
project/
│
├── config/
│   └── config.yaml
│
├── database/
│   └── test_data.db
│
├── src/
│   ├── core/
│   │   ├── browser_manager.py
│   │   └── config_reader.py
│   │
│   ├── data/
│   │   ├── excel_reader.py
│   │   └── database_reader.py
│   │
│   └── pages/
│       ├── base_page.py
│       ├── login_page.py
│       ├── inventory_page.py
│       ├── product_page.py
│       ├── cart_page.py
│       └── checkout_page.py
│
├── test_data/
│   └── test_data.xlsx
│
├── tests/
│   ├── test_database_reader.py
│   ├── test_excel_reader.py
│   ├── test_login.py
│   ├── test_inventory.py
│   └── test_checkout.py
│
├── features/
│   ├── steps/
│   ├── login.feature
│   ├── inventory.feature
│   ├── product.feature
│   ├── cart.feature
│   └── checkout.feature
│
├── docs/
│
├── conftest.py
├── pytest.ini
└── requirements.txt
```

This represents the main framework components. Additional project files may exist.

## 8. Configure the Application

Open:

`config/config.yaml`

Verify that the application URL and browser settings are configured correctly.

The application under test is:

```text
https://www.saucedemo.com/
```

The configuration file manages:

- Application URL.
- Browser selection.
- Headless execution.
- Browser slow-motion settings.
- Default timeout.
- Navigation timeout.
- Database file location.
- Screenshot-on-failure configuration.

The database configuration uses the following setting:

```yaml
database:
  path: "database/test_data.db"
```

The configuration reader validates the required configuration sections and database path setting.

## 9. Configure Excel Test Data

The Excel workbook is located at:

`test_data/test_data.xlsx`

The workbook contains separate worksheets for different test modules.

### LoginData

Used by `tests/test_login.py`.

Expected fields include:

- `test_case`
- `username`
- `password`
- `expected`

### CheckoutData

Used by `tests/test_checkout.py`.

Expected fields include:

- `test_case`
- `username`
- `password`
- `first_name`
- `last_name`
- `postal_code`
- `expected_confirmation_text`

The worksheet names and column headers must match the names expected by the corresponding test modules.

The first row of each worksheet must contain unique, non-empty headers.

Completely empty data rows are ignored by the Excel reader.

**Important:** Keep the workbook at the expected path and do not rename the worksheets or required headers without updating the corresponding tests.

## 10. Configure SQLite Database Integration

The framework includes SQLite-based test data management.

The database reader is implemented in:

`src/data/database_reader.py`

The configured database location is:

`database/test_data.db`

The database path is defined in:

`config/config.yaml`

### Database initialization

The database reader provides an initialization mechanism that creates the database file and the required `test_data` table.

The database can be initialized through the `DatabaseReader` class.

### Database operations

The implemented database functionality includes:

- Establishing SQLite database connections.
- Executing parameterized SQL queries.
- Initializing the database and creating the test data table.
- Inserting test data.
- Retrieving all test data records.
- Retrieving test data by test case.
- Updating existing test data.
- Deleting test data by record ID.

### Database test coverage

Database functionality is tested in:

`tests/test_database_reader.py`

Execute the database reader tests:

```bash
pytest tests/test_database_reader.py -v
```

The tests verify database connectivity, query execution, initialization, insertion, retrieval, updating, and deletion.

### Database testing isolation

The database reader tests use Pytest's `tmp_path` fixture to create temporary database files.

The shared `database` fixture in `conftest.py` initializes an isolated database for individual test functions.

This approach prevents test cases from interfering with each other's database records.

**Important:** The configured database file and temporary test databases serve different purposes. The temporary databases are used for isolated testing, while the configured database path identifies the framework's database location.

SQLite is included in Python's standard library, so no additional SQLite dependency is required in `requirements.txt`.

## 11. Verify Data Source Integration

The framework currently implements two test data sources:

### Excel Integration

Implemented in:

- `src/data/excel_reader.py`
- `tests/test_excel_reader.py`

Execute:

```bash
pytest tests/test_excel_reader.py -v
```

### SQLite Integration

Implemented in:

- `src/data/database_reader.py`
- `tests/test_database_reader.py`

Execute:

```bash
pytest tests/test_database_reader.py -v
```

Both components provide reusable mechanisms for reading and managing test data.

**Current implementation status:** Excel and SQLite integration are implemented. Redis integration has not yet been implemented.

## 12. Verify Framework Installation

Execute the framework setup test:

```bash
pytest tests/test_framework_setup.py -v
```

Execute browser manager tests:

```bash
pytest tests/test_browser_manager.py -v
```

Execute configuration validation:

```bash
pytest tests/test_config_validation.py -v
```

## 13. Run the Framework

Execute the complete Pytest suite:

```bash
pytest -v
```

Execute BDD tests:

```bash
behave
```

Refer to `test_execution.md` for detailed execution commands and reporting instructions.

## 14. Troubleshooting

### Python is not recognized

Verify that Python is installed and added to the system PATH.

### Virtual environment activation fails

For PowerShell, check the execution policy if activation scripts are blocked.

### Missing dependencies

Activate the virtual environment and execute:

```bash
pip install -r requirements.txt
```

### Playwright browser launch failure

Install the required browser binaries:

```bash
python -m playwright install
```

### Excel workbook not found

Verify the workbook location:

```text
test_data/test_data.xlsx
```

### Worksheet not found

Check the exact worksheet name, including capitalization:

- `LoginData`
- `CheckoutData`

### Excel header validation failure

Check that the first row contains unique, non-empty column headers.

### Database initialization or connection failure

Verify:

- The database path in `config/config.yaml`.
- That the parent database directory exists or can be created by the database reader.
- That the application has permission to access the database file.
- That the database file is not locked by another process.

### Database table not found

Ensure that database initialization has been performed before inserting or retrieving test data.

### Browser or application timeout

Verify:

- Internet connectivity.
- SauceDemo availability.
- Application URL.
- Browser configuration.
- Timeout values in `config/config.yaml`.

### Behave command not recognized

Verify that the virtual environment is activated and Behave is installed:

```bash
pip install behave
```

## 15. Important Notes

- Always activate the virtual environment before running tests.
- Keep test data separate from test logic.
- Do not commit virtual environment directories.
- Do not modify Excel worksheet names or headers without updating dependent tests.
- SQLite uses Python's built-in `sqlite3` module.
- Keep database configuration consistent with the actual database file location.
- Use temporary databases for isolated database unit tests.
- Run relevant test modules after changing page objects, configuration, or data readers.
- Review test execution results before committing changes.
- Redis integration is not currently implemented.
- Refer to `test_execution.md` for detailed test execution instructions.