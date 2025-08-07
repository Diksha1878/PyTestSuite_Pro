"""
WebDriver Management Module for PyTestSuite Pro

This module handles WebDriver initialization, management, and cleanup
with support for local and remote execution, parallel testing, and browser options.
"""

import os
import threading
import logging
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from config import browser_config, get_current_config, BROWSER_CONFIGS


class DriverManager:
    """Manages WebDriver instances with support for parallel execution"""
    
    # Thread-local storage for parallel execution
    _local = threading.local()
    _instances: Dict[str, 'DriverManager'] = {}
    _lock = threading.Lock()
    
    def __init__(self, browser_name: str = 'chrome', headless: bool = None):
        self.browser_name = browser_name.lower()
        self.config = get_current_config()
        self.headless = headless if headless is not None else self.config.headless
        self.driver: Optional[WebDriver] = None
        self.wait: Optional[WebDriverWait] = None
        self.logger = self._setup_logger()
        
        # Remote execution settings
        self.remote_url = os.getenv('SELENIUM_REMOTE_URL')
        self.is_remote = bool(self.remote_url)
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for driver manager"""
        logger = logging.getLogger(f'DriverManager.{threading.current_thread().name}')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    @classmethod
    def get_instance(cls, browser_name: str = 'chrome', headless: bool = None) -> 'DriverManager':
        """Get or create DriverManager instance for current thread"""
        thread_id = threading.current_thread().ident
        key = f"{thread_id}_{browser_name}"
        
        with cls._lock:
            if key not in cls._instances:
                cls._instances[key] = cls(browser_name, headless)
            return cls._instances[key]
    
    def start_driver(self) -> WebDriver:
        """Initialize and start WebDriver"""
        try:
            if self.driver:
                self.logger.warning("Driver already initialized. Reusing existing instance.")
                return self.driver
            
            self.logger.info(f"Starting {self.browser_name} driver (headless={self.headless})")
            
            if self.is_remote:
                self.driver = self._create_remote_driver()
            else:
                self.driver = self._create_local_driver()
            
            # Configure driver settings
            self._configure_driver()
            
            # Initialize WebDriverWait
            self.wait = WebDriverWait(self.driver, self.config.timeout)
            
            self.logger.info(f"Driver started successfully: {self.driver.session_id}")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Failed to start driver: {str(e)}")
            self.quit_driver()
            raise WebDriverException(f"Failed to initialize {self.browser_name} driver: {str(e)}")
    def _create_local_driver(self) -> WebDriver:
        """Create local WebDriver instance"""
        driver_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'drivers')

        browser_caps = BROWSER_CONFIGS.get(
            f'{self.browser_name}_headless' if self.headless else f'{self.browser_name}_debug',
            browser_config.get_default_chrome_capabilities()
        )
        browser_caps.headless = self.headless

        if self.browser_name == 'chrome':
            options = browser_config.get_chrome_options(browser_caps)
            driver_path = os.path.join(driver_dir, 'chromedriver.exe')
            service = ChromeService(executable_path=driver_path)
            return webdriver.Chrome(service=service, options=options)

        elif self.browser_name == 'firefox':
            options = browser_config.get_firefox_options(browser_caps)
            driver_path = os.path.join(driver_dir, 'geckodriver.exe')
            service = FirefoxService(executable_path=driver_path)
            return webdriver.Firefox(service=service, options=options)

        elif self.browser_name == 'edge':
            options = browser_config.get_edge_options(browser_caps)
            driver_path = os.path.join(driver_dir, 'msedgedriver.exe')
            service = EdgeService(executable_path=driver_path)
            return webdriver.Edge(service=service, options=options)

        else:
            raise ValueError(f"Unsupported browser: {self.browser_name}")

    
    def _create_remote_driver(self) -> WebDriver:
        """Create remote WebDriver instance for Selenium Grid"""
        capabilities = self._get_remote_capabilities()
        
        try:
            return webdriver.Remote(
                command_executor=self.remote_url,
                desired_capabilities=capabilities
            )
        except Exception as e:
            self.logger.error(f"Failed to connect to remote WebDriver: {str(e)}")
            raise
    
    def _get_remote_capabilities(self) -> Dict[str, Any]:
        """Get capabilities for remote WebDriver"""
        base_caps = {
            'browserName': self.browser_name,
            'platform': os.getenv('SELENIUM_PLATFORM', 'ANY'),
            'version': os.getenv('SELENIUM_VERSION', 'latest'),
            'enableVNC': True,
            'enableVideo': False,
            'screenResolution': '1920x1080x24'
        }
        
        if self.browser_name == 'chrome':
            chrome_options = browser_config.get_chrome_options()
            base_caps['goog:chromeOptions'] = chrome_options.to_capabilities()['goog:chromeOptions']
        elif self.browser_name == 'firefox':
            firefox_options = browser_config.get_firefox_options()
            base_caps['moz:firefoxOptions'] = firefox_options.to_capabilities()['moz:firefoxOptions']
        
        return base_caps
    
    def _configure_driver(self):
        """Configure driver with common settings"""
        if not self.driver:
            return
        
        # Set window size and position
        if not self.headless:
            self.driver.set_window_size(
                self.config.browser_width, 
                self.config.browser_height
            )
            self.driver.set_window_position(0, 0)
        
        # Configure implicit wait
        self.driver.implicitly_wait(5)
        
        # Configure page load timeout
        self.driver.set_page_load_timeout(30)
        
        # Configure script timeout
        self.driver.set_script_timeout(30)
    
    def quit_driver(self):
        """Quit WebDriver and cleanup resources"""
        if self.driver:
            try:
                session_id = getattr(self.driver, 'session_id', 'unknown')
                self.logger.info(f"Quitting driver with session: {session_id}")
                self.driver.quit()
            except Exception as e:
                self.logger.error(f"Error quitting driver: {str(e)}")
            finally:
                self.driver = None
                self.wait = None
    
    def get_driver(self) -> Optional[WebDriver]:
        """Get current WebDriver instance"""
        return self.driver
    
    def get_wait(self) -> Optional[WebDriverWait]:
        """Get WebDriverWait instance"""
        return self.wait
    
    def is_driver_active(self) -> bool:
        """Check if driver is active and responsive"""
        if not self.driver:
            return False
        
        try:
            # Try to get current URL to check if driver is responsive
            self.driver.current_url
            return True
        except Exception:
            return False
    
    def restart_driver(self):
        """Restart WebDriver (quit and start new instance)"""
        self.logger.info("Restarting driver")
        self.quit_driver()
        return self.start_driver()
    
    def take_screenshot(self, filename: str = None) -> str:
        """Take screenshot and return file path"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        if not filename:
            import time
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_path = os.path.join("reports", "screenshots", filename)
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        
        self.driver.save_screenshot(screenshot_path)
        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    def get_page_source(self, filename: str = None) -> str:
        """Get page source and save to file"""
        if not self.driver:
            raise WebDriverException("Driver not initialized")
        
        if not filename:
            import time
            timestamp = int(time.time())
            filename = f"page_source_{timestamp}.html"
        
        source_path = os.path.join("reports", "page_sources", filename)
        os.makedirs(os.path.dirname(source_path), exist_ok=True)
        
        with open(source_path, 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)
        
        self.logger.info(f"Page source saved: {source_path}")
        return source_path
    
    @classmethod
    def cleanup_all_drivers(cls):
        """Cleanup all driver instances (for test teardown)"""
        with cls._lock:
            for instance in cls._instances.values():
                instance.quit_driver()
            cls._instances.clear()


