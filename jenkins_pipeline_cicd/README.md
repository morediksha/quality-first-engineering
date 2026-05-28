# Jenkins Pipeline with Playwright - CI/CD Testing

A complete Jenkins CI/CD pipeline integrated with Playwright for automated testing of newly created accounts with Allure reporting.

## Project Structure

```
.
├── Jenkinsfile                          # Jenkins pipeline definition
├── conftest.py                          # Pytest configuration with fixtures & Allure integration
├── pytest.ini                           # Pytest settings
├── requirements.txt                     # Python dependencies
├── squad_urls.txt                       # Account URLs for testing (one per line)
├── tests/
│   ├── __init__.py
│   ├── smoke/
│   │   ├── __init__.py
│   │   └── test_account_creation.py     # 2 smoke tests
│   └── regression/
│       ├── __init__.py
│       └── test_account_validation.py   # 2 regression tests
├── scripts/
│   └── account_handler.py               # Account validation utility
├── allure-results/                      # Allure test results (generated)
├── allure-reports/                      # Allure HTML reports (generated)
└── reports/                             # HTML test reports (generated)
```

## Features

✅ **Playwright Integration** - Browser automation for account testing
✅ **Allure Reports** - Beautiful, detailed test reports
✅ **Parametrized Testing** - Run tests against multiple newly created accounts
✅ **Input Parameters** - Branch, tests path, squad URL file selection
✅ **Account Validation** - Verify account accessibility before testing
✅ **HTML Reports** - Self-contained HTML test reports
✅ **Parallel Execution** - Tests run in parallel using pytest-xdist
✅ **No Docker Required** - Runs directly on Jenkins agent

## Setup Instructions

### 1. Prerequisites

- Python 3.7+
- Jenkins installed and configured
- Git repository with this code
- Newly created squad account URLs

### 2. Initial Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd jenkins_pipeline_cicd

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Configure Squad Account URLs

Edit [squad_urls.txt](squad_urls.txt) and add your newly created account URLs:

```
https://squad-dev.example.com/account/new-001
https://squad-dev.example.com/account/new-002
https://squad-dev.example.com/account/new-003
```

### 4. Configure Jenkins

#### Create a New Pipeline Job

1. **Jenkins Dashboard** → **New Item**
2. **Enter item name** → Select **Pipeline** → **OK**
3. **Pipeline** section → Select **Pipeline script from SCM**
4. **SCM**: Git
5. **Repository URL**: Your git repository URL
6. **Script Path**: `Jenkinsfile`

#### Configure Build Parameters

The pipeline automatically creates these parameters:

- **BRANCH**: Git branch to checkout (default: `main`)
- **TESTS_PATH**: Path to test files (default: `tests/smoke`)
  - Options: `tests/smoke`, `tests/regression`, or `tests` (all)
- **SQUAD_URL_FILE**: File with account URLs (default: `squad_urls.txt`)
- **HEADLESS_MODE**: Run in headless mode (default: `true`)

## Running Tests

### Locally (Development)

```bash
# Run smoke tests
pytest tests/smoke -v --alluredir=allure-results

# Run regression tests
pytest tests/regression -v --alluredir=allure-results

# Run all tests
pytest tests -v --alluredir=allure-results

# Generate Allure report
allure generate allure-results -o allure-reports
allure open allure-reports
```

### Via Jenkins

1. **Jenkins Dashboard** → Click your pipeline job
2. **Build with Parameters**
3. **Configure parameters**:
   - BRANCH: Select branch
   - TESTS_PATH: Select test suite
   - SQUAD_URL_FILE: Confirm file name
   - HEADLESS_MODE: Check for headless
4. **Build**

## Viewing Reports

### Allure Reports (Recommended)

After pipeline completes:
1. **Jenkins Build page** → **Allure Report** (published automatically)
2. View detailed test results with screenshots

### HTML Reports

- Location: `allure-reports/index.html`
- Also available in: `reports/report.html`

## Test Cases

### Smoke Tests (tests/smoke/test_account_creation.py)

1. **test_account_login_page_loads**
   - Verifies account login page loads successfully
   - Checks page title and basic structure
   - Captures screenshot of loaded page

2. **test_account_url_accessibility**
   - Validates HTTP response status (200-299)
   - Verifies page content is not empty
   - Reports content size

