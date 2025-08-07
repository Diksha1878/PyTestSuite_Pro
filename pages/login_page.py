"""
Login Page Object Model

This module contains the LoginPage class for handling login functionality
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional

from core import BasePage, assertion_manager


class LoginPage(BasePage):
    """Login page object with login functionality"""
    
    # Page URL and identifiers
    page_url = "login"
    page_title = "Login - Application"
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    LOGOUT_BUTTON = (By.ID, "logout-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    
    # Form validation locators
    USERNAME_ERROR = (By.CSS_SELECTOR, "#username + .error")
    PASSWORD_ERROR = (By.CSS_SELECTOR, "#password + .error")
    
    # Loading and state indicators
    LOADING_SPINNER = (By.CSS_SELECTOR, ".loading-spinner")
    LOGIN_FORM = (By.ID, "login-form")
    
    def __init__(self, driver: WebDriver = None):
        super().__init__(driver)
        self.page_load_element = self.LOGIN_FORM
    
    # Navigation methods
    def open_login_page(self):
        """Navigate to login page"""
        self.open(self.page_url)
        self.wait_for_page_load()
        self.logger.info("Login page opened")
    
    # Input methods
    def enter_username(self, username: str):
        """Enter username in the username field"""
        self.type(self.USERNAME_INPUT, username)
        self.logger.info(f"Entered username: {username}")
    
    def enter_password(self, password: str):
        """Enter password in the password field"""
        self.type(self.PASSWORD_INPUT, password)
        self.logger.info("Password entered")
    
    def clear_username(self):
        """Clear username field"""
        self.clear(self.USERNAME_INPUT)
        self.logger.info("Username field cleared")
    
    def clear_password(self):
        """Clear password field"""
        self.clear(self.PASSWORD_INPUT)
        self.logger.info("Password field cleared")
    
    # Action methods
    def click_login_button(self):
        """Click the login button"""
        self.click(self.LOGIN_BUTTON)
        self.logger.info("Login button clicked")
    
    def click_forgot_password(self):
        """Click forgot password link"""
        self.click(self.FORGOT_PASSWORD_LINK)
        self.logger.info("Forgot password link clicked")
    
    def toggle_remember_me(self):
        """Toggle remember me checkbox"""
        self.click(self.REMEMBER_ME_CHECKBOX)
        is_checked = self.is_element_selected(self.REMEMBER_ME_CHECKBOX)
        self.logger.info(f"Remember me toggled: {is_checked}")
        return is_checked
    
    def logout(self):
        """Logout if logout button is present"""
        if self.is_element_present(self.LOGOUT_BUTTON):
            self.click(self.LOGOUT_BUTTON)
            self.logger.info("Logout button clicked")
            return True
        else:
            self.logger.warning("Logout button not found")
            return False
    
    # Composite action methods
    def login(self, username: str, password: str, remember_me: bool = False) -> bool:
        """
        Perform complete login action
        
        Args:
            username: Username to login with
            password: Password for the user
            remember_me: Whether to check remember me checkbox
            
        Returns:
            bool: True if login appears successful, False otherwise
        """
        try:
            self.logger.info(f"Attempting login with username: {username}")
            
            # Clear existing values and enter credentials
            self.clear_username()
            self.clear_password()
            self.enter_username(username)
            self.enter_password(password)
            
            # Handle remember me option
            if remember_me:
                current_state = self.is_element_selected(self.REMEMBER_ME_CHECKBOX)
                if not current_state:
                    self.toggle_remember_me()
            
            # Click login button
            self.click_login_button()
            
            # Wait for login to complete (either success or error)
            self.wait_for_login_completion()
            
            # Check if login was successful
            success = self.is_login_successful()
            
            if success:
                self.logger.info("Login completed successfully")
            else:
                error_msg = self.get_error_message()
                self.logger.warning(f"Login failed: {error_msg}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Login process failed with exception: {str(e)}")
            return False
    
    def quick_login(self, username: str = None, password: str = None):
        """
        Quick login using default credentials from config if not provided
        """
        username = username or self.config.username
        password = password or self.config.password
        
        return self.login(username, password)
    
    # Validation and state methods
    def wait_for_login_completion(self, timeout: int = 10):
        """Wait for login process to complete"""
        # Wait for loading spinner to disappear if present
        if self.is_element_present(self.LOADING_SPINNER):
            self.wait_for_element_invisible(self.LOADING_SPINNER, timeout)
        
        # Wait for either success message or error message to appear
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: (
                    self.is_element_present(self.ERROR_MESSAGE) or
                    self.is_element_present(self.SUCCESS_MESSAGE) or
                    not self.is_element_present(self.LOGIN_FORM)
                )
            )
        except Exception:
            self.logger.warning("Login completion wait timed out")
    
    def is_login_successful(self) -> bool:
        """Check if login was successful"""
        # Login is successful if:
        # 1. No error message is displayed
        # 2. Success message is displayed OR login form is no longer present
        # 3. Current URL has changed from login page
        
        has_error = self.is_element_present(self.ERROR_MESSAGE)
        has_success = self.is_element_present(self.SUCCESS_MESSAGE)
        login_form_present = self.is_element_present(self.LOGIN_FORM)
        current_url = self.get_current_url()
        
        # If there's an error message, login failed
        if has_error:
            return False
        
        # If there's a success message, login succeeded
        if has_success:
            return True
        
        # If login form is gone and URL changed, likely successful
        if not login_form_present and "login" not in current_url.lower():
            return True
        
        return False
    
    def get_error_message(self) -> str:
        """Get error message text if present"""
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def get_success_message(self) -> str:
        """Get success message text if present"""
        if self.is_element_present(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""
    
    def get_username_error(self) -> str:
        """Get username field validation error"""
        if self.is_element_present(self.USERNAME_ERROR):
            return self.get_text(self.USERNAME_ERROR)
        return ""
    
    def get_password_error(self) -> str:
        """Get password field validation error"""
        if self.is_element_present(self.PASSWORD_ERROR):
            return self.get_text(self.PASSWORD_ERROR)
        return ""
    
    def is_username_field_highlighted(self) -> bool:
        """Check if username field has error highlighting"""
        username_element = self.find_element(self.USERNAME_INPUT)
        css_class = username_element.get_attribute("class") or ""
        return "error" in css_class.lower() or "invalid" in css_class.lower()
    
    def is_password_field_highlighted(self) -> bool:
        """Check if password field has error highlighting"""
        password_element = self.find_element(self.PASSWORD_INPUT)
        css_class = password_element.get_attribute("class") or ""
        return "error" in css_class.lower() or "invalid" in css_class.lower()
    
    def is_remember_me_checked(self) -> bool:
        """Check if remember me checkbox is selected"""
        return self.is_element_selected(self.REMEMBER_ME_CHECKBOX)
    
    # Assertion methods for validation
    def assert_login_page_loaded(self):
        """Assert that login page is properly loaded"""
        assertion_manager.assert_true(
            self.is_element_present(self.LOGIN_FORM),
            "Login form should be present on login page"
        )
        assertion_manager.assert_true(
            self.is_element_present(self.USERNAME_INPUT),
            "Username input should be present"
        )
        assertion_manager.assert_true(
            self.is_element_present(self.PASSWORD_INPUT),
            "Password input should be present"
        )
        assertion_manager.assert_true(
            self.is_element_present(self.LOGIN_BUTTON),
            "Login button should be present"
        )
    
    def assert_login_successful(self):
        """Assert that login was successful"""
        assertion_manager.assert_true(
            self.is_login_successful(),
            "Login should be successful"
        )
        
        current_url = self.get_current_url()
        assertion_manager.assert_false(
            "login" in current_url.lower(),
            "Should be redirected away from login page after successful login"
        )
    
    def assert_login_failed_with_error(self, expected_error: str = None):
        """Assert that login failed with specific error message"""
        assertion_manager.assert_false(
            self.is_login_successful(),
            "Login should have failed"
        )
        
        error_message = self.get_error_message()
        assertion_manager.assert_true(
            bool(error_message),
            "Error message should be displayed after failed login"
        )
        
        if expected_error:
            assertion_manager.assert_contains(
                error_message.lower(),
                expected_error.lower(),
                f"Error message should contain expected text"
            )
    
    def assert_validation_errors_present(self, username_error: bool = False, password_error: bool = False):
        """Assert field validation errors are present"""
        if username_error:
            assertion_manager.assert_true(
                bool(self.get_username_error()),
                "Username validation error should be present"
            )
        
        if password_error:
            assertion_manager.assert_true(
                bool(self.get_password_error()),
                "Password validation error should be present"
            )
    
    # Utility methods
    def get_login_form_data(self) -> dict:
        """Get current values from login form"""
        return {
            'username': self.get_attribute(self.USERNAME_INPUT, 'value') or '',
            'password': self.get_attribute(self.PASSWORD_INPUT, 'value') or '',
            'remember_me': self.is_remember_me_checked()
        }
    
    def is_login_form_empty(self) -> bool:
        """Check if login form fields are empty"""
        form_data = self.get_login_form_data()
        return not form_data['username'] and not form_data['password']