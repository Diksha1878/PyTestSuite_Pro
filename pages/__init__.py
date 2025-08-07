"""
Page Objects package for PyTestSuite Pro framework
"""

from .login_page import LoginPage
from .dashboard_page import DashboardPage
from .common_components import Header, Footer, NavigationMenu

__all__ = [
    'LoginPage',
    'DashboardPage',
    'Header',
    'Footer',
    'NavigationMenu'
]