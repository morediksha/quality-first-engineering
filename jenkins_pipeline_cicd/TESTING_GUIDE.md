# Testing Guide

Quick reference for running tests locally and understanding the test structure.

## Test Structure

```
tests/
├── smoke/                          # Fast, basic functionality tests
│   └── test_account_creation.py    # 2 smoke test cases
└── regression/                     # Comprehensive tests
    └── test_account_validation.py  # 2 regression test cases
```

## Quick Test Execution

### Using Test Runner Script

```bash
# Run smoke tests
python3 run_tests.py --suite smoke

# Run regression tests
python3 run_tests.py --suite regression

# Run all tests
python3 run_tests.py --suite all

# Run with custom settings
python3 run_tests.py --suite smoke --headless false --workers 4

# Run verbose with no report
python3 run_tests.py --suite all -v --no-report
```

### Direct Pytest Commands

```bash
# Run smoke tests only
pytest tests/smoke -v

# Run regression tests only
pytest tests/regression -v

# Run all tests
pytest tests -v

# Run with specific markers
pytest tests -m smoke -v
pytest tests -m regression -v
pytest tests -m new_account -v

# Run specific test file
pytest tests/smoke/test_account_creation.py -v

# Run specific test
pytest tests/smoke/test_account_creation.py::TestAccountCreationSmoke::test_account_login_page_loads -v

# Run with parallel workers
pytest tests -n 4 -v

# Run with Allure
pytest tests --alluredir=allure-results -v

# Run with HTML report
pytest tests --html=reports/report.html --self-contained-html -v

# Run with short traceback
pytest tests --tb=short -v

# Run with minimal output
pytest tests -q

# Run and stop on first failure
pytest tests -x -v

# Run with timeout per test (seconds)
pytest tests --timeout=300 -v
```

## Test Execution Workflow

### 1. Smoke Tests (Quick Check)

```bash
# Fast validation of basic functionality
pytest tests/smoke -v --alluredir=allure-results

# Expected time: < 2 minutes
# Tests account page loads and accessibility
```

### 2. Regression Tests (Full Coverage)

```bash
# Comprehensive account validation
pytest tests/regression -v --alluredir=allure-results

# Expected time: 5-10 minutes
# Tests page elements and response time
```

### 3. Full Test Suite

```bash
# All tests with parallel execution
pytest tests -v -n auto --alluredir=allure-results

# Expected time: 5-10 minutes
# Complete validation
```

## Generating Reports

### Allure Reports

```bash
# Generate Allure report
allure generate allure-results -o allure-reports --clean

# Open Allure report
allure open allure-reports

# View Allure history
allure history

# Serve Allure report on custom port
allure open allure-reports --port 8080
```

### HTML Reports

```bash
# Generate HTML report
pytest tests --html=reports/report.html --self-contained-html

# View report
open reports/report.html  # macOS
# or
xdg-open reports/report.html  # Linux
# or
start reports/report.html  # Windows
```

## Test Markers

Use pytest markers to categorize and run specific tests:

```bash
# Run only smoke tests
pytest tests -m smoke

# Run only regression tests
pytest tests -m regression

# Run only new account tests
pytest tests -m new_account

# Run tests excluding smoke
pytest tests -m "not smoke"

# Run tests with multiple markers
pytest tests -m "regression and new_account"
```

## Debugging Tests

### Run with Verbose Output

```bash
# Maximum verbosity
pytest tests -vv

# Show print statements
pytest tests -v -s

# Show local variables on failure
pytest tests -vv --tb=long

# Show all available markers
pytest --markers
```

### Run with Playwright Debug

```bash
# Debug mode with inspector
PWDEBUG=1 pytest tests/smoke/test_account_creation.py::TestAccountCreationSmoke::test_account_login_page_loads -v

# Trace mode (generates trace for analysis)
PLAYWRIGHT_TRACE=1 pytest tests -v

# Slowmo mode (slow down execution)
PWSLOWMO=1000 pytest tests -v
```

### Headless Mode Control

```bash
# Run in headless mode (default)
HEADLESS_MODE=true pytest tests -v

# Run with visible browser (for debugging)
HEADLESS_MODE=false pytest tests -v
```

