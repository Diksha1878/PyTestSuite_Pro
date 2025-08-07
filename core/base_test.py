"""
Base Test Class for PyTestSuite Pro

This module provides the base test class with common functionality
for all test types including setup, teardown, and utility methods.
"""

import os
import time
import logging
import pytest
from typing import Optional, Dict, Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException

from .driver_manager import DriverManager, get_driver, quit_driver, take_screenshot
from .assertions import assertion_manager, AssertionManager
from config import get_current_config


class BaseTest:
    """Base class for all test classes with common functionality"""
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for test class"""
        class_name = self.__class__.__name__
        logger = logging.getLogger(f'Test.{class_name}')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def setup_method(self, method):
        """Setup method called before each test method"""
        # Initialize attributes
        self.driver: Optional[WebDriver] = None
        self.config = get_current_config()
        self.logger = self._setup_logger()
        self.test_start_time = time.time()
        self.test_data: Dict[str, Any] = {}
        
        test_name = f"{self.__class__.__name__}.{method.__name__}"
        
        self.logger.info(f"🚀 Starting test: {test_name}")
        
        # Set test context for assertions
        assertion_manager.reset()
        assertion_manager.set_test_context(test_name)
        
        # Initialize driver if needed for UI tests
        if hasattr(self, 'browser_name'):
            browser = getattr(self, 'browser_name', 'chrome')
            headless = getattr(self, 'headless', None)
            try:
                self.driver = get_driver(browser, headless)
                self.logger.info(f"Driver initialized: {browser}")
            except Exception as e:
                self.logger.error(f"Failed to initialize driver: {str(e)}")
                raise
        
        # Load test data if method has test_data marker
        self._load_test_data(method)
    
    def teardown_method(self, method):
        """Teardown method called after each test method"""
        test_name = f"{self.__class__.__name__}.{method.__name__}"
        execution_time = time.time() - self.test_start_time if self.test_start_time else 0
        
        try:
            # Take screenshot on failure if configured
            if hasattr(self, '_pytest_current_test'):
                test_result = getattr(self._pytest_current_test, 'result', None)
                if (test_result and not test_result.passed and 
                    self.config.screenshot_on_failure and self.driver):
                    screenshot_path = self.take_screenshot(f"{test_name}_failure")
                    self.logger.info(f"Failure screenshot saved: {screenshot_path}")
        except Exception as e:
            self.logger.warning(f"Failed to take failure screenshot: {str(e)}")
        
        # Cleanup driver
        if self.driver:
            try:
                quit_driver()
                self.logger.info("Driver cleanup completed")
            except Exception as e:
                self.logger.warning(f"Driver cleanup warning: {str(e)}")
        
        # Cleanup test data if configured
        if self.config.test_data_cleanup:
            self._cleanup_test_data()
        
        self.logger.info(f"✅ Test completed: {test_name} (Duration: {execution_time:.2f}s)")
    
    def _load_test_data(self, method):
        """Load test data based on method markers or attributes"""
        # Check for test_data marker
        if hasattr(method, 'pytestmark'):
            for marker in method.pytestmark:
                if marker.name == 'test_data':
                    data_file = marker.args[0] if marker.args else None
                    if data_file:
                        self.test_data = self._load_data_from_file(data_file)
                        self.logger.info(f"Test data loaded from: {data_file}")
                        break
    
    def _load_data_from_file(self, data_file: str) -> Dict[str, Any]:
        """Load test data from file"""
        import json
        import yaml
        
        data_path = os.path.join("test_data", data_file)
        
        if not os.path.exists(data_path):
            self.logger.warning(f"Test data file not found: {data_path}")
            return {}
        
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                if data_file.endswith('.json'):
                    return json.load(f)
                elif data_file.endswith(('.yml', '.yaml')):
                    return yaml.safe_load(f)
                else:
                    return {'raw_content': f.read()}
        except Exception as e:
            self.logger.error(f"Failed to load test data from {data_path}: {str(e)}")
            return {}
    
    def _cleanup_test_data(self):
        """Cleanup test data after test execution"""
        # Override in subclasses for specific cleanup logic
        pass
    
    def get_test_data(self, key: str, default=None):
        """Get test data by key"""
        return self.test_data.get(key, default)
    
    def set_test_data(self, key: str, value: Any):
        """Set test data during test execution"""
        self.test_data[key] = value
    
    def take_screenshot(self, filename: str = None) -> str:
        """Take screenshot with current driver"""
        if not self.driver:
            raise WebDriverException("No driver available for screenshot")
        return take_screenshot(filename)
    
    def navigate_to(self, url: str):
        """Navigate to URL (adds base URL if relative)"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        if url.startswith(('http://', 'https://')):
            full_url = url
        else:
            full_url = f"{self.config.base_url.rstrip('/')}/{url.lstrip('/')}"
        
        self.logger.info(f"Navigating to: {full_url}")
        self.driver.get(full_url)
    
    def wait_for_page_load(self, timeout: int = None):
        """Wait for page to be fully loaded"""
        if not self.driver:
            return
        
        timeout = timeout or self.config.timeout
        
        # Wait for document ready state
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        self.logger.debug("Page load completed")
    
    def refresh_page(self):
        """Refresh current page"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        self.logger.info("Refreshing page")
        self.driver.refresh()
        self.wait_for_page_load()
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get current page title"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        return self.driver.title
    
    def execute_javascript(self, script: str, *args):
        """Execute JavaScript in browser"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        self.logger.debug(f"Executing JavaScript: {script}")
        return self.driver.execute_script(script, *args)
    
    def switch_to_window(self, window_handle: str = None):
        """Switch to window by handle or to the latest window"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        if window_handle:
            self.driver.switch_to.window(window_handle)
        else:
            # Switch to the latest opened window
            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[-1])
        
        self.logger.info(f"Switched to window: {self.driver.current_window_handle}")
    
    def close_current_window(self):
        """Close current window and switch to previous"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        windows = self.driver.window_handles
        if len(windows) > 1:
            self.driver.close()
            # Switch to the first available window
            self.driver.switch_to.window(windows[0])
            self.logger.info("Closed current window and switched to previous")
        else:
            self.logger.warning("Cannot close the only window")
    
    def maximize_window(self):
        """Maximize browser window"""
        if self.driver:
            self.driver.maximize_window()
            self.logger.debug("Window maximized")
    
    def set_window_size(self, width: int, height: int):
        """Set browser window size"""
        if self.driver:
            self.driver.set_window_size(width, height)
            self.logger.debug(f"Window size set to: {width}x{height}")
    
    def delete_all_cookies(self):
        """Delete all browser cookies"""
        if self.driver:
            self.driver.delete_all_cookies()
            self.logger.info("All cookies deleted")
    
    def add_cookie(self, cookie_dict: Dict[str, Any]):
        """Add cookie to browser"""
        if self.driver:
            self.driver.add_cookie(cookie_dict)
            self.logger.debug(f"Cookie added: {cookie_dict.get('name', 'unknown')}")
    
    def get_cookie(self, name: str) -> Optional[Dict[str, Any]]:
        """Get cookie by name"""
        if self.driver:
            return self.driver.get_cookie(name)
        return None
    
    def implicit_wait(self, timeout: int):
        """Set implicit wait timeout"""
        if self.driver:
            self.driver.implicitly_wait(timeout)
            self.logger.debug(f"Implicit wait set to: {timeout}s")


