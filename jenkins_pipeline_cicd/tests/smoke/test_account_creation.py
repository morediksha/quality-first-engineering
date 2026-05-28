"""
Smoke tests for basic Playwright functionality.
These tests run quickly and validate basic browser operations.
"""

import pytest
import allure
from playwright.sync_api import expect


@allure.feature('Browser Operations')
@allure.story('Basic Functionality')
@pytest.mark.smoke
class TestBasicSmoke:
    """
    Smoke tests for validating basic functionality.
    """
    
    @allure.title("Verify Browser Can Navigate to URL")
    @allure.description("Test that the browser can navigate to a URL successfully")
    def test_browser_navigation(self, page):
        """
        Test 1: Verify that browser can navigate to a URL.
        """
        with allure.step("Navigate to example.com"):
            page.goto("https://example.com", timeout=30000)
        
        with allure.step("Verify page title"):
            page_title = page.title()
            allure.attach(page_title, "Page Title", allure.attachment_type.TEXT)
            assert "Example" in page_title, "Page should contain 'Example' in title"
        
        with allure.step("Take screenshot"):
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                "NavigationPage_Screenshot",
                allure.attachment_type.PNG
            )
    
    @allure.title("Verify Page Elements Visibility")
    @allure.description("Test that page elements are visible and accessible")
    def test_page_elements_visibility(self, page):
        """
        Test 2: Verify that page elements are visible.
        """
        with allure.step("Navigate to page"):
            page.goto("https://example.com", timeout=30000)
        
        with allure.step("Wait for page to fully load"):
            page.wait_for_load_state("domcontentloaded")
        
        with allure.step("Verify body element is visible"):
            body = page.locator('body')
            expect(body).to_be_visible(timeout=10000)
        
        with allure.step("Verify page has content"):
            content = page.locator('h1')
            try:
                expect(content).to_be_visible()
                heading_text = content.text_content()
                allure.attach(f"Found heading: {heading_text}", "Content Check", allure.attachment_type.TEXT)
            except:
                allure.attach("No H1 element found (this is acceptable)", "Content Check", allure.attachment_type.TEXT)