## CI/CD Integration

### GitHub Actions

```bash
# In your workflow
pytest tests --alluredir=allure-results

# Publish Allure report
allure generate allure-results -o allure-reports
```

### GitLab CI

```bash
# In .gitlab-ci.yml
script:
  - pytest tests --alluredir=allure-results
  - allure generate allure-results -o allure-reports
```

### Jenkins

Handled by Jenkinsfile - just build with parameters.

## Common Issues & Solutions

### Issue: "No tests found"

**Solution:**
```bash
# Verify test discovery
pytest tests --collect-only

# Check test file naming (must start with test_)
ls -la tests/*/test_*.py
```

### Issue: "squad_urls.txt not found"

**Solution:**
```bash
# Create squad_urls.txt with sample URLs
cat > squad_urls.txt << EOF
https://example.com/account/1
https://example.com/account/2
EOF
```

### Issue: "Playwright browsers not installed"

**Solution:**
```bash
# Install Chromium
playwright install chromium

# Install all browsers
playwright install
```

### Issue: "Tests run slow"

**Solution:**
```bash
# Run with more parallel workers
pytest tests -n 8 -v

# Or run specific suite only
pytest tests/smoke -v
```

### Issue: "Timeout errors"

**Solution:**
```bash
# Increase page timeout
pytest tests --timeout=600 -v

# Or in code: page.goto(url, timeout=60000)
```

## Test Output Examples

### Successful Test Run

```
tests/smoke/test_account_creation.py::TestAccountCreationSmoke::test_account_login_page_loads PASSED
tests/smoke/test_account_creation.py::TestAccountCreationSmoke::test_account_url_accessibility PASSED
tests/regression/test_account_validation.py::TestAccountValidationRegression::test_account_page_elements PASSED
tests/regression/test_account_validation.py::TestAccountValidationRegression::test_account_response_time PASSED

========================= 4 passed in 25.34s =========================
```

### Failed Test

```
tests/smoke/test_account_creation.py::TestAccountCreationSmoke::test_account_login_page_loads FAILED
...
assert 200 <= 404 < 300
ERROR: Expected 2xx status, got 404
```

## Test Configuration

### pytest.ini

Controls test discovery and execution:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers = smoke, regression, new_account
timeout = 300
```

### conftest.py

Provides fixtures and hooks:

```python
@pytest.fixture
def page(browser_context):
    """Provides a Playwright page"""
    return browser_context.new_page()

@pytest.fixture(scope="session")
def squad_accounts():
    """Loads squad account URLs"""
    return load_urls_from_file()
```

## Best Practices

1. **Run locally before pushing** - Verify tests pass locally first
2. **Use descriptive test names** - Makes reports easier to read
3. **Keep tests independent** - No test should depend on another
4. **Use fixtures** - Avoid duplicating setup code
5. **Add Allure decorators** - Improves report quality
6. **Check reports** - Review failure details in Allure
7. **Run smoke first** - Quick validation before full suite
8. **Maintain test data** - Keep squad_urls.txt updated

## Test Metrics

### Expected Execution Times

- **Smoke Tests**: 1-2 minutes
- **Regression Tests**: 5-10 minutes
- **Full Suite**: 8-12 minutes
- **With Parallel (4 workers)**: 3-6 minutes

### Expected Success Rate

- **Healthy Run**: 95-100% pass rate
- **Investigation Needed**: < 90% pass rate
- **Blocking Issue**: 0% pass rate

## Continuous Monitoring

```bash
# Watch tests on every change
pytest-watch tests -- -v

# Or use:
ptw tests -- -v

# Run specific suite on change
ptw tests/smoke -- -v --alluredir=allure-results
```

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Python Docs](https://playwright.dev/python/)
- [Allure Documentation](https://docs.qameteor.com/display/general/Allure+Framework)
- [pytest-xdist (Parallel Execution)](https://pytest-xdist.readthedocs.io/)
- [pytest-html (HTML Reports)](https://pytest-html.readthedocs.io/)

---

For more help: `pytest --help`
