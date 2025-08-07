"""
Assertion Keywords for PyTestSuite Pro

This module provides high-level assertion keywords that combine
web actions with assertion logic for comprehensive validations.
"""

import logging
from typing import Any, List, Dict, Optional, Union
from selenium.webdriver.common.by import By

from core import assertion_manager, AssertionLevel
from .web_actions import WebActions
from .api_actions import APIActions


class AssertionKeywords:
    """High-level assertion keywords combining actions with validations"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.web_actions = WebActions()
        self.api_actions = APIActions()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for assertion keywords"""
        logger = logging.getLogger('AssertionKeywords')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    # Web Element Assertion Keywords
    def assert_element_text(self, locator: tuple, expected_text: str, 
                           level: AssertionLevel = AssertionLevel.HARD, timeout: int = 10):
        """
        Assert element text matches expected value
        
        Args:
            locator: Element locator tuple
            expected_text: Expected text content
            level: Assertion level (HARD, SOFT, WARNING)
            timeout: Wait timeout in seconds
        """
        self.logger.info(f"Asserting element text: {locator} = '{expected_text}'")
        
        try:
            actual_text = self.web_actions.get_element_text(locator, timeout)
            
            if level == AssertionLevel.HARD:
                assertion_manager.assert_equals(actual_text, expected_text, 
                                              f"Element text mismatch at {locator}")
            elif level == AssertionLevel.SOFT:
                assertion_manager.assert_equals(actual_text, expected_text, 
                                              f"Element text mismatch at {locator}", level)
            else:
                assertion_manager.warning_assert(actual_text == expected_text, 
                                                f"Element text mismatch at {locator}")
        
        except Exception as e:
            error_msg = f"Failed to get element text for assertion: {str(e)}"
            self.logger.error(error_msg)
            
            if level == AssertionLevel.HARD:
                assertion_manager.hard_assert(False, error_msg)
            elif level == AssertionLevel.SOFT:
                assertion_manager.soft_assert(False, error_msg)
            else:
                assertion_manager.warning_assert(False, error_msg)
    
    def assert_element_visible(self, locator: tuple, 
                              level: AssertionLevel = AssertionLevel.HARD, timeout: int = 10):
        """
        Assert element is visible on page
        
        Args:
            locator: Element locator tuple
            level: Assertion level (HARD, SOFT, WARNING)
            timeout: Wait timeout in seconds
        """
        self.logger.info(f"Asserting element visible: {locator}")
        
        is_visible = self.web_actions.wait_for_element_visible(locator, timeout)
        
        if level == AssertionLevel.HARD:
            assertion_manager.hard_assert(is_visible, f"Element should be visible: {locator}")
        elif level == AssertionLevel.SOFT:
            assertion_manager.soft_assert(is_visible, f"Element should be visible: {locator}")
        else:
            assertion_manager.warning_assert(is_visible, f"Element should be visible: {locator}")
    
    def assert_element_not_visible(self, locator: tuple, 
                                  level: AssertionLevel = AssertionLevel.HARD, timeout: int = 10):
        """
        Assert element is not visible on page
        
        Args:
            locator: Element locator tuple
            level: Assertion level (HARD, SOFT, WARNING)
            timeout: Wait timeout in seconds
        """
        self.logger.info(f"Asserting element not visible: {locator}")
        
        is_invisible = self.web_actions.wait_for_element_invisible(locator, timeout)
        
        if level == AssertionLevel.HARD:
            assertion_manager.hard_assert(is_invisible, f"Element should not be visible: {locator}")
        elif level == AssertionLevel.SOFT:
            assertion_manager.soft_assert(is_invisible, f"Element should not be visible: {locator}")
        else:
            assertion_manager.warning_assert(is_invisible, f"Element should not be visible: {locator}")
    
    def assert_element_present(self, locator: tuple, 
                              level: AssertionLevel = AssertionLevel.HARD):
        """
        Assert element is present in DOM
        
        Args:
            locator: Element locator tuple
            level: Assertion level (HARD, SOFT, WARNING)
        """
        self.logger.info(f"Asserting element present: {locator}")
        
        is_present = self.web_actions.is_element_present(locator)
        
        if level == AssertionLevel.HARD:
            assertion_manager.hard_assert(is_present, f"Element should be present: {locator}")
        elif level == AssertionLevel.SOFT:
            assertion_manager.soft_assert(is_present, f"Element should be present: {locator}")
        else:
            assertion_manager.warning_assert(is_present, f"Element should be present: {locator}")
    
    def assert_element_attribute(self, locator: tuple, attribute: str, expected_value: str,
                                level: AssertionLevel = AssertionLevel.HARD, timeout: int = 10):
        """
        Assert element attribute has expected value
        
        Args:
            locator: Element locator tuple
            attribute: Attribute name
            expected_value: Expected attribute value
            level: Assertion level (HARD, SOFT, WARNING)
            timeout: Wait timeout in seconds
        """
        self.logger.info(f"Asserting element attribute: {locator}[{attribute}] = '{expected_value}'")
        
        try:
            actual_value = self.web_actions.get_element_attribute(locator, attribute, timeout)
            
            if level == AssertionLevel.HARD:
                assertion_manager.assert_equals(actual_value, expected_value,
                                              f"Element attribute '{attribute}' mismatch at {locator}")
            elif level == AssertionLevel.SOFT:
                assertion_manager.assert_equals(actual_value, expected_value,
                                              f"Element attribute '{attribute}' mismatch at {locator}", level)
            else:
                assertion_manager.warning_assert(actual_value == expected_value,
                                                f"Element attribute '{attribute}' mismatch at {locator}")
        
        except Exception as e:
            error_msg = f"Failed to get element attribute for assertion: {str(e)}"
            self.logger.error(error_msg)
            
            if level == AssertionLevel.HARD:
                assertion_manager.hard_assert(False, error_msg)
            elif level == AssertionLevel.SOFT:
                assertion_manager.soft_assert(False, error_msg)
            else:
                assertion_manager.warning_assert(False, error_msg)
    
    # Page-level Assertion Keywords
    def assert_page_title(self, expected_title: str, 
                         level: AssertionLevel = AssertionLevel.HARD):
        """
        Assert page title matches expected value
        
        Args:
            expected_title: Expected page title
            level: Assertion level (HARD, SOFT, WARNING)
        """
        self.logger.info(f"Asserting page title: '{expected_title}'")
        
        actual_title = self.web_actions.get_page_title()
        
        if level == AssertionLevel.HARD:
            assertion_manager.assert_equals(actual_title, expected_title, "Page title mismatch")
        elif level == AssertionLevel.SOFT:
            assertion_manager.assert_equals(actual_title, expected_title, "Page title mismatch", level)
        else:
            assertion_manager.warning_assert(actual_title == expected_title, "Page title mismatch")
    
    def assert_page_url_contains(self, expected_url_part: str,
                                level: AssertionLevel = AssertionLevel.HARD):
        """
        Assert current URL contains expected part
        
        Args:
            expected_url_part: Expected URL substring
            level: Assertion level (HARD, SOFT, WARNING)
        """
        self.logger.info(f"Asserting URL contains: '{expected_url_part}'")
        
        current_url = self.web_actions.get_current_url()
        
        if level == AssertionLevel.HARD:
            assertion_manager.assert_contains(current_url, expected_url_part, 
                                            f"URL should contain '{expected_url_part}'")
        elif level == AssertionLevel.SOFT:
            assertion_manager.assert_contains(current_url, expected_url_part,
                                            f"URL should contain '{expected_url_part}'", level)
        else:
            assertion_manager.warning_assert(expected_url_part in current_url,
                                           f"URL should contain '{expected_url_part}'")
    
    def assert_page_loaded_successfully(self, level: AssertionLevel = AssertionLevel.HARD):
        """
        Assert page loaded successfully (basic checks)
        
        Args:
            level: Assertion level (HARD, SOFT, WARNING)
        """
        self.logger.info("Asserting page loaded successfully")
        
        # Check that page title is not empty
        title = self.web_actions.get_page_title()
        title_check = bool(title.strip())
        
        # Check that URL is valid
        url = self.web_actions.get_current_url()
        url_check = url.startswith(('http://', 'https://'))
        
        # Check that page source is not empty
        page_source = self.web_actions.get_page_source()
        source_check = len(page_source) > 100  # Basic check for substantial content
        
        overall_success = title_check and url_check and source_check
        
        if level == AssertionLevel.HARD:
            assertion_manager.hard_assert(overall_success, "Page should load successfully")
        elif level == AssertionLevel.SOFT:
            assertion_manager.soft_assert(overall_success, "Page should load successfully")
        else:
            assertion_manager.warning_assert(overall_success, "Page should load successfully")
    
    # API Assertion Keywords
    def assert_api_status_code(self, expected_status: int, response=None,
                              level: AssertionLevel = AssertionLevel.HARD):
        """
        Assert API response status code
        
        Args:
            expected_status: Expected HTTP status code
            response: Response object (uses last response if None)
            level: Assertion level (HARD, SOFT, WARNING)
        """
        self.logger.info(f"Asserting API status code: {expected_status}")
        
        actual_status = self.api_actions.get_response_status_code(response)
        
        if level == AssertionLevel.HARD:
            assertion_manager.assert_equals(actual_status, expected_status, 
                                          f"API status code should be {expected_status}")
        elif level == AssertionLevel.SOFT:
            assertion_manager.assert_equals(actual_status, expected_status,
                                          f"API status code should be {expected_status}", level)
        else:
            assertion_manager.warning_assert(actual_status == expected_status,
                                           f"API status code should be {expected_status}")
    
    def assert_api_response_contains(self, expected_text: str, response=None,
                                    level: AssertionLevel = AssertionLevel.HARD):
        """
        Assert API response contains expected text
        
        Args:
            expected_text: Expected text in response
            response: Response object (uses last response if None)
            level: Assertion level (HARD, SOFT, WARNING)
        """
        self.logger.info(f"Asserting API response contains: '{expected_text}'")
        
        response_text = self.api_actions.get_response_text(response)
        
        if level == AssertionLevel.HARD:
            assertion_manager.assert_contains(response_text, expected_text,
                                            f"API response should contain '{expected_text}'")
        elif level == AssertionLevel.SOFT:
            assertion_manager.assert_contains(response_text, expected_text,
                                            f"API response should contain '{expected_text}'", level)
        else:
            assertion_manager.warning_assert(expected_text in response_text,
                                           f"API response should contain '{expected_text}'")
    
    def assert_api_json_value(self, json_path: str, expected_value: Any, response=None,
                             level: AssertionLevel = AssertionLevel.HARD):
        """
        Assert API JSON response value at specific path
        
        Args:
            json_path: JSON path to the value
            expected_value: Expected value
            response: Response object (uses last response if None)
            level: Assertion level (HARD, SOFT, WARNING)
        """
        self.logger.info(f"Asserting API JSON value: {json_path} = {expected_value}")
        
        try:
            actual_value = self.api_actions.get_json_value(json_path, response)
            
            if level == AssertionLevel.HARD:
                assertion_manager.assert_equals(actual_value, expected_value,
                                              f"JSON value at '{json_path}' should be {expected_value}")
            elif level == AssertionLevel.SOFT:
                assertion_manager.assert_equals(actual_value, expected_value,
                                              f"JSON value at '{json_path}' should be {expected_value}", level)
            else:
                assertion_manager.warning_assert(actual_value == expected_value,
                                               f"JSON value at '{json_path}' should be {expected_value}")
        
        except Exception as e:
            error_msg = f"Failed to get JSON value for assertion: {str(e)}"
            self.logger.error(error_msg)
            
            if level == AssertionLevel.HARD:
                assertion_manager.hard_assert(False, error_msg)
            elif level == AssertionLevel.SOFT:
                assertion_manager.soft_assert(False, error_msg)
            else:
                assertion_manager.warning_assert(False, error_msg)
    
    def assert_api_response_time_under(self, max_seconds: float, response=None,
                                      level: AssertionLevel = AssertionLevel.WARNING):
        """
        Assert API response time is under specified limit
        
        Args:
            max_seconds: Maximum allowed response time
            response: Response object (uses last response if None)
            level: Assertion level (usually WARNING for performance)
        """
        self.logger.info(f"Asserting API response time under: {max_seconds}s")
        
        response_time = self.api_actions.get_response_time(response)
        
        if level == AssertionLevel.HARD:
            assertion_manager.assert_less_than(response_time, max_seconds,
                                             f"API response time should be under {max_seconds}s")
        elif level == AssertionLevel.SOFT:
            assertion_manager.assert_less_than(response_time, max_seconds,
                                             f"API response time should be under {max_seconds}s", level)
        else:
            assertion_manager.warning_assert(response_time < max_seconds,
                                           f"API response time should be under {max_seconds}s")
    
    # Composite Assertion Keywords
    def assert_login_successful(self, expected_username: str = None,
                               level: AssertionLevel = AssertionLevel.HARD):
        """
        Assert that login was successful with comprehensive checks
        
        Args:
            expected_username: Expected username to verify (optional)
            level: Assertion level (HARD, SOFT, WARNING)
        """
        self.logger.info("Asserting login successful")
        
        # Check URL changed from login page
        current_url = self.web_actions.get_current_url()
        url_check = "login" not in current_url.lower()
        
        # Check for dashboard or welcome elements
        dashboard_indicators = [
            (By.CSS_SELECTOR, ".dashboard"),
            (By.CSS_SELECTOR, ".welcome"),
            (By.CSS_SELECTOR, "[data-testid='dashboard']"),
            (By.CSS_SELECTOR, ".user-menu"),
            (By.ID, "dashboard")
        ]
        
        dashboard_present = any(self.web_actions.is_element_present(locator) 
                              for locator in dashboard_indicators)
        
        login_success = url_check and dashboard_present
        
        if level == AssertionLevel.HARD:
            assertion_manager.hard_assert(login_success, "Login should be successful")
        elif level == AssertionLevel.SOFT:
            assertion_manager.soft_assert(login_success, "Login should be successful")
        else:
            assertion_manager.warning_assert(login_success, "Login should be successful")
        
        # Additional username check if provided
        if expected_username and login_success:
            try:
                welcome_selectors = [
                    (By.CSS_SELECTOR, ".welcome-message"),
                    (By.CSS_SELECTOR, ".user-name"),
                    (By.CSS_SELECTOR, "[data-testid='username']")
                ]
                
                for selector in welcome_selectors:
                    if self.web_actions.is_element_present(selector):
                        element_text = self.web_actions.get_element_text(selector)
                        if expected_username.lower() in element_text.lower():
                            self.logger.info(f"Username verification successful: {expected_username}")
                            break
                else:
                    if level == AssertionLevel.HARD:
                        assertion_manager.hard_assert(False, f"Username '{expected_username}' not found after login")
                    elif level == AssertionLevel.SOFT:
                        assertion_manager.soft_assert(False, f"Username '{expected_username}' not found after login")
                    else:
                        assertion_manager.warning_assert(False, f"Username '{expected_username}' not found after login")
            except Exception as e:
                self.logger.warning(f"Could not verify username after login: {str(e)}")
    
    def assert_form_validation_errors(self, field_errors: Dict[tuple, str],
                                     level: AssertionLevel = AssertionLevel.SOFT):
        """
        Assert that form validation errors are displayed as expected
        
        Args:
            field_errors: Dictionary mapping field locators to expected error messages
            level: Assertion level (usually SOFT for UI validation)
        """
        self.logger.info("Asserting form validation errors")
        
        for field_locator, expected_error in field_errors.items():
            try:
                # Check for error message near the field
                error_locator = (field_locator[0], field_locator[1] + " + .error, " + field_locator[1] + " .error")
                
                if self.web_actions.is_element_present(error_locator):
                    actual_error = self.web_actions.get_element_text(error_locator)
                    
                    if level == AssertionLevel.HARD:
                        assertion_manager.assert_contains(actual_error, expected_error,
                                                        f"Field {field_locator} should have error: {expected_error}")
                    elif level == AssertionLevel.SOFT:
                        assertion_manager.assert_contains(actual_error, expected_error,
                                                        f"Field {field_locator} should have error: {expected_error}", level)
                    else:
                        assertion_manager.warning_assert(expected_error in actual_error,
                                                       f"Field {field_locator} should have error: {expected_error}")
                else:
                    error_msg = f"No validation error found for field: {field_locator}"
                    if level == AssertionLevel.HARD:
                        assertion_manager.hard_assert(False, error_msg)
                    elif level == AssertionLevel.SOFT:
                        assertion_manager.soft_assert(False, error_msg)
                    else:
                        assertion_manager.warning_assert(False, error_msg)
            
            except Exception as e:
                self.logger.warning(f"Could not check validation error for {field_locator}: {str(e)}")