### Regression Tests (tests/regression/test_account_validation.py)

1. **test_account_page_elements**
   - Validates HTML structure (html, body tags)
   - Counts visible elements
   - Tests page interactivity

2. **test_account_response_time**
   - Measures page load time
   - Validates against 10-second threshold
   - Verifies content is fully rendered

## Account Handler Utility

Pre-validate accounts before running tests:

```bash
# Validate all accounts
python scripts/account_handler.py --validate

# Custom squad file
python scripts/account_handler.py --squad-file custom_urls.txt --validate

# Generate report only
python scripts/account_handler.py --report account_status.json

# Set custom timeout
python scripts/account_handler.py --validate --timeout 15
```

Output: `account_validation_report.json`

## Environment Variables

The pipeline supports these environment variables:

```bash
SQUAD_URL_FILE=squad_urls.txt    # Squad URLs file location
HEADLESS_MODE=true               # Run in headless mode
ALLURE_RESULTS=allure-results    # Allure results directory
ALLURE_REPORTS=allure-reports    # Allure reports directory
```

## Troubleshooting

### Tests Not Running

```bash
# Check if squad_urls.txt exists
ls -la squad_urls.txt

# Verify test discovery
pytest tests --collect-only

# Run with verbose output
pytest tests -vv
```

### Playwright Issues

```bash
# Reinstall Playwright
pip install --upgrade playwright
playwright install chromium

# Run with debug mode
PWDEBUG=1 pytest tests
```

### Allure Report Issues

```bash
# Clear old results
rm -rf allure-results/*

# Verify allure is installed
allure --version

# Generate report manually
allure generate allure-results -o allure-reports --clean
```

### Jenkins Pipeline Failures

1. **Checkout Failed**: Verify Git credentials and branch name
2. **Setup Failed**: Check Python version and pip permissions
3. **Validation Failed**: Ensure `squad_urls.txt` exists and has valid URLs
4. **Tests Failed**: Check test paths match parameter values

## Customization

### Adding New Test Cases

1. Create test file in `tests/smoke/` or `tests/regression/`
2. Use provided fixtures: `page`, `browser_context`, `squad_accounts`
3. Add Allure decorators for reporting
4. Mark with `@pytest.mark.smoke` or `@pytest.mark.regression`

Example:

```python
@pytest.mark.smoke
@allure.title("My Test")
def test_new_feature(page, squad_accounts):
    account_url = squad_accounts[0]
    page.goto(account_url)
    # Your test logic
```

### Modifying Pipeline Stages

Edit [Jenkinsfile](Jenkinsfile):

- Add custom validation steps in `Validate Inputs` stage
- Modify test execution in `Run Tests` stage
- Add post-build actions in `post` section

### Custom Allure Environment

Edit [conftest.py](conftest.py) - `allure_environment` fixture:

```python
allure.environment(
    Browser="Chromium",
    CustomVar="Custom Value"
)
```

## Performance Optimization

### Parallel Test Execution

Tests run in parallel by default using pytest-xdist (`-n auto`).

To control parallel workers:

```bash
# Edit Jenkinsfile, Run Tests stage:
pytest tests -n 4  # Use 4 workers
```

### Headless Mode

Recommended for CI/CD (faster, no display required):

```bash
# Enabled by default in Jenkins
# Disable locally for debugging:
HEADLESS_MODE=false pytest tests
```

## Best Practices

1. **Keep squad_urls.txt Updated** - Always include newly created accounts
2. **Use Meaningful Test Names** - Helps with Allure report readability
3. **Add Allure Steps** - Provides detailed execution flow in reports
4. **Run Locally Before Push** - Test locally before committing
5. **Monitor Report Trends** - Check Allure reports for flaky tests
6. **Maintain Test Independence** - Tests should not depend on execution order

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: playwright install chromium
      - run: pytest tests --alluredir=allure-results
      - name: Publish Allure Report
        uses: simple-elf/allure-report-action@master
        if: always()
```

## Support & Documentation

- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Allure Framework](https://docs.qameteor.com/display/general/Allure+Framework)
- [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/)

## License

MIT License - Feel free to use and modify as needed.

---

**Last Updated**: 2026-05-28
