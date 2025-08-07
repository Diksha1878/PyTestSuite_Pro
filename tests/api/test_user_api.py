"""
User API Tests for PyTestSuite Pro

This module contains comprehensive API tests for user-related endpoints
with different HTTP methods and response validations.
"""

import pytest
import json
from core import APITest, assertion_manager
from keywords import APIActions, AssertionKeywords, DataActions


class TestUserAPI(APITest):
    """User API endpoints test suite"""
    
    def setup_method(self, method):
        """Setup before each test method"""
        super().setup_method(method)
        self.api_actions = APIActions()
        self.assertions = AssertionKeywords()
        self.data_actions = DataActions()
        
        # Set API base URL
        self.api_actions.set_base_url(self.api_base_url)
    
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.api
    def test_get_request_success(self):
        """
        Test GET request to httpbin.org returns successful response
        Priority: Critical - Basic API functionality
        """
        import requests
        
        # Send GET request to httpbin.org/get
        response = requests.get(f"{self.api_base_url}/get")
        
        # Assert successful status code
        assertion_manager.hard_assert(
            response.status_code == 200,
            f"GET request should return 200 status (got {response.status_code})"
        )
        
        # Verify response contains expected data structure
        json_data = response.json()
        assertion_manager.hard_assert(
            isinstance(json_data, dict),
            "Response should be a JSON object"
        )
        
        # Verify httpbin.org response structure
        expected_fields = ["args", "headers", "origin", "url"]
        for field in expected_fields:
            assertion_manager.soft_assert(
                field in json_data,
                f"Response should contain {field} field"
            )
        
        # Verify response time (warning level)
        assertion_manager.warning_assert(
            response.elapsed.total_seconds() < 5.0,
            f"Request should complete under 5s (actual: {response.elapsed.total_seconds():.2f}s)"
        )
    
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.api
    def test_post_request_success(self):
        """
        Test POST request to httpbin.org returns successful response
        Priority: Critical - Basic API functionality
        """
        import requests
        
        # Test data to send
        test_data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test POST request"
        }
        
        # Send POST request to httpbin.org/post
        response = requests.post(f"{self.api_base_url}/post", json=test_data)
        
        # Assert successful status code
        assertion_manager.hard_assert(
            response.status_code == 200,
            f"POST request should return 200 status (got {response.status_code})"
        )
        
        # Verify response contains expected data structure
        json_response = response.json()
        assertion_manager.hard_assert(
            isinstance(json_response, dict),
            "Response should be a JSON object"
        )
        
        # Verify the data we sent is echoed back in the response
        assertion_manager.hard_assert(
            "json" in json_response,
            "Response should contain 'json' field with our sent data"
        )
        
        if "json" in json_response:
            sent_data = json_response["json"]
            assertion_manager.soft_assert(
                sent_data.get("name") == test_data["name"],
                f"Sent name should match response: {test_data['name']}"
            )
            assertion_manager.soft_assert(
                sent_data.get("email") == test_data["email"],
                f"Sent email should match response: {test_data['email']}"
            )

    @pytest.mark.regression
    @pytest.mark.high
    @pytest.mark.api
    def test_get_user_by_id_success(self, assertions):
        """
        Test GET /users/{id} endpoint returns specific user
        Priority: Critical - Core API functionality
        """
        # First get list of users to get a valid ID
        users_response = self.api_actions.get_request("/users")
        self.assertions.assert_api_status_code(200, users_response)
        
        users_data = self.api_actions.get_response_json(users_response)
        
        # Extract user ID (handling different response formats)
        if isinstance(users_data, dict) and "users" in users_data:
            users_list = users_data["users"]
        else:
            users_list = users_data
        
        if not users_list:
            pytest.skip("No users available to test individual user retrieval")
        
        test_user_id = users_list[0].get("id") or users_list[0].get("user_id") or "1"
        
        # Get specific user
        response = self.api_actions.get_request(f"/users/{test_user_id}")
        
        # Assert successful response
        self.assertions.assert_api_status_code(200, response)
        
        # Verify user data structure
        user_data = self.api_actions.get_response_json(response)
        
        expected_fields = ["id", "name", "email"]
        for field in expected_fields:
            if field in user_data or field.replace("name", "username") in user_data:
                assertion_manager.soft_assert(
                    True,
                    f"User data should contain {field} field"
                )
            else:
                assertion_manager.soft_assert(
                    False,
                    f"User data should contain {field} field"
                )
    
    @pytest.mark.regression
    @pytest.mark.high
    @pytest.mark.api
    def test_create_user_success(self, assertions):
        """
        Test POST /users endpoint creates new user successfully
        Priority: High - User creation functionality
        """
        # Generate test user data
        new_user_data = self.data_actions.generate_user_data()
        
        # Prepare request payload
        user_payload = {
            "name": f"{new_user_data['first_name']} {new_user_data['last_name']}",
            "email": new_user_data['email'],
            "username": new_user_data['username']
        }
        
        # Send POST request to create user
        response = self.api_actions.post_request("/users", json_data=user_payload)
        
        # Assert successful creation (201 or 200)
        status_code = self.api_actions.get_response_status_code(response)
        assertion_manager.hard_assert(
            status_code in [200, 201],
            f"User creation should return 200 or 201 status (got {status_code})"
        )
        
        # Verify response contains created user data
        created_user = self.api_actions.get_response_json(response)
        
        assertion_manager.hard_assert(
            "id" in created_user or "user_id" in created_user,
            "Created user response should contain user ID"
        )
        
        # Verify created user data matches sent data
        self.assertions.assert_api_json_value("email", user_payload["email"], response)
        
        # Store created user ID for cleanup
        user_id = created_user.get("id") or created_user.get("user_id")
        self.set_test_data("created_user_id", user_id)
    
    @pytest.mark.regression
    @pytest.mark.high
    @pytest.mark.api
    def test_update_user_success(self, assertions):
        """
        Test PUT /users/{id} endpoint updates user successfully
        Priority: High - User update functionality
        """
        # First create a user to update
        new_user_data = self.data_actions.generate_user_data()
        user_payload = {
            "name": f"{new_user_data['first_name']} {new_user_data['last_name']}",
            "email": new_user_data['email'],
            "username": new_user_data['username']
        }
        
        create_response = self.api_actions.post_request("/users", json_data=user_payload)
        
        if self.api_actions.get_response_status_code(create_response) not in [200, 201]:
            pytest.skip("Could not create user for update test")
        
        created_user = self.api_actions.get_response_json(create_response)
        user_id = created_user.get("id") or created_user.get("user_id")
        
        # Update user data
        updated_name = "Updated Test User"
        update_payload = {
            "name": updated_name,
            "email": user_payload["email"],
            "username": user_payload["username"]
        }
        
        # Send PUT request to update user
        response = self.api_actions.put_request(f"/users/{user_id}", json_data=update_payload)
        
        # Assert successful update
        self.assertions.assert_api_status_code(200, response)
        
        # Verify updated data
        updated_user = self.api_actions.get_response_json(response)
        self.assertions.assert_api_json_value("name", updated_name, response)
        
        self.set_test_data("updated_user_id", user_id)
    
    @pytest.mark.regression
    @pytest.mark.medium
    @pytest.mark.api
    def test_delete_user_success(self, assertions):
        """
        Test DELETE /users/{id} endpoint deletes user successfully
        Priority: Medium - User deletion functionality
        """
        # First create a user to delete
        new_user_data = self.data_actions.generate_user_data()
        user_payload = {
            "name": f"{new_user_data['first_name']} {new_user_data['last_name']}",
            "email": new_user_data['email'],
            "username": new_user_data['username']
        }
        
        create_response = self.api_actions.post_request("/users", json_data=user_payload)
        
        if self.api_actions.get_response_status_code(create_response) not in [200, 201]:
            pytest.skip("Could not create user for delete test")
        
        created_user = self.api_actions.get_response_json(create_response)
        user_id = created_user.get("id") or created_user.get("user_id")
        
        # Send DELETE request
        response = self.api_actions.delete_request(f"/users/{user_id}")
        
        # Assert successful deletion (200, 204, or 404 acceptable)
        status_code = self.api_actions.get_response_status_code(response)
        assertion_manager.hard_assert(
            status_code in [200, 204, 404],
            f"User deletion should return appropriate status (got {status_code})"
        )
        
        # Verify user is deleted by trying to get it
        get_response = self.api_actions.get_request(f"/users/{user_id}")
        get_status = self.api_actions.get_response_status_code(get_response)
        
        assertion_manager.soft_assert(
            get_status == 404,
            "Deleted user should not be found (404 status)"
        )
    
    @pytest.mark.regression
    @pytest.mark.high
    @pytest.mark.api
    def test_get_nonexistent_user_404(self, assertions):
        """
        Test GET /users/{id} returns 404 for nonexistent user
        Priority: High - Error handling
        """
        # Use a presumably non-existent user ID
        nonexistent_id = "99999999"
        
        response = self.api_actions.get_request(f"/users/{nonexistent_id}")
        
        # Assert 404 status code
        self.assertions.assert_api_status_code(404, response)
        
        # Verify error response structure
        error_response = self.api_actions.get_response_json(response)
        
        # Common error response fields
        error_indicators = ["error", "message", "detail", "status"]
        has_error_field = any(field in error_response for field in error_indicators)
        
        assertion_manager.soft_assert(
            has_error_field,
            "404 response should contain error information"
        )
    
    @pytest.mark.regression
    @pytest.mark.medium
    @pytest.mark.api
    def test_create_user_invalid_data(self, assertions):
        """
        Test POST /users with invalid data returns appropriate error
        Priority: Medium - Input validation
        """
        # Test with invalid email format
        invalid_payload = {
            "name": "Test User",
            "email": "invalid-email-format",
            "username": "testuser"
        }
        
        response = self.api_actions.post_request("/users", json_data=invalid_payload)
        
        # Assert error status code (400 or 422)
        status_code = self.api_actions.get_response_status_code(response)
        assertion_manager.hard_assert(
            status_code in [400, 422],
            f"Invalid user data should return 400 or 422 status (got {status_code})"
        )
        
        # Verify error response contains validation information
        if status_code in [400, 422]:
            error_response = self.api_actions.get_response_json(response)
            
            # Look for validation error indicators
            error_text = str(error_response).lower()
            validation_keywords = ["email", "invalid", "validation", "format"]
            
            has_validation_error = any(keyword in error_text for keyword in validation_keywords)
            assertion_manager.soft_assert(
                has_validation_error,
                "Error response should indicate email validation issue"
            )
    
    @pytest.mark.performance
    @pytest.mark.medium
    @pytest.mark.api
    def test_users_api_performance(self, assertions):
        """
        Test API performance with multiple requests
        Priority: Medium - Performance validation
        """
        import time
        
        # Test multiple GET requests
        request_times = []
        
        for i in range(5):
            start_time = time.time()
            
            response = self.api_actions.get_request("/users")
            
            end_time = time.time()
            request_time = end_time - start_time
            request_times.append(request_time)
            
            # Assert each request is successful
            assertion_manager.hard_assert(
                self.api_actions.get_response_status_code(response) == 200,
                f"Request {i+1} should be successful"
            )
        
        # Calculate average response time
        avg_response_time = sum(request_times) / len(request_times)
        max_response_time = max(request_times)
        
        # Performance assertions (warning level)
        assertion_manager.warning_assert(
            avg_response_time < 1.0,
            f"Average response time should be under 1s (actual: {avg_response_time:.3f}s)"
        )
        
        assertion_manager.warning_assert(
            max_response_time < 2.0,
            f"Max response time should be under 2s (actual: {max_response_time:.3f}s)"
        )
        
        self.logger.info(f"API Performance - Avg: {avg_response_time:.3f}s, Max: {max_response_time:.3f}s")
    
    @pytest.mark.smoke
    @pytest.mark.high
    @pytest.mark.api
    @pytest.mark.test_data("api_test_data.json")
    def test_users_with_test_data(self, assertions):
        """
        Test user operations with data from test data file
        Priority: High - Data-driven API testing
        """
        # Load test data
        try:
            api_test_data = self.data_actions.load_json_data("api_test_data.json")
        except FileNotFoundError:
            pytest.skip("API test data file not found")
        
        users_data = api_test_data.get("users", [])
        
        if not users_data:
            pytest.skip("No user test data available")
        
        # Test creating users from test data
        created_users = []
        
        for user_data in users_data[:3]:  # Test first 3 users
            response = self.api_actions.post_request("/users", json_data=user_data)
            
            status_code = self.api_actions.get_response_status_code(response)
            
            if status_code in [200, 201]:
                created_user = self.api_actions.get_response_json(response)
                created_users.append(created_user)
                
                # Verify created user data
                self.assertions.assert_api_json_value("email", user_data["email"], response)
            else:
                assertion_manager.soft_assert(
                    False,
                    f"Failed to create user with test data: {user_data}"
                )
        
        assertion_manager.hard_assert(
            len(created_users) > 0,
            "At least one user should be created from test data"
        )
    
    def teardown_method(self, method):
        """Cleanup after each test method"""
        # Clean up created test users
        user_ids_to_cleanup = [
            self.get_test_data("created_user_id"),
            self.get_test_data("updated_user_id")
        ]
        
        for user_id in user_ids_to_cleanup:
            if user_id:
                try:
                    self.api_actions.delete_request(f"/users/{user_id}")
                    self.logger.info(f"Cleaned up test user: {user_id}")
                except Exception as e:
                    self.logger.warning(f"Failed to cleanup user {user_id}: {str(e)}")
        
        super().teardown_method(method)