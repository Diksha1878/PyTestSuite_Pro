"""
Environment Configuration Module for PyTestSuite Pro

This module manages environment-specific configurations for different 
testing environments (dev, staging, production).
"""

import os
from dataclasses import dataclass
from typing import Dict, Any
from pathlib import Path


@dataclass
class EnvironmentConfig:
    """Environment configuration data class"""
    name: str
    base_url: str
    api_base_url: str
    database_url: str
    username: str
    password: str
    timeout: int
    debug: bool
    
    # Browser configurations
    headless: bool = False
    browser_width: int = 1920
    browser_height: int = 1080
    
    # API configurations
    api_timeout: int = 30
    api_retry_count: int = 3
    
    # Test data configurations
    test_data_cleanup: bool = True
    screenshot_on_failure: bool = True


class EnvironmentManager:
    """Manages environment configurations and settings"""
    
    def __init__(self):
        self.current_env = os.getenv('TEST_ENV', 'dev').lower()
        self.config_dir = Path(__file__).parent
        self.environments = self._load_environments()
    
    def _load_environments(self) -> Dict[str, EnvironmentConfig]:
        """Load all environment configurations"""
        return {
            'dev': EnvironmentConfig(
                name='development',
                base_url='https://httpbin.org',
                api_base_url='https://httpbin.org',
                database_url='postgresql://user:pass@dev-db:5432/testdb',
                username='test_user@example.com',
                password='test_password123',
                timeout=10,
                debug=True,
                headless=False,
                screenshot_on_failure=True,
                test_data_cleanup=False
            ),
            
            'staging': EnvironmentConfig(
                name='staging',
                base_url='https://staging-app.example.com',
                api_base_url='https://staging-api.example.com/v1',
                database_url='postgresql://user:pass@staging-db:5432/testdb',
                username='staging_user@example.com',
                password='staging_password123',
                timeout=15,
                debug=False,
                headless=True,
                screenshot_on_failure=True,
                test_data_cleanup=True
            ),
            
            'prod': EnvironmentConfig(
                name='production',
                base_url='https://app.example.com',
                api_base_url='https://api.example.com/v1',
                database_url='postgresql://user:pass@prod-db:5432/testdb',
                username='prod_user@example.com',
                password='prod_password123',
                timeout=20,
                debug=False,
                headless=True,
                screenshot_on_failure=True,
                test_data_cleanup=True
            )
        }
    
    def get_config(self) -> EnvironmentConfig:
        """Get configuration for current environment"""
        if self.current_env not in self.environments:
            raise ValueError(f"Unknown environment: {self.current_env}")
        return self.environments[self.current_env]
    
    def set_environment(self, env_name: str) -> None:
        """Set the current environment"""
        if env_name.lower() not in self.environments:
            raise ValueError(f"Unknown environment: {env_name}")
        self.current_env = env_name.lower()
    
    def get_environment_names(self) -> list:
        """Get list of available environment names"""
        return list(self.environments.keys())
    
    def is_debug_enabled(self) -> bool:
        """Check if debug mode is enabled for current environment"""
        return self.get_config().debug
    
    def get_base_url(self) -> str:
        """Get base URL for current environment"""
        return self.get_config().base_url
    
    def get_api_base_url(self) -> str:
        """Get API base URL for current environment"""
        return self.get_config().api_base_url
    
    def should_cleanup_test_data(self) -> bool:
        """Check if test data should be cleaned up"""
        return self.get_config().test_data_cleanup


# Global environment manager instance
env_manager = EnvironmentManager()


def get_current_config() -> EnvironmentConfig:
    """Convenience function to get current environment configuration"""
    return env_manager.get_config()


def get_base_url() -> str:
    """Convenience function to get base URL"""
    return env_manager.get_base_url()


def get_api_base_url() -> str:
    """Convenience function to get API base URL"""
    return env_manager.get_api_base_url()


# Environment configuration examples for different use cases
ENVIRONMENT_EXAMPLES = {
    'local_docker': EnvironmentConfig(
        name='local_docker',
        base_url='http://localhost:3000',
        api_base_url='http://localhost:8000/api/v1',
        database_url='postgresql://postgres:password@localhost:5432/testdb',
        username='local_user@example.com',
        password='local_password',
        timeout=5,
        debug=True,
        headless=False
    ),
    
    'ci_cd': EnvironmentConfig(
        name='ci_cd',
        base_url='http://test-app:3000',
        api_base_url='http://test-api:8000/api/v1',
        database_url='postgresql://postgres:password@test-db:5432/testdb',
        username='ci_user@example.com',
        password='ci_password',
        timeout=30,
        debug=False,
        headless=True,
        screenshot_on_failure=True,
        test_data_cleanup=True
    )
}