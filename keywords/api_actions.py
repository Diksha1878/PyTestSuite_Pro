"""
API Actions Keywords for PyTestSuite Pro

This module provides high-level keyword actions for API testing
with support for different HTTP methods, authentication, and validation.
"""

import json
import logging
import time
from typing import Dict, Any, Optional, List, Union
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests_oauthlib import OAuth1

from config import get_current_config


class APIActions:
    """High-level API action keywords for test automation"""
    
    def __init__(self):
        self.config = get_current_config()
        self.session = requests.Session()
        self.logger = self._setup_logger()
        self.base_url = self.config.api_base_url
        self.default_timeout = self.config.api_timeout
        self.last_response = None
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'PyTestSuite-Pro/1.0'
        })
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for API actions"""
        logger = logging.getLogger('APIActions')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    # Configuration Methods
    def set_base_url(self, base_url: str):
        """
        Set base URL for API requests
        
        Args:
            base_url: Base URL for API endpoints
        """
        self.base_url = base_url.rstrip('/')
        self.logger.info(f"API base URL set to: {self.base_url}")
    
    def set_timeout(self, timeout: int):
        """
        Set default timeout for API requests
        
        Args:
            timeout: Timeout in seconds
        """
        self.default_timeout = timeout
        self.logger.info(f"API timeout set to: {timeout}s")
    
    def set_header(self, key: str, value: str):
        """
        Set or update HTTP header
        
        Args:
            key: Header name
            value: Header value
        """
        self.session.headers[key] = value
        self.logger.info(f"Header set: {key} = {value}")
    
    def remove_header(self, key: str):
        """
        Remove HTTP header
        
        Args:
            key: Header name to remove
        """
        if key in self.session.headers:
            del self.session.headers[key]
            self.logger.info(f"Header removed: {key}")
    
    def set_auth_token(self, token: str, token_type: str = 'Bearer'):
        """
        Set authentication token
        
        Args:
            token: Authentication token
            token_type: Type of token (Bearer, Token, etc.)
        """
        self.session.headers['Authorization'] = f"{token_type} {token}"
        self.logger.info(f"Authentication token set: {token_type}")
    
    def set_basic_auth(self, username: str, password: str):
        """
        Set basic authentication
        
        Args:
            username: Username for basic auth
            password: Password for basic auth
        """
        self.session.auth = HTTPBasicAuth(username, password)
        self.logger.info(f"Basic authentication set for user: {username}")
    
    def clear_auth(self):
        """Clear all authentication"""
        self.session.auth = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        self.logger.info("Authentication cleared")
    
    # HTTP Method Keywords
    def get_request(self, endpoint: str, params: Dict = None, headers: Dict = None, timeout: int = None) -> requests.Response:
        """
        Send GET request
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout
            
        Returns:
            requests.Response: Response object
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        
        self.logger.info(f"Sending GET request to: {url}")
        if params:
            self.logger.info(f"Query parameters: {params}")
        
        try:
            self.last_response = self.session.get(
                url, 
                params=params, 
                headers=headers, 
                timeout=timeout
            )
            
            self._log_response(self.last_response)
            return self.last_response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"GET request failed: {str(e)}")
            raise
    
    def post_request(self, endpoint: str, data: Union[Dict, str] = None, json_data: Dict = None, 
                     headers: Dict = None, timeout: int = None) -> requests.Response:
        """
        Send POST request
        
        Args:
            endpoint: API endpoint path
            data: Form data or raw data
            json_data: JSON data
            headers: Additional headers
            timeout: Request timeout
            
        Returns:
            requests.Response: Response object
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        
        self.logger.info(f"Sending POST request to: {url}")
        if json_data:
            self.logger.info(f"JSON payload: {json.dumps(json_data, indent=2)}")
        
        try:
            self.last_response = self.session.post(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout
            )
            
            self._log_response(self.last_response)
            return self.last_response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"POST request failed: {str(e)}")
            raise
    
    def put_request(self, endpoint: str, data: Union[Dict, str] = None, json_data: Dict = None,
                    headers: Dict = None, timeout: int = None) -> requests.Response:
        """
        Send PUT request
        
        Args:
            endpoint: API endpoint path
            data: Form data or raw data
            json_data: JSON data
            headers: Additional headers
            timeout: Request timeout
            
        Returns:
            requests.Response: Response object
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        
        self.logger.info(f"Sending PUT request to: {url}")
        if json_data:
            self.logger.info(f"JSON payload: {json.dumps(json_data, indent=2)}")
        
        try:
            self.last_response = self.session.put(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout
            )
            
            self._log_response(self.last_response)
            return self.last_response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"PUT request failed: {str(e)}")
            raise
    
    def patch_request(self, endpoint: str, data: Union[Dict, str] = None, json_data: Dict = None,
                      headers: Dict = None, timeout: int = None) -> requests.Response:
        """
        Send PATCH request
        
        Args:
            endpoint: API endpoint path
            data: Form data or raw data
            json_data: JSON data
            headers: Additional headers
            timeout: Request timeout
            
        Returns:
            requests.Response: Response object
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        
        self.logger.info(f"Sending PATCH request to: {url}")
        if json_data:
            self.logger.info(f"JSON payload: {json.dumps(json_data, indent=2)}")
        
        try:
            self.last_response = self.session.patch(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout
            )
            
            self._log_response(self.last_response)
            return self.last_response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"PATCH request failed: {str(e)}")
            raise
    
    def delete_request(self, endpoint: str, params: Dict = None, headers: Dict = None,
                       timeout: int = None) -> requests.Response:
        """
        Send DELETE request
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout
            
        Returns:
            requests.Response: Response object
        """
        url = self._build_url(endpoint)
        timeout = timeout or self.default_timeout
        
        self.logger.info(f"Sending DELETE request to: {url}")
        if params:
            self.logger.info(f"Query parameters: {params}")
        
        try:
            self.last_response = self.session.delete(
                url,
                params=params,
                headers=headers,
                timeout=timeout
            )
            
            self._log_response(self.last_response)
            return self.last_response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"DELETE request failed: {str(e)}")
            raise
    
    # Response Analysis Keywords
    def get_response_status_code(self, response: requests.Response = None) -> int:
        """
        Get response status code
        
        Args:
            response: Response object (uses last response if None)
            
        Returns:
            int: HTTP status code
        """
        response = response or self.last_response
        if not response:
            raise ValueError("No response available")
        
        status_code = response.status_code
        self.logger.info(f"Response status code: {status_code}")
        return status_code
    
    def get_response_json(self, response: requests.Response = None) -> Dict:
        """
        Get response JSON data
        
        Args:
            response: Response object (uses last response if None)
            
        Returns:
            Dict: JSON response data
        """
        response = response or self.last_response
        if not response:
            raise ValueError("No response available")
        
        try:
            json_data = response.json()
            self.logger.info("Response JSON data retrieved")
            return json_data
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON response: {str(e)}")
            raise
    
    def get_response_text(self, response: requests.Response = None) -> str:
        """
        Get response text content
        
        Args:
            response: Response object (uses last response if None)
            
        Returns:
            str: Response text
        """
        response = response or self.last_response
        if not response:
            raise ValueError("No response available")
        
        text = response.text
        self.logger.info(f"Response text length: {len(text)} characters")
        return text
    
    def get_response_headers(self, response: requests.Response = None) -> Dict:
        """
        Get response headers
        
        Args:
            response: Response object (uses last response if None)
            
        Returns:
            Dict: Response headers
        """
        response = response or self.last_response
        if not response:
            raise ValueError("No response available")
        
        headers = dict(response.headers)
        self.logger.info(f"Response headers: {headers}")
        return headers
    
    def get_response_time(self, response: requests.Response = None) -> float:
        """
        Get response time in seconds
        
        Args:
            response: Response object (uses last response if None)
            
        Returns:
            float: Response time in seconds
        """
        response = response or self.last_response
        if not response:
            raise ValueError("No response available")
        
        response_time = response.elapsed.total_seconds()
        self.logger.info(f"Response time: {response_time}s")
        return response_time
    
    # JSON Path Keywords
    def get_json_value(self, json_path: str, response: requests.Response = None) -> Any:
        """
        Get value from JSON response using JSONPath
        
        Args:
            json_path: JSONPath expression (simplified dot notation)
            response: Response object (uses last response if None)
            
        Returns:
            Any: Value at JSONPath
        """
        response = response or self.last_response
        if not response:
            raise ValueError("No response available")
        
        json_data = self.get_response_json(response)
        
        # Simple JSONPath implementation for basic paths like "data.user.name"
        try:
            value = json_data
            for key in json_path.split('.'):
                if key.isdigit():
                    value = value[int(key)]
                else:
                    value = value[key]
            
            self.logger.info(f"JSON value at '{json_path}': {value}")
            return value
            
        except (KeyError, IndexError, TypeError) as e:
            self.logger.error(f"Failed to get value at JSONPath '{json_path}': {str(e)}")
            raise
    
    def json_contains_key(self, key: str, response: requests.Response = None) -> bool:
        """
        Check if JSON response contains specific key
        
        Args:
            key: Key to check for
            response: Response object (uses last response if None)
            
        Returns:
            bool: True if key exists, False otherwise
        """
        response = response or self.last_response
        if not response:
            raise ValueError("No response available")
        
        json_data = self.get_response_json(response)
        exists = key in json_data
        
        self.logger.info(f"JSON key '{key}' exists: {exists}")
        return exists
    
    # Validation Keywords
    def assert_status_code(self, expected_status: int, response: requests.Response = None):
        """
        Assert response status code
        
        Args:
            expected_status: Expected HTTP status code
            response: Response object (uses last response if None)
        """
        actual_status = self.get_response_status_code(response)
        
        from core import assertion_manager
        assertion_manager.assert_equals(
            actual_status,
            expected_status,
            f"Status code should be {expected_status}"
        )
    
    def assert_response_contains(self, expected_text: str, response: requests.Response = None):
        """
        Assert response text contains expected text
        
        Args:
            expected_text: Text that should be in response
            response: Response object (uses last response if None)
        """
        response_text = self.get_response_text(response)
        
        from core import assertion_manager
        assertion_manager.assert_contains(
            response_text,
            expected_text,
            f"Response should contain '{expected_text}'"
        )
    
    def assert_json_value(self, json_path: str, expected_value: Any, response: requests.Response = None):
        """
        Assert JSON value at specific path
        
        Args:
            json_path: JSONPath to the value
            expected_value: Expected value
            response: Response object (uses last response if None)
        """
        actual_value = self.get_json_value(json_path, response)
        
        from core import assertion_manager
        assertion_manager.assert_equals(
            actual_value,
            expected_value,
            f"JSON value at '{json_path}' should be {expected_value}"
        )
    
    def assert_response_time_under(self, max_seconds: float, response: requests.Response = None):
        """
        Assert response time is under specified limit
        
        Args:
            max_seconds: Maximum allowed response time
            response: Response object (uses last response if None)
        """
        response_time = self.get_response_time(response)
        
        from core import assertion_manager
        assertion_manager.assert_less_than(
            response_time,
            max_seconds,
            f"Response time should be under {max_seconds}s"
        )
    
    # Utility Methods
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        if endpoint.startswith(('http://', 'https://')):
            return endpoint
        
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"
    
    def _log_response(self, response: requests.Response):
        """Log response details"""
        self.logger.info(f"Response: {response.status_code} {response.reason}")
        self.logger.info(f"Response time: {response.elapsed.total_seconds()}s")
        
        # Log response body for debugging (truncated)
        if response.text:
            text_preview = response.text[:500]
            if len(response.text) > 500:
                text_preview += "... (truncated)"
            self.logger.debug(f"Response body: {text_preview}")
    
    def save_response_to_file(self, filename: str, response: requests.Response = None):
        """
        Save response to file
        
        Args:
            filename: File path to save response
            response: Response object (uses last response if None)
        """
        response = response or self.last_response
        if not response:
            raise ValueError("No response available")
        
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        self.logger.info(f"Response saved to: {filename}")
    
    def close_session(self):
        """Close the HTTP session"""
        self.session.close()
        self.logger.info("API session closed")