"""
Base Page Object Model for PyTestSuite Pro

This module provides the base page class with common functionality
for all page objects including element interactions, waits, and utilities.
"""

import time
import logging
from typing import Optional, List, Tuple, Any, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementNotInteractableException,
    StaleElementReferenceException, WebDriverException
)

from .driver_manager import get_driver, get_wait
from .assertions import assertion_manager
from config import get_current_config


class BasePage:
    """Base Page Object Model class with common page functionality"""
    
    def __init__(self, driver: WebDriver = None):
        self.driver = driver or get_driver()
        self.config = get_current_config()
        self.logger = self._setup_logger()
        self.wait = WebDriverWait(self.driver, self.config.timeout)
        self.actions = ActionChains(self.driver)
        
        # Page-specific properties (override in subclasses)
        self.page_url = ""
        self.page_title = ""
        self.page_load_element = None
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for page object"""
        page_name = self.__class__.__name__
        logger = logging.getLogger(f'Page.{page_name}')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    # Navigation methods
    def open(self, relative_url: str = None):
        """Open page using base URL + relative URL"""
        url = relative_url or self.page_url
        if url.startswith(('http://', 'https://')):
            full_url = url
        else:
            full_url = f"{self.config.base_url.rstrip('/')}/{url.lstrip('/')}"
        
        self.logger.info(f"Opening page: {full_url}")
        self.driver.get(full_url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: int = None):
        """Wait for page to load completely"""
        timeout = timeout or self.config.timeout
        
        try:
            # Wait for document ready state
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for page-specific load element if defined
            if self.page_load_element:
                self.wait_for_element_visible(self.page_load_element, timeout)
            
            self.logger.debug("Page loaded successfully")
            
        except TimeoutException:
            self.logger.warning(f"Page load timeout after {timeout}s")
            raise
    
    def refresh(self):
        """Refresh current page"""
        self.logger.info("Refreshing page")
        self.driver.refresh()
        self.wait_for_page_load()
    
    def go_back(self):
        """Navigate back in browser history"""
        self.logger.info("Navigating back")
        self.driver.back()
        self.wait_for_page_load()
    
    def go_forward(self):
        """Navigate forward in browser history"""
        self.logger.info("Navigating forward")
        self.driver.forward()
        self.wait_for_page_load()
    
    # Element finding methods
    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Find element with explicit wait"""
        timeout = timeout or self.config.timeout
        
        try:
            self.logger.debug(f"Finding element: {locator}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
            
        except TimeoutException:
            self.logger.error(f"Element not found within {timeout}s: {locator}")
            raise NoSuchElementException(f"Element not found: {locator}")
    
    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """Find multiple elements with explicit wait"""
        timeout = timeout or self.config.timeout
        
        try:
            self.logger.debug(f"Finding elements: {locator}")
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
            
        except TimeoutException:
            self.logger.debug(f"No elements found: {locator}")
            return []
    
    def find_clickable_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Find clickable element with explicit wait"""
        timeout = timeout or self.config.timeout
        
        try:
            self.logger.debug(f"Finding clickable element: {locator}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
            
        except TimeoutException:
            self.logger.error(f"Clickable element not found within {timeout}s: {locator}")
            raise NoSuchElementException(f"Clickable element not found: {locator}")
    
    def find_visible_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Find visible element with explicit wait"""
        timeout = timeout or self.config.timeout
        
        try:
            self.logger.debug(f"Finding visible element: {locator}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
            
        except TimeoutException:
            self.logger.error(f"Visible element not found within {timeout}s: {locator}")
            raise NoSuchElementException(f"Visible element not found: {locator}")
    
    # Element interaction methods
    def click(self, locator: Tuple[str, str], timeout: int = None):
        """Click on element with retry logic"""
        timeout = timeout or self.config.timeout
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                element = self.find_clickable_element(locator, timeout)
                
                # Scroll element into view
                self.scroll_to_element(element)
                
                # Try regular click first
                element.click()
                self.logger.debug(f"Clicked element: {locator}")
                return
                
            except (StaleElementReferenceException, ElementNotInteractableException) as e:
                if attempt == max_attempts - 1:
                    self.logger.error(f"Failed to click element after {max_attempts} attempts: {locator}")
                    # Try JavaScript click as last resort
                    try:
                        self.click_with_javascript(locator)
                        return
                    except Exception:
                        raise e
                
                self.logger.warning(f"Click attempt {attempt + 1} failed, retrying: {str(e)}")
                time.sleep(0.5)
    
    def click_with_javascript(self, locator: Tuple[str, str]):
        """Click element using JavaScript"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
        self.logger.debug(f"JavaScript clicked element: {locator}")
    
    def double_click(self, locator: Tuple[str, str]):
        """Double click on element"""
        element = self.find_clickable_element(locator)
        self.scroll_to_element(element)
        self.actions.double_click(element).perform()
        self.logger.debug(f"Double clicked element: {locator}")
    
    def right_click(self, locator: Tuple[str, str]):
        """Right click on element"""
        element = self.find_clickable_element(locator)
        self.scroll_to_element(element)
        self.actions.context_click(element).perform()
        self.logger.debug(f"Right clicked element: {locator}")
    
    def type(self, locator: Tuple[str, str], text: str, clear_first: bool = True):
        """Type text into element"""
        element = self.find_visible_element(locator)
        self.scroll_to_element(element)
        
        if clear_first:
            element.clear()
        
        element.send_keys(text)
        self.logger.debug(f"Typed text into element {locator}: '{text}'")
    
    def type_slowly(self, locator: Tuple[str, str], text: str, delay: float = 0.1):
        """Type text slowly character by character"""
        element = self.find_visible_element(locator)
        self.scroll_to_element(element)
        element.clear()
        
        for char in text:
            element.send_keys(char)
            time.sleep(delay)
        
        self.logger.debug(f"Slowly typed text into element {locator}: '{text}'")
    
    def clear(self, locator: Tuple[str, str]):
        """Clear text from element"""
        element = self.find_visible_element(locator)
        element.clear()
        self.logger.debug(f"Cleared element: {locator}")
    
    def press_key(self, locator: Tuple[str, str], key: Keys):
        """Press specific key on element"""
        element = self.find_visible_element(locator)
        element.send_keys(key)
        self.logger.debug(f"Pressed key {key} on element: {locator}")
    
    def submit_form(self, locator: Tuple[str, str]):
        """Submit form using element"""
        element = self.find_element(locator)
        element.submit()
        self.logger.debug(f"Submitted form via element: {locator}")
    
    # Text and attribute methods
    def get_text(self, locator: Tuple[str, str]) -> str:
        """Get text content of element"""
        element = self.find_visible_element(locator)
        text = element.text
        self.logger.debug(f"Got text from element {locator}: '{text}'")
        return text
    
    def get_attribute(self, locator: Tuple[str, str], attribute_name: str) -> Optional[str]:
        """Get attribute value from element"""
        element = self.find_element(locator)
        value = element.get_attribute(attribute_name)
        self.logger.debug(f"Got attribute '{attribute_name}' from element {locator}: '{value}'")
        return value
    
    def get_property(self, locator: Tuple[str, str], property_name: str) -> Optional[str]:
        """Get property value from element"""
        element = self.find_element(locator)
        value = element.get_property(property_name)
        self.logger.debug(f"Got property '{property_name}' from element {locator}: '{value}'")
        return value
    
    def get_css_value(self, locator: Tuple[str, str], property_name: str) -> str:
        """Get CSS property value from element"""
        element = self.find_element(locator)
        value = element.value_of_css_property(property_name)
        self.logger.debug(f"Got CSS property '{property_name}' from element {locator}: '{value}'")
        return value
    
    # Dropdown/Select methods
    def select_by_visible_text(self, locator: Tuple[str, str], text: str):
        """Select dropdown option by visible text"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)
        self.logger.debug(f"Selected by visible text '{text}' in dropdown: {locator}")
    
    def select_by_value(self, locator: Tuple[str, str], value: str):
        """Select dropdown option by value"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_value(value)
        self.logger.debug(f"Selected by value '{value}' in dropdown: {locator}")
    
    def select_by_index(self, locator: Tuple[str, str], index: int):
        """Select dropdown option by index"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_index(index)
        self.logger.debug(f"Selected by index {index} in dropdown: {locator}")
    
    def get_selected_text(self, locator: Tuple[str, str]) -> str:
        """Get selected option text from dropdown"""
        element = self.find_element(locator)
        select = Select(element)
        return select.first_selected_option.text
    
    def get_all_options(self, locator: Tuple[str, str]) -> List[str]:
        """Get all option texts from dropdown"""
        element = self.find_element(locator)
        select = Select(element)
        return [option.text for option in select.options]
    
    # Wait methods
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Wait for element to be visible"""
        timeout = timeout or self.config.timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.debug(f"Element became visible: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Element not visible within {timeout}s: {locator}")
            return False
    
    def wait_for_element_invisible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Wait for element to be invisible"""
        timeout = timeout or self.config.timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            self.logger.debug(f"Element became invisible: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Element still visible after {timeout}s: {locator}")
            return False
    
    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Wait for element to be clickable"""
        timeout = timeout or self.config.timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.logger.debug(f"Element became clickable: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Element not clickable within {timeout}s: {locator}")
            return False
    
    def wait_for_text_present(self, locator: Tuple[str, str], text: str, timeout: int = None) -> bool:
        """Wait for specific text to be present in element"""
        timeout = timeout or self.config.timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            self.logger.debug(f"Text '{text}' present in element: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Text '{text}' not present in element within {timeout}s: {locator}")
            return False
    
    # Scroll and viewport methods
    def scroll_to_element(self, element: WebElement):
        """Scroll element into view"""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.2)  # Small delay for scroll completion
        self.logger.debug("Scrolled element into view")
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.logger.debug("Scrolled to top of page")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.logger.debug("Scrolled to bottom of page")
    
    def scroll_by_pixels(self, x: int, y: int):
        """Scroll by specified pixels"""
        self.driver.execute_script(f"window.scrollBy({x}, {y});")
        self.logger.debug(f"Scrolled by {x}, {y} pixels")
    
    # Validation methods
    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """Check if element is visible"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def is_element_enabled(self, locator: Tuple[str, str]) -> bool:
        """Check if element is enabled"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_enabled()
        except NoSuchElementException:
            return False
    
    def is_element_selected(self, locator: Tuple[str, str]) -> bool:
        """Check if element is selected (checkboxes, radio buttons)"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_selected()
        except NoSuchElementException:
            return False
    
    # Utility methods
    def get_page_title(self) -> str:
        """Get current page title"""
        return self.driver.title
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    def execute_javascript(self, script: str, *args) -> Any:
        """Execute JavaScript and return result"""
        return self.driver.execute_script(script, *args)
    
    def take_screenshot(self, filename: str = None) -> str:
        """Take screenshot and return file path"""
        from .driver_manager import take_screenshot
        return take_screenshot(filename)
    
    def hover(self, locator: Tuple[str, str]):
        """Hover over element"""
        element = self.find_visible_element(locator)
        self.actions.move_to_element(element).perform()
        self.logger.debug(f"Hovered over element: {locator}")
    
    def drag_and_drop(self, source_locator: Tuple[str, str], target_locator: Tuple[str, str]):
        """Drag element from source to target"""
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        self.actions.drag_and_drop(source, target).perform()
        self.logger.debug(f"Dragged from {source_locator} to {target_locator}")
    
    def wait_and_assert_element_text(self, locator: Tuple[str, str], expected_text: str, timeout: int = None):
        """Wait for element and assert its text content"""
        timeout = timeout or self.config.timeout
        
        if self.wait_for_element_visible(locator, timeout):
            actual_text = self.get_text(locator)
            assertion_manager.assert_equals(
                actual_text, 
                expected_text, 
                f"Element text mismatch for {locator}"
            )
        else:
            assertion_manager.hard_assert(
                False, 
                f"Element not visible within {timeout}s: {locator}"
            )
    
    def wait_and_assert_page_title(self, expected_title: str, timeout: int = None):
        """Wait for and assert page title"""
        timeout = timeout or self.config.timeout
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.title_is(expected_title)
            )
            assertion_manager.hard_assert(
                True, 
                f"Page title is correct: '{expected_title}'"
            )
        except TimeoutException:
            actual_title = self.get_page_title()
            assertion_manager.hard_assert(
                False, 
                f"Page title mismatch. Expected: '{expected_title}', Actual: '{actual_title}'"
            )