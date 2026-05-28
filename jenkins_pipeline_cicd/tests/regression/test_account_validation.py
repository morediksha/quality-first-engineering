"""
Regression tests for comprehensive Playwright testing.
These tests provide comprehensive coverage of browser functionality.
"""

import pytest
import allure
from playwright.sync_api import expect
import time


@allure.feature('Browser Testing')
@allure.story('Content Verification')
@pytest.mark.regression
class TestContentValidation:
    """
    Regression tests for validating page content and structure.
    """
    
    @allure.title("Verify Page Structure and Elements")
    @allure.description("Test that page has proper HTML structure and elements")
    def test_page_structure(self, page):
        """
        Test 1: Verify that pages have proper HTML structure.
        """
        with allure.step("Navigate to page"):
            page.goto("https://example.com", timeout=30000)
        
        with allure.step("Wait for page to fully load"):
            page.wait_for_load_state("domcontentloaded")
        
        with allure.step("Verify essential HTML elements"):
            html_element = page.locator('html')
            body_element = page.locator('body')
            
            expect(html_element).to_have_count(1)
            expect(body_element).to_have_count(1)
        
        with allure.step("Verify page has visible content"):
            visible_elements = page.locator('*:visible').count()
            allure.attach(
                f"Total visible elements: {visible_elements}",
                "Page Analysis",
                allure.attachment_type.TEXT
            )
            assert visible_elements > 0, "Page should have visible elements"
        
        with allure.step("Take screenshot"):
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                "PageStructure_Screenshot",
                allure.attachment_type.PNG
            )
    
    @allure.title("Verify Browser DOM Operations")
    @allure.description("Test that browser can perform DOM operations correctly")
    def test_browser_dom_operations(self, page):
        """
        Test 2: Verify browser DOM operations.
        """
        with allure.step("Navigate to page"):
            page.goto("https://example.com", timeout=30000)
        
        with allure.step("Retrieve page content"):
            content = page.content()
            allure.attach(f"Page size: {len(content)} bytes", "Content Info", allure.attachment_type.TEXT)
            assert len(content) > 0, "Page should have content"
        
        with allure.step("Verify page URL"):
            current_url = page.url
            allure.attach(f"Current URL: {current_url}", "URL Info", allure.attachment_type.TEXT)
            assert "example.com" in current_url, "URL should contain example.com"
        
        with allure.step("Wait briefly and verify page state"):
            time.sleep(1)
            page_title = page.title()
            assert len(page_title) > 0, "Page should have a title"
            allure.attach(f"Final page title: {page_title}", "Final State", allure.attachment_type.TEXT)

