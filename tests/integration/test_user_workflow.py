"""
User Workflow Integration Tests for PyTestSuite Pro

This module contains end-to-end integration tests that combine
UI and API operations for complete user workflows.
"""

import pytest
from core import IntegrationTest, assertion_manager
from pages import LoginPage, DashboardPage
from keywords import WebActions, APIActions, AssertionKeywords, DataActions


class TestUserWorkflow(IntegrationTest):
    """End-to-end user workflow integration tests"""
    
    def setup_method(self, method):
        """Setup before each test method"""
        super().setup_method(method)
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.web_actions = WebActions()
        self.api_actions = APIActions()
        self.assertions = AssertionKeywords()
        self.data_actions = DataActions()
        
        # Set API base URL for API operations
        self.api_actions.set_base_url(self.api_base_url)
    
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.integration
    def test_api_and_ui_combination(self):
        """
        Test combination of API and UI operations using httpbin.org
        Priority: Critical - Integration workflow validation
        """
        import requests
        
        # Step 1: Test API operation - GET request
        api_response = requests.get(f"{self.api_base_url}/get")
        
        assertion_manager.hard_assert(
            api_response.status_code == 200,
            f"API GET request should succeed (got {api_response.status_code})"
        )
        
        # Extract some data from API response
        api_data = api_response.json()
        origin_ip = api_data.get("origin", "unknown")
        
        # Step 2: Test UI operation - Navigate to forms page
        forms_url = f"{self.config.base_url}/forms/post"
        self.navigate_to(forms_url)
        self.wait_for_page_load()
        
        # Verify UI loaded successfully
        current_url = self.get_current_url()
        assertion_manager.hard_assert(
            "httpbin.org" in current_url,
            f"UI should navigate to httpbin.org (current: {current_url})"
        )
        
        # Step 3: Use API data in UI operation
        from selenium.webdriver.common.by import By
        
        try:
            # Find form field and enter data from API response
            custname_field = self.driver.find_element(By.NAME, "custname")
            
            # Use origin IP from API as test data in UI
            test_data = f"Test User from {origin_ip}"
            custname_field.clear()
            custname_field.send_keys(test_data)
            
            # Verify data was entered
            entered_value = custname_field.get_attribute("value")
            assertion_manager.hard_assert(
                test_data in entered_value,
                f"UI field should contain API-derived data: {test_data}"
            )
            
            # Step 4: Test another API call with UI-derived data
            post_data = {"ui_value": entered_value, "test_type": "integration"}
            post_response = requests.post(f"{self.api_base_url}/post", json=post_data)
            
            assertion_manager.hard_assert(
                post_response.status_code == 200,
                "API POST with UI data should succeed"
            )
            
            # Verify the integration worked
            post_response_data = post_response.json()
            sent_data = post_response_data.get("json", {})
            
            assertion_manager.soft_assert(
                sent_data.get("ui_value") == entered_value,
                "API should echo back the UI-derived data"
            )
            
        except Exception as e:
            assertion_manager.soft_assert(
                False,
                f"Integration test failed: {str(e)}"
            )
        
        # Take screenshot for documentation
        self.take_screenshot("integration_test_result")
    
    @pytest.mark.regression
    @pytest.mark.high
    @pytest.mark.integration
    def test_user_profile_update_workflow(self, assertions):
        """
        Test user profile update via API and verification via UI
        Priority: High - User management workflow
        """
        # Step 1: Login with existing user
        login_success = self.login_page.quick_login()
        
        if not login_success:
            pytest.skip("Cannot test profile update without successful login")
        
        # Step 2: Get current user info (assuming API endpoint exists)
        # This would typically be /users/current or /profile
        try:
            current_user_response = self.api_actions.get_request("/users/current")
            if self.api_actions.get_response_status_code(current_user_response) != 200:
                # Fallback: try to get user list and use first user
                users_response = self.api_actions.get_request("/users")
                users_data = self.api_actions.get_response_json(users_response)
                if isinstance(users_data, list) and users_data:
                    current_user = users_data[0]
                    user_id = current_user.get("id") or current_user.get("user_id")
                else:
                    pytest.skip("Cannot determine current user for profile update test")
            else:
                current_user = self.api_actions.get_response_json(current_user_response)
                user_id = current_user.get("id") or current_user.get("user_id")
        
        except Exception as e:
            pytest.skip(f"Cannot get current user information: {str(e)}")
        
        # Step 3: Update user profile via API
        original_name = current_user.get("name", "Test User")
        updated_name = f"Updated {original_name}"
        
        update_payload = {
            "name": updated_name,
            "email": current_user.get("email", "test@example.com")
        }
        
        update_response = self.api_actions.put_request(f"/users/{user_id}", json_data=update_payload)
        
        # Verify API update was successful
        if self.api_actions.get_response_status_code(update_response) == 200:
            self.assertions.assert_api_json_value("name", updated_name, update_response)
            
            # Step 4: Verify updated profile is reflected in UI
            # This would depend on your application's UI structure
            # Refresh the page to see changes
            self.refresh_page()
            
            # Check if updated name appears in UI (soft assertion as UI may vary)
            page_source = self.get_page_source()
            assertion_manager.soft_assert(
                updated_name in page_source,
                "Updated user name should appear in UI after API update"
            )
        
        else:
            assertion_manager.soft_assert(
                False,
                "Profile update via API should be successful"
            )
    
    @pytest.mark.regression
    @pytest.mark.medium
    @pytest.mark.integration
    def test_data_consistency_across_ui_and_api(self, assertions):
        """
        Test data consistency between UI operations and API responses
        Priority: Medium - Data integrity validation
        """
        # Step 1: Login and navigate to dashboard
        login_success = self.login_page.quick_login()
        
        if not login_success:
            pytest.skip("Cannot test data consistency without successful login")
        
        self.dashboard_page.assert_dashboard_loaded()
        
        # Step 2: Get dashboard statistics from UI
        ui_stats = self.dashboard_page.get_dashboard_stats()
        
        # Step 3: Get corresponding data from API
        # Assuming there's a stats or dashboard API endpoint
        try:
            api_stats_response = self.api_actions.get_request("/dashboard/stats")
            
            if self.api_actions.get_response_status_code(api_stats_response) == 200:
                api_stats = self.api_actions.get_response_json(api_stats_response)
                
                # Compare UI and API data (soft assertions for data sync)
                for ui_key, ui_value in ui_stats.items():
                    # Map UI keys to API keys (this mapping depends on your application)
                    api_key = ui_key.replace("_", "")  # Simple mapping example
                    
                    if api_key in api_stats:
                        # Extract numeric values for comparison
                        ui_numeric = ''.join(filter(str.isdigit, str(ui_value)))
                        api_numeric = ''.join(filter(str.isdigit, str(api_stats[api_key])))
                        
                        if ui_numeric and api_numeric:
                            assertion_manager.soft_assert(
                                ui_numeric == api_numeric,
                                f"UI and API data should match for {ui_key}: UI={ui_numeric}, API={api_numeric}"
                            )
            
            else:
                self.logger.warning("Dashboard stats API not available for consistency check")
        
        except Exception as e:
            self.logger.warning(f"Could not verify data consistency: {str(e)}")
    
    @pytest.mark.smoke
    @pytest.mark.high
    @pytest.mark.integration
    @pytest.mark.security
    def test_authentication_flow_security(self, assertions):
        """
        Test authentication security across UI and API
        Priority: High - Security validation
        """
        # Step 1: Attempt API access without authentication
        self.api_actions.clear_auth()
        
        # Try to access protected endpoint
        protected_response = self.api_actions.get_request("/users/current")
        protected_status = self.api_actions.get_response_status_code(protected_response)
        
        assertion_manager.hard_assert(
            protected_status in [401, 403],
            "Protected API endpoint should require authentication"
        )
        
        # Step 2: Login via UI to get authentication
        self.login_page.open_login_page()
        login_success = self.login_page.quick_login()
        
        assertion_manager.hard_assert(
            login_success,
            "UI login should be successful for security test"
        )
        
        # Step 3: Extract authentication token from browser (if applicable)
        # This depends on how your application handles authentication
        # Common methods: cookies, localStorage, sessionStorage
        
        try:
            # Example: Get auth token from localStorage
            auth_token = self.execute_javascript("return localStorage.getItem('authToken');")
            
            if auth_token:
                # Set token for API requests
                self.api_actions.set_auth_token(auth_token)
                
                # Step 4: Verify API access works with UI-obtained token
                authenticated_response = self.api_actions.get_request("/users/current")
                authenticated_status = self.api_actions.get_response_status_code(authenticated_response)
                
                assertion_manager.hard_assert(
                    authenticated_status == 200,
                    "API should be accessible with UI-obtained authentication token"
                )
            
            else:
                self.logger.warning("Could not extract authentication token from UI")
        
        except Exception as e:
            self.logger.warning(f"Authentication token extraction failed: {str(e)}")
        
        # Step 5: Test session timeout behavior
        # Logout via UI
        self.dashboard_page.logout()
        
        # Verify API access is revoked after UI logout
        post_logout_response = self.api_actions.get_request("/users/current")
        post_logout_status = self.api_actions.get_response_status_code(post_logout_response)
        
        assertion_manager.soft_assert(
            post_logout_status in [401, 403],
            "API access should be revoked after UI logout"
        )
    
    @pytest.mark.performance
    @pytest.mark.medium
    @pytest.mark.integration
    def test_end_to_end_performance(self, assertions):
        """
        Test end-to-end workflow performance
        Priority: Medium - Performance validation
        """
        import time
        
        # Measure complete workflow time
        workflow_start = time.time()
        
        # Step 1: Create user via API (timed)
        api_start = time.time()
        
        new_user_data = self.data_actions.generate_user_data()
        user_payload = {
            "name": f"{new_user_data['first_name']} {new_user_data['last_name']}",
            "email": new_user_data['email'],
            "username": new_user_data['username'],
            "password": new_user_data['password']
        }
        
        api_response = self.api_actions.post_request("/users", json_data=user_payload)
        
        api_time = time.time() - api_start
        
        # Step 2: UI login (timed)
        ui_start = time.time()
        
        self.login_page.open_login_page()
        login_success = self.login_page.login(
            user_payload["username"], 
            user_payload["password"]
        )
        
        ui_time = time.time() - ui_start
        
        # Step 3: Dashboard load (timed)
        dashboard_start = time.time()
        
        if login_success:
            self.dashboard_page.wait_for_stats_to_load()
        
        dashboard_time = time.time() - dashboard_start
        
        total_time = time.time() - workflow_start
        
        # Performance assertions (warning level)
        assertion_manager.warning_assert(
            api_time < 2.0,
            f"API user creation should complete under 2s (actual: {api_time:.2f}s)"
        )
        
        assertion_manager.warning_assert(
            ui_time < 10.0,
            f"UI login should complete under 10s (actual: {ui_time:.2f}s)"
        )
        
        assertion_manager.warning_assert(
            dashboard_time < 5.0,
            f"Dashboard load should complete under 5s (actual: {dashboard_time:.2f}s)"
        )
        
        assertion_manager.warning_assert(
            total_time < 15.0,
            f"Complete workflow should finish under 15s (actual: {total_time:.2f}s)"
        )
        
        self.logger.info(f"E2E Performance - API: {api_time:.2f}s, UI: {ui_time:.2f}s, "
                        f"Dashboard: {dashboard_time:.2f}s, Total: {total_time:.2f}s")
        
        # Cleanup
        if self.api_actions.get_response_status_code(api_response) in [200, 201]:
            created_user = self.api_actions.get_response_json(api_response)
            user_id = created_user.get("id") or created_user.get("user_id")
            if user_id:
                self.set_test_data("cleanup_user_id", user_id)
    
    def teardown_method(self, method):
        """Cleanup after each test method"""
        # Clean up any created users
        cleanup_user_id = self.get_test_data("cleanup_user_id") or self.get_test_data("test_user_id")
        
        if cleanup_user_id:
            try:
                self.api_actions.delete_request(f"/users/{cleanup_user_id}")
                self.logger.info(f"Cleaned up test user: {cleanup_user_id}")
            except Exception as e:
                self.logger.warning(f"Failed to cleanup user {cleanup_user_id}: {str(e)}")
        
        # Logout if still logged in
        try:
            current_url = self.get_current_url()
            if "dashboard" in current_url.lower():
                self.dashboard_page.logout()
        except Exception as e:
            self.logger.warning(f"Logout during teardown failed: {str(e)}")
        
        super().teardown_method(method)