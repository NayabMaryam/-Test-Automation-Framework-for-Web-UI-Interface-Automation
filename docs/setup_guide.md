# Setup Guide

## 1. Introduction

This guide explains how to configure and run the UI Test Automation Framework on a local computer.

The framework uses Python, Playwright, Pytest, and Behave to automate web UI testing of the SauceDemo application.

It supports two testing approaches:

- **Pytest:** Executes conventional automated test cases.
- **Behave:** Executes Behavior-Driven Development (BDD) scenarios written in Gherkin syntax.

## 2. Prerequisites

Before setting up the project, install:

- Python 3.10 or later (locally verified with Python 3.12.9).
- Git.
- Visual Studio Code or another code editor.
- Google Chrome or Microsoft Edge (if using those browser channels).

## 3. Clone the Repository

Open PowerShell or a terminal and execute:

```bash
git clone https://github.com/NayabMaryam/-Test-Automation-Framework-for-Web-UI-Interface-Automation.git
```

Navigate to the cloned project directory:

```powershell
cd -Test-Automation-Framework-for-Web-UI-Interface-Automation
```

Alternatively, open the cloned repository directly in Visual Studio Code.

## 4. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use an appropriate execution policy for your environment or activate the environment using another supported terminal.

After activation, the terminal should display the virtual environment name:

```text
(.venv)
```

## 5. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

The project dependencies include the libraries required for:

- Playwright browser automation.
- Pytest test execution.
- Behave BDD execution.
- Configuration and other framework utilities.

## 6. Install Playwright Browsers

Install the default Playwright browsers:

```bash
python -m playwright install
```

For additional Chrome and Edge browser channels, install the corresponding browsers if they are not already available:

```bash
python -m playwright install chrome
python -m playwright install msedge
```

The default browser configuration uses Chromium.

## 7. Configuration

The framework configuration is stored in:

`config/config.yaml`

The current configuration contains:

| Setting | Description |
|---|---|
| application.name | Application name |
| application.base_url | SauceDemo application URL |
| browser.name | Selected browser |
| browser.headless | Headless execution setting |
| browser.slow_mo | Browser action delay |
| timeouts.default | Default page operation timeout |
| timeouts.navigation | Navigation timeout |
| test.screenshot_on_failure | Screenshot configuration flag |

The default browser is Chromium.

Environment variables can override supported browser settings.

## 8. Run Pytest Tests

Execute the complete Pytest test suite:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_login.py -v
```

The Pytest suite covers framework components, browser management, configuration, login, and inventory functionality.

## 9. Run Behave BDD Tests

The framework uses Behave to execute Gherkin feature files.

The BDD features are located in:

```text
features/
    login.feature
    inventory.feature
    cart.feature
    steps/
        login_steps.py
        inventory_steps.py
        cart_steps.py
    environment.py
```

**Execute all BDD features:**

```bash
behave
```

**Execute a specific feature:**

Login:

```bash
behave features/login.feature
```

Inventory:

```bash
behave features/inventory.feature
```

Shopping Cart:

```bash
behave features/cart.feature
```

**Execute a feature with pretty output:**

```bash
behave features/cart.feature --format=pretty
```

**Validate step-definition matching without executing scenarios:**

```bash
behave --dry-run features/cart.feature
```

Note: Dry-run validates step matching but does not execute the actual browser interactions or test assertions.

## 10. Select a Browser

The browser can be selected using the `BROWSER` environment variable.

**Chromium:**

```powershell
$env:BROWSER = "chromium"
pytest -v
```

**Google Chrome:**

```powershell
$env:BROWSER = "chrome"
pytest -v
```

**Microsoft Edge:**

```powershell
$env:BROWSER = "edge"
pytest -v
```

For continuous integration, the `CI=true` environment variable enables headless browser execution, as configured in the framework.

## 11. Troubleshooting

**Problem: Playwright browser executable not found**

Solution:

```bash
python -m playwright install
```

**Problem: Python dependency not found**

Solution:

```bash
pip install -r requirements.txt
```

**Problem: Virtual environment is not activated**

Solution:

```powershell
.venv\Scripts\Activate.ps1
```

**Problem: Browser channel is unavailable**

Solution:

Install the corresponding Chrome or Edge browser channel and verify that the browser is installed.

**Problem: Behave command is not recognized**

Solution:

Verify that Behave is installed in the active virtual environment:

```bash
pip show behave
```

If it is missing, install the project dependencies again:

```bash
pip install -r requirements.txt
```

**Problem: Undefined steps in Behave**

Solution:

- Verify that the relevant step definitions exist in `features/steps/`.
- Check that the Gherkin steps match their corresponding step definitions.
- Validate step matching using:

```bash
behave --dry-run
```

## 12. Expected Results

After successful setup, both Pytest and Behave should discover and execute their respective automated tests.

The latest locally verified results are:

**Pytest:**
- 12 tests passed.
- 0 tests failed.

**Behave:**
- 3 features passed.
- 16 scenarios passed.
- 65 steps passed.
- 0 scenarios failed.

The Cart feature was also independently verified:

- 1 feature passed.
- 5 scenarios passed.
- 29 steps passed.

These results represent the current verified implementation and may change as additional features and integrations are developed.