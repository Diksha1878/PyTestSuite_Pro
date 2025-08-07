"""
Web Actions Keywords for PyTestSuite Pro

This module provides high-level keyword actions for web testing
that can be used across different test scenarios.
"""

import time
import logging
from typing import List, Dict, Any, Optional, Union
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from core import get_driver, assertion_manager
from pages import LoginPage, DashboardPage


class WebActions:
    """High-level web action keywords for test automation"""
    
    def __init__(self):
        self.driver = None
        self.logger = self._setup_logger()
        self.login_page = None
        self.dashboard_page = None
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for web actions"""
        logger = logging.getLogger('WebActions')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _ensure_driver(self):
        """Ensure driver is available"""
        if not self.driver:
            self.driver = get_driver()
        
        if not self.login_page:
            self.login_page = LoginPage(self.driver)
        
        if not self.dashboard_page:
            self.dashboard_page = DashboardPage(self.driver)
    
    # Navigation Keywords
    def navigate_to_url(self, url: str):
        """
        Navigate to specific URL
        
        Args:
            url: URL to navigate to (can be relative or absolute)
        """
        self._ensure_driver()
        
        if url.startswith(('http://', 'https://')):
            full_url = url
        else:
            from config import get_base_url
            base_url = get_base_url()
            full_url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"
        
        self.logger.info(f"Navigating to URL: {full_url}")
        self.driver.get(full_url)
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
        self.logger.info(f"Successfully navigated to: {self.driver.current_url}")
    
    def refresh_page(self):
        """Refresh the current page"""
        self._ensure_driver()
        self.logger.info("Refreshing current page")
        self.driver.refresh()
        
        # Wait for page to reload
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    def go_back(self):
        """Navigate back in browser history"""
        self._ensure_driver()
        self.logger.info("Navigating back in browser history")
        self.driver.back()
    
    def go_forward(self):
        """Navigate forward in browser history"""
        self._ensure_driver()
        self.logger.info("Navigating forward in browser history")
        self.driver.forward()
    
    # Authentication Keywords
    def login_user(self, username: str, password: str, remember_me: bool = False) -> bool:
        """
        Login with username and password
        
        Args:
            username: Username for login
            password: Password for login  
            remember_me: Whether to check remember me option
            
        Returns:
            bool: True if login successful, False otherwise
        """
        self._ensure_driver()
        self.logger.info(f"Attempting to login user: {username}")
        
        # Navigate to login page if not already there
        current_url = self.driver.current_url
        if "login" not in current_url.lower():
            self.login_page.open_login_page()
        
        # Perform login
        success = self.login_page.login(username, password, remember_me)
        
        if success:
            self.logger.info(f"Login successful for user: {username}")
        else:
            error_msg = self.login_page.get_error_message()
            self.logger.error(f"Login failed for user {username}: {error_msg}")
        
        return success
    
    def quick_login(self) -> bool:
        """
        Quick login using default credentials from configuration
        
        Returns:
            bool: True if login successful, False otherwise
        """
        self._ensure_driver()
        self.logger.info("Performing quick login with default credentials")
        
        if "login" not in self.driver.current_url.lower():
            self.login_page.open_login_page()
        
        return self.login_page.quick_login()
    
    def logout_user(self):
        """Logout current user"""
        self._ensure_driver()
        self.logger.info("Attempting to logout user")
        
        # Try logout from dashboard first
        try:
            self.dashboard_page.logout()
            self.logger.info("Logout successful from dashboard")
        except:
            # Try logout from login page
            try:
                self.login_page.logout()
                self.logger.info("Logout successful from login page")
            except:
                self.logger.warning("Could not find logout option")
    
    # Element Interaction Keywords
    def click_element(self, locator: tuple, timeout: int = 10):
        """
        Click on element with wait
        
        Args:
            locator: Element locator tuple (By, value)
            timeout: Wait timeout in seconds
        """
        self._ensure_driver()
        self.logger.info(f"Clicking element: {locator}")
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            self.logger.info(f"Successfully clicked element: {locator}")
            
        except TimeoutException:
            self.logger.error(f"Element not clickable within {timeout}s: {locator}")
            raise
    
    def type_text(self, locator: tuple, text: str, clear_first: bool = True, timeout: int = 10):
        """
        Type text into element
        
        Args:
            locator: Element locator tuple (By, value)
            text: Text to type
            clear_first: Whether to clear field before typing
            timeout: Wait timeout in seconds
        """
        self._ensure_driver()
        self.logger.info(f"Typing text into element {locator}: '{text}'")
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            
            if clear_first:
                element.clear()
            
            element.send_keys(text)
            self.logger.info(f"Successfully typed text into element: {locator}")
            
        except TimeoutException:
            self.logger.error(f"Element not visible within {timeout}s: {locator}")
            raise
    
    def get_element_text(self, locator: tuple, timeout: int = 10) -> str:
        """
        Get text content from element
        
        Args:
            locator: Element locator tuple (By, value)
            timeout: Wait timeout in seconds
            
        Returns:
            str: Element text content
        """
        self._ensure_driver()
        self.logger.info(f"Getting text from element: {locator}")
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            
            text = element.text
            self.logger.info(f"Got text from element {locator}: '{text}'")
            return text
            
        except TimeoutException:
            self.logger.error(f"Element not visible within {timeout}s: {locator}")
            raise
    
    def get_element_attribute(self, locator: tuple, attribute: str, timeout: int = 10) -> str:
        """
        Get attribute value from element
        
        Args:
            locator: Element locator tuple (By, value)
            attribute: Attribute name to get
            timeout: Wait timeout in seconds
            
        Returns:
            str: Attribute value
        """
        self._ensure_driver()
        self.logger.info(f"Getting attribute '{attribute}' from element: {locator}")
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            
            value = element.get_attribute(attribute) or ""
            self.logger.info(f"Got attribute '{attribute}' from element {locator}: '{value}'")
            return value
            
        except TimeoutException:
            self.logger.error(f"Element not found within {timeout}s: {locator}")
            raise
    
    def select_dropdown_option(self, dropdown_locator: tuple, option_text: str, timeout: int = 10):
        """
        Select option from dropdown by visible text
        
        Args:
            dropdown_locator: Dropdown element locator
            option_text: Visible text of option to select
            timeout: Wait timeout in seconds
        """
        self._ensure_driver()
        self.logger.info(f"Selecting dropdown option '{option_text}' from: {dropdown_locator}")
        
        from selenium.webdriver.support.ui import Select
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(dropdown_locator)
            )
            
            select = Select(element)
            select.select_by_visible_text(option_text)
            self.logger.info(f"Successfully selected option: {option_text}")
            
        except TimeoutException:
            self.logger.error(f"Dropdown not clickable within {timeout}s: {dropdown_locator}")
            raise
    
    def check_checkbox(self, locator: tuple, timeout: int = 10):
        """
        Check checkbox if not already checked
        
        Args:
            locator: Checkbox element locator
            timeout: Wait timeout in seconds
        """
        self._ensure_driver()
        self.logger.info(f"Checking checkbox: {locator}")
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            
            if not element.is_selected():
                element.click()
                self.logger.info(f"Checkbox checked: {locator}")
            else:
                self.logger.info(f"Checkbox already checked: {locator}")
                
        except TimeoutException:
            self.logger.error(f"Checkbox not clickable within {timeout}s: {locator}")
            raise
    
    def uncheck_checkbox(self, locator: tuple, timeout: int = 10):
        """
        Uncheck checkbox if currently checked
        
        Args:
            locator: Checkbox element locator
            timeout: Wait timeout in seconds
        """
        self._ensure_driver()
        self.logger.info(f"Unchecking checkbox: {locator}")
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            
            if element.is_selected():
                element.click()
                self.logger.info(f"Checkbox unchecked: {locator}")
            else:
                self.logger.info(f"Checkbox already unchecked: {locator}")
                
        except TimeoutException:
            self.logger.error(f"Checkbox not clickable within {timeout}s: {locator}")
            raise
    
    # Wait Keywords
    def wait_for_element_visible(self, locator: tuple, timeout: int = 10) -> bool:
        """
        Wait for element to be visible
        
        Args:
            locator: Element locator tuple (By, value)
            timeout: Wait timeout in seconds
            
        Returns:
            bool: True if element becomes visible, False if timeout
        """
        self._ensure_driver()
        self.logger.info(f"Waiting for element to be visible: {locator}")
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f"Element became visible: {locator}")
            return True
            
        except TimeoutException:
            self.logger.warning(f"Element not visible within {timeout}s: {locator}")
            return False
    
    def wait_for_element_invisible(self, locator: tuple, timeout: int = 10) -> bool:
        """
        Wait for element to be invisible
        
        Args:
            locator: Element locator tuple (By, value)
            timeout: Wait timeout in seconds
            
        Returns:
            bool: True if element becomes invisible, False if timeout
        """
        self._ensure_driver()
        self.logger.info(f"Waiting for element to be invisible: {locator}")
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            self.logger.info(f"Element became invisible: {locator}")
            return True
            
        except TimeoutException:
            self.logger.warning(f"Element still visible after {timeout}s: {locator}")
            return False
    
    def wait_for_text_present(self, locator: tuple, text: str, timeout: int = 10) -> bool:
        """
        Wait for specific text to be present in element
        
        Args:
            locator: Element locator tuple (By, value)
            text: Text to wait for
            timeout: Wait timeout in seconds
            
        Returns:
            bool: True if text appears, False if timeout
        """
        self._ensure_driver()
        self.logger.info(f"Waiting for text '{text}' in element: {locator}")
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            self.logger.info(f"Text '{text}' found in element: {locator}")
            return True
            
        except TimeoutException:
            self.logger.warning(f"Text '{text}' not found within {timeout}s: {locator}")
            return False
    
    # Utility Keywords
    def take_screenshot(self, filename: str = None) -> str:
        """
        Take screenshot of current page
        
        Args:
            filename: Optional filename for screenshot
            
        Returns:
            str: Path to saved screenshot
        """
        self._ensure_driver()
        from core.driver_manager import take_screenshot
        return take_screenshot(filename)
    
    def scroll_to_element(self, locator: tuple, timeout: int = 10):
        """
        Scroll element into view
        
        Args:
            locator: Element locator tuple (By, value)
            timeout: Wait timeout in seconds
        """
        self._ensure_driver()
        self.logger.info(f"Scrolling to element: {locator}")
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)  # Small delay for scroll completion
            self.logger.info(f"Scrolled to element: {locator}")
            
        except TimeoutException:
            self.logger.error(f"Element not found for scrolling: {locator}")
            raise
    
    def hover_over_element(self, locator: tuple, timeout: int = 10):
        """
        Hover mouse over element
        
        Args:
            locator: Element locator tuple (By, value)
            timeout: Wait timeout in seconds
        """
        self._ensure_driver()
        self.logger.info(f"Hovering over element: {locator}")
        
        from selenium.webdriver.common.action_chains import ActionChains
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.logger.info(f"Hovered over element: {locator}")
            
        except TimeoutException:
            self.logger.error(f"Element not visible for hover: {locator}")
            raise
    
    def execute_javascript(self, script: str, *args) -> Any:
        """
        Execute JavaScript code
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to script
            
        Returns:
            Any: Result of JavaScript execution
        """
        self._ensure_driver()
        self.logger.info(f"Executing JavaScript: {script}")
        
        result = self.driver.execute_script(script, *args)
        self.logger.info(f"JavaScript execution completed")
        return result
    
    # Form Keywords
    def fill_form(self, form_data: Dict[tuple, str], submit_button: tuple = None):
        """
        Fill form with provided data
        
        Args:
            form_data: Dictionary mapping locators to values
            submit_button: Optional submit button locator
        """
        self._ensure_driver()
        self.logger.info(f"Filling form with {len(form_data)} fields")
        
        for locator, value in form_data.items():
            self.type_text(locator, value)
        
        if submit_button:
            self.click_element(submit_button)
            self.logger.info("Form submitted")
    
    # Validation Keywords
    def is_element_present(self, locator: tuple) -> bool:
        """
        Check if element is present in DOM
        
        Args:
            locator: Element locator tuple (By, value)
            
        Returns:
            bool: True if element is present, False otherwise
        """
        self._ensure_driver()
        
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: tuple) -> bool:
        """
        Check if element is visible on page
        
        Args:
            locator: Element locator tuple (By, value)
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        self._ensure_driver()
        
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def is_element_enabled(self, locator: tuple) -> bool:
        """
        Check if element is enabled
        
        Args:
            locator: Element locator tuple (By, value)
            
        Returns:
            bool: True if element is enabled, False otherwise
        """
        self._ensure_driver()
        
        try:
            element = self.driver.find_element(*locator)
            return element.is_enabled()
        except NoSuchElementException:
            return False
    
    # Page Information Keywords
    def get_page_title(self) -> str:
        """
        Get current page title
        
        Returns:
            str: Current page title
        """
        self._ensure_driver()
        title = self.driver.title
        self.logger.info(f"Current page title: '{title}'")
        return title
    
    def get_current_url(self) -> str:
        """
        Get current page URL
        
        Returns:
            str: Current page URL
        """
        self._ensure_driver()
        url = self.driver.current_url
        self.logger.info(f"Current URL: '{url}'")
        return url
    
    def get_page_source(self) -> str:
        """
        Get page source HTML
        
        Returns:
            str: Page source HTML
        """
        self._ensure_driver()
        self.logger.info("Getting page source")
        return self.driver.page_source