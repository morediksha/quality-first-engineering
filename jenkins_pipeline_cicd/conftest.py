import pytest
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# FIXTURES FOR PLAYWRIGHT TESTING
# ============================================================================

@pytest.fixture(scope="session")
def headless_mode():
    """
    Determine if browser should run in headless mode.
    Can be controlled via environment variable HEADLESS_MODE.
    """
    return os.getenv('HEADLESS_MODE', 'true').lower() == 'true'


@pytest.fixture
def browser_context(headless_mode):
    """
    Create and provide a browser context for testing.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless_mode)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(browser_context):
    """
    Create and provide a page within the browser context.
    """
    page = browser_context.new_page()
    yield page
    page.close()


# ============================================================================
# TEST MARKERS CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """
    Configure pytest with custom markers.
    """
    config.addinivalue_line(
        "markers",
        "smoke: Mark test as a smoke test (fast, basic functionality checks)"
    )
    config.addinivalue_line(
        "markers",
        "regression: Mark test as a regression test (comprehensive checks)"
    )



    """
    Hook to capture test execution details for Allure reporting.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        import allure
        
        # Add test ID to Allure report
        allure.dynamic.id(f"{item.nodeid}")
        
        # Add markers as labels
        for marker in item.iter_markers():
            allure.dynamic.label(marker.name, marker.args[0] if marker.args else "")


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to ensure proper categorization.
    """
    for item in items:
        # Auto-mark tests based on file path
        if "smoke" in str(item.fspath):
            item.add_marker(pytest.mark.smoke)
        if "regression" in str(item.fspath):
            item.add_marker(pytest.mark.regression)
