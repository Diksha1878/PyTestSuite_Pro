"""
Login UI Tests for PyTestSuite Pro

This module contains comprehensive login functionality tests
with different assertion strategies and test groupings.
"""

import pytest
from core import UITest, assertion_manager
from pages import LoginPage, DashboardPage
from keywords import WebActions, AssertionKeywords, DataActions


class TestLogin(UITest):
    """Login functionality test suite"""
    
    def setup_method(self, method):
        """Setup before each test method"""
        super().setup_method(method)
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.web_actions = WebActions()
        self.assertions = AssertionKeywords()
        self.data_actions = DataActions()
    
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.ui
    def test_httpbin_forms_page_loads(self):
        """
        Test that httpbin.org forms page loads successfully
        Priority: Critical - Basic UI functionality
        """
        # Navigate to httpbin.org forms page
        forms_url = f"{self.config.base_url}/forms/post"
        self.navigate_to(forms_url)
        
        # Wait for page to load
        self.wait_for_page_load()
        
        # Verify page loaded successfully
        current_url = self.get_current_url()
        assertion_manager.hard_assert(
            "httpbin.org" in current_url,
            f"Should navigate to httpbin.org (current: {current_url})"
        )
        
        # Verify page title
        page_title = self.get_page_title()
        assertion_manager.soft_assert(
            "httpbin" in page_title.lower(),
            f"Page title should contain 'httpbin' (actual: {page_title})"
        )
        
        # Verify form elements are present
        from selenium.webdriver.common.by import By
        
        try:
            form_element = self.driver.find_element(By.TAG_NAME, "form")
            assertion_manager.hard_assert(
                form_element is not None,
                "Form element should be present on the page"
            )
        except Exception as e:
            assertion_manager.soft_assert(
                False,
                f"Could not find form element: {str(e)}"
            )
        
        # Take screenshot for documentation
        self.take_screenshot("httpbin_forms_page")
    
    @pytest.mark.smoke
    @pytest.mark.high
    @pytest.mark.ui
    def test_form_interaction(self):
        """
        Test basic form interaction on httpbin.org
        Priority: High - UI interaction functionality
        """
        # Navigate to httpbin.org forms page
        forms_url = f"{self.config.base_url}/forms/post"
        self.navigate_to(forms_url)
        
        # Wait for page to load
        self.wait_for_page_load()
        
        from selenium.webdriver.common.by import By
        
        try:
            # Find and interact with form elements
            custname_field = self.driver.find_element(By.NAME, "custname")
            custtel_field = self.driver.find_element(By.NAME, "custtel")
            
            # Enter test data
            test_name = "Test User"
            test_phone = "123-456-7890"
            
            custname_field.clear()
            custname_field.send_keys(test_name)
            
            custtel_field.clear()
            custtel_field.send_keys(test_phone)
            
            # Verify data was entered
            entered_name = custname_field.get_attribute("value")
            entered_phone = custtel_field.get_attribute("value")
            
            assertion_manager.hard_assert(
                entered_name == test_name,
                f"Name field should contain '{test_name}' (actual: '{entered_name}')"
            )
            
            assertion_manager.hard_assert(
                entered_phone == test_phone,
                f"Phone field should contain '{test_phone}' (actual: '{entered_phone}')"
            )
            
            # Take screenshot showing form interaction
            self.take_screenshot("form_interaction")
            
        except Exception as e:
            assertion_manager.soft_assert(
                False,
                f"Form interaction failed: {str(e)}"
            )

    @pytest.mark.regression
    @pytest.mark.high
    @pytest.mark.ui
    def test_invalid_login_credentials(self, assertions):
        """
        Test login failure with invalid credentials
        Priority: High - Security validation
        """
        # Navigate to login page
        self.login_page.open_login_page()
        
        # Verify login page loaded
        self.login_page.assert_login_page_loaded()
        
        # Attempt login with invalid credentials
        login_success = self.login_page.login("invalid_user", "invalid_password")
        
        # Assert login failed
        assertion_manager.hard_assert(
            not login_success,
            "Login should fail with invalid credentials"
        )
        
        # Verify error message is displayed
        self.login_page.assert_login_failed_with_error("Invalid")
        
        # Verify user remains on login page
        self.assertions.assert_page_url_contains("login")
    
    @pytest.mark.regression
    @pytest.mark.medium
    @pytest.mark.ui
    def test_empty_credentials_validation(self, assertions):
        """
        Test form validation with empty credentials
        Priority: Medium - Form validation
        """
        # Navigate to login page
        self.login_page.open_login_page()
        
        # Clear any existing values
        self.login_page.clear_username()
        self.login_page.clear_password()
        
        # Attempt to login with empty fields
        self.login_page.click_login_button()
        
        # Wait for validation to trigger
        self.wait_for_page_load()
        
        # Verify validation errors (using soft assertions for UI validation)
        self.login_page.assert_validation_errors_present(
            username_error=True, 
            password_error=True
        )
        
        # Verify form highlighting (soft assertion as it's UI-specific)
        assertion_manager.soft_assert(
            self.login_page.is_username_field_highlighted(),
            "Username field should be highlighted for validation error"
        )
        
        assertion_manager.soft_assert(
            self.login_page.is_password_field_highlighted(),
            "Password field should be highlighted for validation error"
        )
    
    @pytest.mark.regression
    @pytest.mark.medium
    @pytest.mark.ui
    def test_remember_me_functionality(self, assertions):
        """
        Test remember me checkbox functionality
        Priority: Medium - User experience feature
        """
        # Navigate to login page
        self.login_page.open_login_page()
        
        # Verify remember me checkbox is present
        assertion_manager.soft_assert(
            self.login_page.is_element_present(self.login_page.REMEMBER_ME_CHECKBOX),
            "Remember me checkbox should be present"
        )
        
        # Test checkbox toggle
        initial_state = self.login_page.is_remember_me_checked()
        self.login_page.toggle_remember_me()
        new_state = self.login_page.is_remember_me_checked()
        
        assertion_manager.soft_assert(
            initial_state != new_state,
            "Remember me checkbox should toggle state"
        )
        
        # Login with remember me checked
        if not new_state:
            self.login_page.toggle_remember_me()
        
        login_success = self.login_page.quick_login(remember_me=True)
        
        assertion_manager.hard_assert(
            login_success,
            "Login should work with remember me option"
        )
    
    @pytest.mark.regression
    @pytest.mark.low
    @pytest.mark.ui
    def test_forgot_password_link(self, assertions):
        """
        Test forgot password link functionality
        Priority: Low - Secondary functionality
        """
        # Navigate to login page
        self.login_page.open_login_page()
        
        # Verify forgot password link is present
        assertion_manager.soft_assert(
            self.login_page.is_element_present(self.login_page.FORGOT_PASSWORD_LINK),
            "Forgot password link should be present"
        )
        
        # Click forgot password link
        self.login_page.click_forgot_password()
        
        # Verify navigation to forgot password page (soft assertion)
        current_url = self.get_current_url()
        assertion_manager.soft_assert(
            "forgot" in current_url.lower() or "reset" in current_url.lower(),
            "Should navigate to forgot password page"
        )
    
    @pytest.mark.smoke
    @pytest.mark.high
    @pytest.mark.ui
    @pytest.mark.security
    def test_password_field_masking(self, assertions):
        """
        Test password field input masking for security
        Priority: High - Security feature
        """
        # Navigate to login page
        self.login_page.open_login_page()
        
        # Type password and verify it's masked
        test_password = "TestPassword123"
        self.login_page.enter_password(test_password)
        
        # Check password field type attribute
        password_type = self.login_page.get_attribute(
            self.login_page.PASSWORD_INPUT, "type"
        )
        
        assertion_manager.hard_assert(
            password_type.lower() == "password",
            "Password field should have type='password' for masking"
        )
        
        # Verify password value is not visible in page source (security check)
        page_source = self.get_page_source()
        assertion_manager.hard_assert(
            test_password not in page_source,
            "Password should not be visible in plain text in page source"
        )
    
    @pytest.mark.performance
    @pytest.mark.medium
    @pytest.mark.ui
    def test_login_response_time(self, assertions):
        """
        Test login process response time
        Priority: Medium - Performance validation
        """
        import time
        
        # Navigate to login page
        self.login_page.open_login_page()
        
        # Measure login time
        start_time = time.time()
        
        login_success = self.login_page.quick_login()
        
        end_time = time.time()
        login_time = end_time - start_time
        
        # Assert login was successful first
        assertion_manager.hard_assert(
            login_success,
            "Login should be successful for performance test"
        )
        
        # Performance assertion (warning level - shouldn't fail test)
        assertion_manager.warning_assert(
            login_time < 5.0,
            f"Login should complete within 5 seconds (actual: {login_time:.2f}s)"
        )
        
        self.logger.info(f"Login completed in {login_time:.2f} seconds")
    
    @pytest.mark.regression
    @pytest.mark.medium
    @pytest.mark.ui
    @pytest.mark.cross_browser
    def test_login_form_layout(self, assertions):
        """
        Test login form layout and elements
        Priority: Medium - UI consistency
        """
        # Navigate to login page
        self.login_page.open_login_page()
        
        # Verify all form elements are present (soft assertions for UI)
        form_elements = [
            (self.login_page.USERNAME_INPUT, "Username input"),
            (self.login_page.PASSWORD_INPUT, "Password input"),
            (self.login_page.LOGIN_BUTTON, "Login button"),
            (self.login_page.REMEMBER_ME_CHECKBOX, "Remember me checkbox"),
            (self.login_page.FORGOT_PASSWORD_LINK, "Forgot password link")
        ]
        
        for locator, description in form_elements:
            assertion_manager.soft_assert(
                self.login_page.is_element_present(locator),
                f"{description} should be present on login form"
            )
            
            assertion_manager.soft_assert(
                self.login_page.is_element_visible(locator),
                f"{description} should be visible on login form"
            )
    
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.ui
    @pytest.mark.test_data("users.json")
    def test_login_with_test_data(self, assertions):
        """
        Test login with various user data from test data file
        Priority: Critical - Data-driven testing
        """
        # Load test data
        users_data = self.data_actions.load_json_data("users.json")
        
        # Get valid user data
        valid_user = users_data.get("valid_users", [{}])[0]
        
        if not valid_user:
            pytest.skip("No valid user data available for test")
        
        # Navigate to login page
        self.login_page.open_login_page()
        
        # Login with test data user
        login_success = self.login_page.login(
            valid_user.get("username", ""),
            valid_user.get("password", "")
        )
        
        assertion_manager.hard_assert(
            login_success,
            f"Login should succeed with test data user: {valid_user.get('username')}"
        )
        
        # Verify expected user role or permissions if available
        expected_role = valid_user.get("role")
        if expected_role:
            # This would depend on how roles are displayed in your application
            assertion_manager.soft_assert(
                True,  # Placeholder for role verification logic
                f"User should have role: {expected_role}"
            )
    
    def teardown_method(self, method):
        """Cleanup after each test method"""
        try:
            # Logout if logged in
            if "dashboard" in self.get_current_url().lower():
                self.dashboard_page.logout()
        except Exception as e:
            self.logger.warning(f"Logout during teardown failed: {str(e)}")
        
        super().teardown_method(method)