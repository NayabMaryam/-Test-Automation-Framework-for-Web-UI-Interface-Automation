# UI Test Automation Framework

## 1. Project Overview

The UI Test Automation Framework is a Python-based web UI automation solution developed using Playwright and Pytest.

The framework automates testing of the [SauceDemo](https://www.saucedemo.com/) web application. It follows the Page Object Model (POM) design pattern to improve code reusability, maintainability, and separation of test logic from page interactions.

The current implementation provides browser management, configuration handling, reusable page objects, automated UI test cases, and cross-browser execution through GitHub Actions.

## 2. Implemented Features

- Browser management using Playwright.
- Support for Chromium, Google Chrome, and Microsoft Edge.
- Centralized YAML-based configuration.
- Environment variable overrides for CI execution.
- Pytest fixtures for browser, page, and configuration management.
- Page Object Model (POM).
- Login and Inventory page automation.
- Automated UI test scenarios.
- Cross-browser testing using GitHub Actions.
- Automated test execution on pushes and pull requests to the main branch.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Playwright | Browser automation |
| Pytest | Test execution and fixtures |
| PyYAML | YAML configuration handling |
| Git and GitHub | Version control and collaboration |
| GitHub Actions | Continuous Integration |

## 4. Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── automation.yml
├── config/
│   └── config.yaml
├── docs/
│   ├── architecture.md
│   ├── setup_guide.md
│   └── test_execution.md
├── src/
│   ├── core/
│   ├── data/
│   ├── pages/
│   └── utilities/
├── tests/
├── test_data/
├── features/
├── report/
├── screenshots/
├── pytest.ini
├── requirements.txt
└── README.md
```

Some directories and files are reserved for planned framework extensions and are not fully implemented in the current version.

## 5. Application Under Test

**Application:** SauceDemo

**URL:** https://www.saucedemo.com/

The framework currently focuses on login and inventory-related UI automation.

## 6. Cross-Browser Testing

The framework supports the following browsers:

- Chromium
- Google Chrome
- Microsoft Edge

GitHub Actions executes the automated test suite using a browser matrix, allowing the same tests to run across all three browsers.

## 7. Test Execution

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
python -m playwright install
```

Run the complete test suite:

```bash
pytest -v
```

Run tests using a specific browser:

```powershell
$env:BROWSER = "edge"
pytest -v
```

For Google Chrome:

```powershell
$env:BROWSER = "chrome"
pytest -v
```

For Chromium:

```powershell
$env:BROWSER = "chromium"
pytest -v
```

## 8. Continuous Integration

GitHub Actions automatically executes tests when code is pushed to the main branch or a pull request targets the main branch.

The workflow uses a browser matrix containing Chromium, Chrome, and Edge.

## 9. Current Test Results

The current local test suite contains 13 passing tests.

Cross-browser execution has also been verified successfully through GitHub Actions.

## 10. Planned Extensions

The following components are present in the project structure but are not yet implemented or verified as functional:

- BDD and Gherkin-based testing.
- Excel-based test data integration.
- Database integration.
- Redis integration.
- Logging utilities.
- Helper utilities.
- Allure reporting.
- Automatic screenshot capture on test failure.

These features may be added in future development milestones.

## 11. Team Responsibilities

**Member 1 — Framework and Automation**
- Browser management.
- Configuration management.
- Pytest fixtures.
- Base Page and Page Object Model.
- Login and Inventory automation.
- GitHub Actions and cross-browser testing.

**Member 2 — Framework Extensions**
- BDD and Gherkin integration.
- Data-driven testing.
- Additional page objects.
- Excel, Database, and Redis integration.
- Reporting and logging.

## 12. Project Status

The core UI automation framework and cross-browser CI pipeline have been implemented and tested. Additional framework extensions remain pending.