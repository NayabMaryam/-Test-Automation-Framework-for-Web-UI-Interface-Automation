# Setup and Installation Guide

## 1. Introduction

This guide explains how to configure and run the automated web UI testing framework.

The framework uses Python, Playwright, Pytest, Behave, and OpenPyXL to automate and validate the SauceDemo application.

Application under test:

https://www.saucedemo.com/

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

After activation, the terminal should display the environment name:

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

The framework uses the following main directories:

```text
project/
│
├── config/
│   └── config.yaml
│
├── src/
│   ├── core/
│   │   ├── browser_manager.py
│   │   └── config_reader.py
│   │
│   ├── data/
│   │   └── excel_reader.py
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

This is a representation of the main framework components. Additional project files may exist.

## 8. Configure the Application

Open:

`config/config.yaml`

Verify that the application URL and browser settings are configured correctly.

The application under test is:

```text
https://www.saucedemo.com/
```

The configuration file also manages browser selection, headless execution, and timeout settings.

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

## 10. Verify Excel Integration

Execute the Excel reader tests:

```bash
pytest tests/test_excel_reader.py -v
```

These tests validate:

- Reading login data.
- Reading all login records.
- Missing workbook handling.
- Missing worksheet handling.
- Duplicate header validation.

## 11. Verify Framework Installation

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

## 12. Run the Framework

Execute the complete Pytest suite:

```bash
pytest -v
```

Execute BDD tests:

```bash
behave
```

Refer to `test_execution.md` for detailed execution commands and reporting instructions.

## 13. Troubleshooting

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

## 14. Important Notes

- Always activate the virtual environment before running tests.
- Keep test data separate from test logic.
- Do not commit virtual environment directories.
- Do not modify Excel worksheet names or headers without updating dependent tests.
- Run the relevant test modules after changing page objects or test data.
- Review the test execution results before committing changes.