class UITest(BaseTest):
    """Base class for UI tests with browser-specific functionality"""
    
    # Default browser for UI tests
    browser_name = 'chrome'
    headless = False
    
    def setup_method(self, method):
        """UI test specific setup"""
        super().setup_method(method)
        
        if self.driver:
            self.maximize_window()
            self.delete_all_cookies()


class APITest(BaseTest):
    """Base class for API tests"""
    
    def setup_method(self, method):
        """API test specific setup"""
        super().setup_method(method)
        
        # Initialize API-specific attributes
        self.api_base_url = self.config.api_base_url
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        import requests
        self.session = requests.Session()
        self.session.headers.update(self.default_headers)
        
        self.logger.info(f"API session initialized for: {self.api_base_url}")
    
    def teardown_method(self, method):
        """API test specific teardown"""
        if self.session:
            self.session.close()
            self.logger.info("API session closed")
        
        super().teardown_method(method)
    
    def get_full_api_url(self, endpoint: str) -> str:
        """Get full API URL for endpoint"""
        return f"{self.api_base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    
    def set_auth_token(self, token: str, token_type: str = 'Bearer'):
        """Set authentication token for API requests"""
        if self.session:
            self.session.headers['Authorization'] = f"{token_type} {token}"
            self.logger.info("Authentication token set")


class IntegrationTest(BaseTest):
    """Base class for integration tests combining UI and API"""
    
    browser_name = 'chrome'
    headless = True  # Usually run headless for integration tests
    
    def setup_method(self, method):
        """Integration test specific setup"""
        super().setup_method(method)
        
        # Initialize API-specific attributes
        self.api_base_url = self.config.api_base_url
        
        # Initialize API session
        import requests
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        self.logger.info("Integration test setup completed (UI + API)")
    
    def teardown_method(self, method):
        """Integration test specific teardown"""
        if self.session:
            self.session.close()
        
        super().teardown_method(method)


# Pytest fixtures for base test functionality
@pytest.fixture(scope="function")
def base_test():
    """Fixture providing base test instance"""
    return BaseTest()


@pytest.fixture(scope="function")
def ui_test():
    """Fixture providing UI test instance"""
    test_instance = UITest()
    yield test_instance
    # Cleanup is handled by teardown_method


@pytest.fixture(scope="function")
def api_test():
    """Fixture providing API test instance"""
    test_instance = APITest()
    yield test_instance
    # Cleanup is handled by teardown_method