# Global driver manager functions for easy access
def get_driver(browser_name: str = 'chrome', headless: bool = None) -> WebDriver:
    """Get WebDriver instance for current thread"""
    driver_manager = DriverManager.get_instance(browser_name, headless)
    if not driver_manager.is_driver_active():
        driver_manager.start_driver()
    return driver_manager.get_driver()


def quit_driver():
    """Quit current thread's WebDriver"""
    thread_id = threading.current_thread().ident
    for key, instance in DriverManager._instances.items():
        if key.startswith(str(thread_id)):
            instance.quit_driver()


def get_wait(timeout: int = None) -> WebDriverWait:
    """Get WebDriverWait instance for current driver"""
    driver = get_driver()
    if timeout:
        return WebDriverWait(driver, timeout)
    
    # Try to get existing wait from driver manager
    thread_id = threading.current_thread().ident
    for key, instance in DriverManager._instances.items():
        if key.startswith(str(thread_id)):
            return instance.get_wait()
    
    # Create new wait with default timeout
    return WebDriverWait(driver, 10)


def take_screenshot(filename: str = None) -> str:
    """Take screenshot with current driver"""
    thread_id = threading.current_thread().ident
    for key, instance in DriverManager._instances.items():
        if key.startswith(str(thread_id)):
            return instance.take_screenshot(filename)
    
    raise WebDriverException("No active driver found for current thread")