# 🚀 Quick Start Guide

Get the Jenkins Playwright pipeline up and running in 5 minutes!

## ✅ Prerequisites

- Python 3.7+ installed
- Git installed  
- Jenkins 2.235+ (for CI/CD part)
- macOS/Linux/Windows

## 📋 Step 1: Initial Setup (2 minutes)

### On macOS/Linux:

```bash
# Navigate to project directory
cd jenkins_pipeline_cicd

# Run setup script
bash scripts/setup.sh
```

### On Windows:

```bash
# Run setup script
scripts\setup.bat
```

The setup script will:
- ✓ Check Python installation
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Install Playwright browsers
- ✓ Verify test discovery
- ✓ Create squad_urls.txt template

## 🔗 Step 2: Add Account URLs (1 minute)

Edit `squad_urls.txt` and add your newly created account URLs:

```
https://your-squad-domain.com/account/new-001
https://your-squad-domain.com/account/new-002
https://your-squad-domain.com/account/new-003
```

**One URL per line** - no empty lines

## 🧪 Step 3: Run Tests Locally (1 minute)

### Option A: Using Test Runner (Recommended)

```bash
# Activate virtual environment first
source venv/bin/activate

# Run smoke tests
python3 run_tests.py --suite smoke

# Run regression tests
python3 run_tests.py --suite regression

# Run all tests
python3 run_tests.py --suite all
```

### Option B: Direct pytest

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
pytest tests/smoke -v --alluredir=allure-results
```

## 📊 Step 4: View Reports (1 minute)

### Allure Report (Beautiful Format)

```bash
# Generate Allure report
allure generate allure-results -o allure-reports --clean

# Open in browser
allure open allure-reports
```

### HTML Report (Simple Format)

```bash
# Already generated during test run
# Open: reports/report.html
open reports/report.html
```

## 🔧 Step 5: Configure Jenkins (Optional - 3 minutes)

### Create Pipeline Job in Jenkins

1. **Jenkins Dashboard** → **+ New Item**
2. **Name**: `squad-playwright-tests`
3. **Type**: **Pipeline** → **OK**
4. **Pipeline** → **Pipeline script from SCM**
5. **SCM**: Git
6. **Repository URL**: Your Git repo URL
7. **Script Path**: `Jenkinsfile`
8. **Save**

### Build with Parameters

1. Click **Build with Parameters**
2. Configure:
   - **BRANCH**: `main` (or your branch)
   - **TESTS_PATH**: `tests/smoke` (or `tests/regression` or `tests`)
   - **SQUAD_URL_FILE**: `squad_urls.txt`
   - **HEADLESS_MODE**: ✓ Checked
3. **Build** and watch console output

## 📁 What Was Created

```
jenkins_pipeline_cicd/
├── Jenkinsfile                          # Jenkins pipeline definition
├── conftest.py                          # Pytest fixtures & Allure config
├── pytest.ini                           # Pytest settings
├── requirements.txt                     # Python dependencies
├── squad_urls.txt                       # ⭐ ADD YOUR URLS HERE
├── run_tests.py                         # Test runner script
├── README.md                            # Full documentation
├── QUICKSTART.md                        # This file
├── TESTING_GUIDE.md                     # Detailed testing guide
├── JENKINS_SETUP.md                     # Jenkins configuration guide
├── tests/
│   ├── smoke/
│   │   └── test_account_creation.py     # 2 smoke tests
│   └── regression/
│       └── test_account_validation.py   # 2 regression tests
├── scripts/
│   ├── setup.sh                         # Setup script (macOS/Linux)
│   ├── setup.bat                        # Setup script (Windows)
│   └── account_handler.py               # Account validation utility
├── allure-results/                      # Test results (generated)
├── allure-reports/                      # HTML reports (generated)
└── reports/                             # HTML test reports (generated)
```

## 🧪 Test Cases Overview

### Smoke Tests (tests/smoke/)
Fast validation for newly created accounts:

**Test 1**: `test_account_login_page_loads`
- Verifies page loads successfully
- Checks page title
- Validates page structure
- Screenshots the page

**Test 2**: `test_account_url_accessibility`  
- Validates HTTP response (200-299)
- Verifies page content exists
- Reports response status

### Regression Tests (tests/regression/)
Comprehensive account validation:

**Test 1**: `test_account_page_elements`
- Validates HTML structure
- Counts visible elements
- Tests interactivity

**Test 2**: `test_account_response_time`
- Measures page load time
- Validates < 10s threshold
- Screenshots final state

## 💡 Common Commands

```bash
# Activate environment
source venv/bin/activate

# Run smoke tests only
pytest tests/smoke -v

