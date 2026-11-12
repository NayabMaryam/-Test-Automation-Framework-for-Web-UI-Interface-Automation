# Setup Guide

## 1. Introduction

This guide explains how to configure and run the UI Test Automation Framework on a local computer.

The framework uses Python, Playwright, and Pytest to automate web UI testing of the SauceDemo application.

## 2. Prerequisites

Before setting up the project, install:

- Python 3.10 or later (the current project has been tested with Python 3.13.6).
- Git.
- Visual Studio Code or another code editor.
- Google Chrome or Microsoft Edge (if using those browser channels).

## 3. Clone the Repository

Open PowerShell or a terminal and execute:

```bash
git clone https://github.com/NayabMaryam/-Test-Automation-Framework-for-Web-UI-Interface-Automation.git
```

Navigate to the project directory:

```bash
cd E:\-Test-Automation-Framework-for-Web-UI-Interface-Automation
``

Replace the placeholders with your actual GitHub repository URL and folder name.

## 4. Create a Virtual Environment

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use an appropriate execution policy for your environment or activate the environment using another supported terminal.

## 5. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

## 6. Install Playwright Browsers

Install the default Playwright browsers:

```bash
python -m playwright install
```

For the additional Chrome and Edge browser channels, install the corresponding browsers if they are not already available:

```bash
python -m playwright install chrome
python -m playwright install msedge
```

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

## 8. Run the Tests

Execute the complete test suite:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_login.py -v
```

## 9. Select a Browser

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

For continuous integration, the `CI=true` environment variable enables headless browser execution.

## 10. Troubleshooting

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

## 11. Expected Result

After successful setup, Pytest should discover and execute the framework's automated tests.

The currently verified local test suite contains 13 tests.
