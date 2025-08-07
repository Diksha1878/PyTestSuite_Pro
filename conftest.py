"""
Global pytest configuration and fixtures for PyTestSuite Pro

This module contains shared pytest fixtures and configuration
that are available to all test modules in the framework.
"""

import os
import pytest
import logging
from datetime import datetime
from pathlib import Path 

# Framework imports
from core import DriverManager, assertion_manager
from keywords import WebActions, APIActions, DataActions, AssertionKeywords
from config import env_manager, get_current_config


def pytest_addoption(parser):
    """Add custom command line options for pytest"""
    
    # Browser selection
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Browser to use for UI tests"
    )
    
    # Environment selection  
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        choices=["dev", "staging", "prod"],
        help="Environment to run tests against"
    )
    
    # Headless mode
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )
    
    # Base URL override
    parser.addoption(
        "--base-url",
        action="store",
        help="Override base URL for testing"
    )
    
    # API URL override
    parser.addoption(
        "--api-url", 
        action="store",
        help="Override API base URL for testing"
    )
    
    # Selenium Grid URL
    parser.addoption(
        "--selenium-hub",
        action="store",
        help="Selenium Grid hub URL for remote execution"
    )
    
    # Screenshot on failure
    parser.addoption(
        "--screenshot-on-failure",
        action="store_true",
        default=True,
        help="Take screenshot on test failure"
    )
    
    # Keep browser open for debugging
    parser.addoption(
        "--keep-browser-open",
        action="store_true", 
        default=False,
        help="Keep browser open after test completion (debug mode)"
    )


def pytest_configure(config):
    """Configure pytest with custom settings"""
    
    # Set environment based on command line option
    env_name = config.getoption("--env")
    if env_name:
        os.environ["TEST_ENV"] = env_name
        env_manager.set_environment(env_name)
    
    # Set browser preference
    browser = config.getoption("--browser")
    if browser:
        os.environ["BROWSER"] = browser
    
    # Set headless mode
    headless = config.getoption("--headless")
    if headless:
        os.environ["HEADLESS"] = "true"
    
    # Set Selenium Grid URL if provided
    selenium_hub = config.getoption("--selenium-hub")
    if selenium_hub:
        os.environ["SELENIUM_REMOTE_URL"] = selenium_hub
    
    # Override URLs if provided
    base_url = config.getoption("--base-url")
    if base_url:
        os.environ["BASE_URL_OVERRIDE"] = base_url
        
    api_url = config.getoption("--api-url")
    if api_url:
        os.environ["API_URL_OVERRIDE"] = api_url
    
    # Create reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Create subdirectories for artifacts
    (reports_dir / "screenshots").mkdir(exist_ok=True)
    (reports_dir / "page_sources").mkdir(exist_ok=True)
    (reports_dir / "logs").mkdir(exist_ok=True)
    
    # Configure logging
    log_level = logging.INFO
    if config.getoption("--log-cli-level"):
        log_level = getattr(logging, config.getoption("--log-cli-level").upper(), logging.INFO)
    
    # Set up root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('reports/pytest.log'),
            logging.StreamHandler()
        ]
    )