# Run regression tests only
pytest tests/regression -v

# Run all tests
pytest tests -v

# Run with Allure reporting
pytest tests --alluredir=allure-results -v

# Run tests in parallel (faster)
pytest tests -n auto -v

# Generate Allure report
allure generate allure-results -o allure-reports --clean

# View Allure report
allure open allure-reports

# Validate account URLs
python3 scripts/account_handler.py --validate

# Stop tests on first failure
pytest tests -x -v

# Run with verbose output
pytest tests -vv

# Run specific test file
pytest tests/smoke/test_account_creation.py -v

# Run specific test
pytest tests/smoke/test_account_creation.py::TestAccountCreationSmoke::test_account_login_page_loads -v
```

## ⚡ Pipeline Stages (Jenkins)

When you build the pipeline in Jenkins, it runs these stages:

1. **Checkout** - Gets code from Git branch
2. **Setup** - Creates venv & installs dependencies
3. **Validate Inputs** - Checks parameters and URLs file
4. **Clean Reports** - Removes old test results
5. **Run Tests** - Executes Playwright tests
6. **Generate Allure Reports** - Creates HTML reports
7. **Post Actions** - Archives results & publishes reports

## 🎯 Next Steps

### For Local Testing:
- [ ] Run `bash scripts/setup.sh` (or .bat on Windows)
- [ ] Add URLs to `squad_urls.txt`
- [ ] Run `python3 run_tests.py --suite smoke`
- [ ] View reports with `allure open allure-reports`

### For Jenkins Integration:
- [ ] Review [JENKINS_SETUP.md](JENKINS_SETUP.md) for detailed setup
- [ ] Create Jenkins pipeline job
- [ ] Configure Git credentials
- [ ] Add Jenkins plugins (Allure, Git, etc.)
- [ ] Build with parameters

### For Custom Testing:
- [ ] Check [TESTING_GUIDE.md](TESTING_GUIDE.md) for advanced options
- [ ] Read [README.md](README.md) for full documentation
- [ ] Modify tests in `tests/smoke/` and `tests/regression/`

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Complete project documentation |
| [QUICKSTART.md](QUICKSTART.md) | This quick start guide |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | Detailed testing instructions |
| [JENKINS_SETUP.md](JENKINS_SETUP.md) | Jenkins configuration guide |

## 🐛 Troubleshooting

### Issue: "Python command not found"
```bash
# Use python3 explicitly
python3 run_tests.py --suite smoke
```

### Issue: "No module named pytest"
```bash
# Activate virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "squad_urls.txt not found"
```bash
# Create it with your URLs
echo "https://your-url.com/account/1" > squad_urls.txt
```

### Issue: "playwright command not found"
```bash
# Install Playwright
pip install playwright
playwright install chromium
```

### Issue: "Permission denied on setup.sh"
```bash
# Make script executable
chmod +x scripts/setup.sh
bash scripts/setup.sh
```

### Issue: "Tests timeout or fail"
- Verify URLs in `squad_urls.txt` are correct and accessible
- Check network connectivity
- Increase timeout: `pytest tests --timeout=600 -v`
- Run with visible browser: `HEADLESS_MODE=false pytest tests -v`

## 🔗 Useful Links

- [Playwright Docs](https://playwright.dev/python/)
- [Pytest Docs](https://docs.pytest.org/)
- [Allure Framework](https://docs.qameteor.com/display/general/Allure+Framework)
- [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/)

## 📝 Quick Tips

✅ **Keep squad_urls.txt updated** - Always include recently created accounts

✅ **Run smoke first** - Quick check before regression tests (< 2 min vs 10 min)

✅ **Check reports** - Allure reports have detailed step-by-step breakdown

✅ **Use markers** - Run specific test types: `pytest -m smoke`

✅ **Parallel execution** - Speeds up test runs significantly: `-n auto`

✅ **Monitor logs** - Jenkins console output shows everything

## 🚦 Test Results Summary

After running tests, you'll see:

```
========================= 4 passed in 25.34s =========================

✅ Allure report generated successfully!
📊 Report location: allure-reports/index.html
```

- View detailed reports with screenshots and timings
- Check failure reasons with full stack traces  
- Monitor test trends over time
- Download evidence files

## 📞 Support

For issues or questions:

1. Check **Troubleshooting** section above
2. Review [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed commands
3. Check [JENKINS_SETUP.md](JENKINS_SETUP.md) for Jenkins issues
4. See [README.md](README.md) for complete documentation

---

**That's it! You're ready to go. 🎉**

Start with: `bash scripts/setup.sh` then `python3 run_tests.py --suite smoke`
