"""
Configuration package for PyTestSuite Pro framework
"""

from .environment import env_manager, get_current_config, get_base_url, get_api_base_url
from .browser_config import browser_config, BrowserCapabilities, BROWSER_CONFIGS

__all__ = [
    'env_manager',
    'get_current_config',
    'get_base_url',
    'get_api_base_url',
    'browser_config',
    'BrowserCapabilities',
    'BROWSER_CONFIGS'
]