def pytest_sessionstart(session):
    """Called after the Session object has been created"""
    logger = logging.getLogger("pytest_session")
    
    # Log session start information
    config = get_current_config()
    logger.info("=" * 80)
    logger.info("PYTEST SESSION STARTING")
    logger.info("=" * 80)
    logger.info(f"Environment: {config.name}")
    logger.info(f"Base URL: {config.base_url}")
    logger.info(f"API URL: {config.api_base_url}")
    logger.info(f"Browser: {os.getenv('BROWSER', 'chrome')}")
    logger.info(f"Headless: {os.getenv('HEADLESS', 'false')}")
    logger.info(f"Parallel: {session.config.getoption('-n', default='1')}")
    logger.info(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished"""
    logger = logging.getLogger("pytest_session")
    
    # Cleanup all driver instances
    DriverManager.cleanup_all_drivers()
    
    # Log session completion
    logger.info("=" * 80)
    logger.info("PYTEST SESSION FINISHED")
    logger.info("=" * 80)
    logger.info(f"Exit Status: {exitstatus}")
    logger.info(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and take screenshots on failure"""
    outcome = yield
    report = outcome.get_result()
    
    # Take screenshot on UI test failure
    if (call.when == "call" and 
        report.failed and 
        hasattr(item.cls, 'driver') and 
        item.cls.driver and
        item.config.getoption("--screenshot-on-failure")):
        
        try:
            # Create screenshot filename
            test_name = item.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{test_name}_failure_{timestamp}.png"
            
            # Take screenshot
            from core.driver_manager import take_screenshot
            screenshot_path = take_screenshot(screenshot_name)
            
            # Add screenshot info to test report
            if hasattr(report, 'extra'):
                report.extra = getattr(report, 'extra', [])
                report.extra.append({
                    'name': 'Screenshot',
                    'path': screenshot_path,
                    'mime_type': 'image/png'
                })
            
            logging.getLogger("pytest").info(f"Screenshot saved: {screenshot_path}")
            
        except Exception as e:
            logging.getLogger("pytest").warning(f"Failed to take screenshot: {str(e)}")


# Global Fixtures

@pytest.fixture(scope="session")
def browser_name(request):
    """Get browser name from command line option"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def environment(request):
    """Get environment from command line option"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def headless_mode(request):
    """Get headless mode setting"""
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def test_config():
    """Get current test configuration"""
    return get_current_config()


@pytest.fixture(scope="function")
def web_driver(browser_name, headless_mode):
    """Provide WebDriver instance for tests"""
    from core.driver_manager import get_driver, quit_driver
    
    driver = get_driver(browser_name, headless_mode)
    yield driver
    quit_driver()


@pytest.fixture(scope="function") 
def web_actions():
    """Provide WebActions instance for tests"""
    return WebActions()


@pytest.fixture(scope="function")
def api_actions():
    """Provide APIActions instance for tests"""
    return APIActions()


@pytest.fixture(scope="function")
def data_actions():
    """Provide DataActions instance for tests"""
    return DataActions()


@pytest.fixture(scope="function")
def assertion_keywords():
    """Provide AssertionKeywords instance for tests"""
    return AssertionKeywords()


@pytest.fixture(scope="function")
def assertions():
    """Provide assertion manager with automatic cleanup"""
    # Reset assertion manager for clean test state
    assertion_manager.reset()
    
    # Set test context from current test
    import inspect
    frame = inspect.currentframe()
    test_name = "unknown_test"
    
    try:
        # Walk up the call stack to find the test function
        for frame_info in inspect.stack():
            if frame_info.function.startswith('test_'):
                test_name = frame_info.function
                break
    except:
        pass
    finally:
        del frame
    
    assertion_manager.set_test_context(test_name)
    
    yield assertion_manager
    
    # Finalize assertions after test completion
    try:
        assertion_manager.finalize_assertions()
    except Exception as e:
        logging.getLogger("assertions").error(f"Failed to finalize assertions: {str(e)}")


@pytest.fixture(scope="function")
def test_data_manager():
    """Provide test data manager with cleanup"""
    data_manager = DataActions()
    yield data_manager
    # Cleanup cached data
    data_manager.clear_cache()


# Markers for test categorization (registered in pytest.ini)
# These are documented here for reference:

# Priority markers
# smoke: Quick validation tests for critical functionality
# critical: Must-pass functionality, blocking issues
# high: Important features, major functionality
# medium: Standard feature validation
# low: Nice-to-have features, edge cases

# Type markers  
# ui: User interface tests
# api: API endpoint tests
# integration: End-to-end workflow tests
# database: Database-related tests

# Execution markers
# regression: Full regression test suite
# performance: Performance and load tests
# security: Security-focused tests
# cross_browser: Cross-browser compatibility tests
# mobile: Mobile-specific tests

# Execution control markers
# slow: Tests that take longer to execute
# fast: Quick executing tests
# flaky: Tests that may occasionally fail
# skip_parallel: Tests that should not run in parallel


# Helper functions for test data management

def get_test_data_path(filename: str, data_type: str = "json") -> Path:
    """Get full path to test data file"""
    return Path("test_data") / data_type / filename


def load_test_data(filename: str, data_type: str = "json"):
    """Load test data from file"""
    data_manager = DataActions()
    
    if data_type == "json":
        return data_manager.load_json_data(filename)
    elif data_type == "csv":
        return data_manager.load_csv_data(filename)
    elif data_type == "yaml":
        return data_manager.load_yaml_data(filename)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


# Pytest plugins configuration
pytest_plugins = [
    # Enable HTML reporting
    "pytest_html",
    # # Enable parallel execution  
    # "pytest_xdist",
    # # Enable test reruns on failure
    # "pytest_rerunfailures"
]