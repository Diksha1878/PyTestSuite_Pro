# PyTestSuite Pro

## 🚀 Advanced Hybrid Test Automation Framework

PyTestSuite Pro is a comprehensive, enterprise-grade test automation framework that combines data-driven, keyword-driven, and modular testing approaches. Built on top of pytest and Selenium WebDriver, it provides a scalable solution for UI, API, and integration testing with advanced features like smart test categorization, and multi-level assertion strategies.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Test Organization](#-test-organization)
- [Assertion Strategies](#-assertion-strategies)
- [Keywords System](#-keywords-system)
<!-- - [Parallel Execution](#-parallel-execution) -->
- [CI/CD Integration](#-cicd-integration)
- [Reporting](#-reporting)
<!-- - [Best Practices](#-best-practices) -->
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

### 🏗️ **Hybrid Architecture**
- **Data-Driven Testing**: External test data from JSON, CSV, YAML files
- **Keyword-Driven Testing**: Reusable action keywords for common operations  
- **Page Object Model**: Organized page objects and component structure
- **Multi-Layer Assertions**: Hard, soft, and warning assertion strategies

### 🎯 **Smart Test Organization**
- **15+ Pytest Markers**: `smoke`, `regression`, `critical`, `high`, `medium`, `low`, `ui`, `api`, `integration`, `database`, `performance`, `security`, `cross_browser`, `mobile`, `fast`, `slow`, `flaky`, `skip_parallel`, `test_data`
- **Flexible Test Grouping**: Run specific test combinations based on priority, type, or custom criteria
- **Environment-Specific Configuration**: Support for dev, staging, production environments

### 🔧 **Advanced Keywords System**
- **WebActions**: High-level web interaction keywords
- **APIActions**: Comprehensive API testing methods with authentication
- **DataActions**: Test data management with Faker integration
- **AssertionKeywords**: Custom assertion combinations and validations

<!-- ### ⚡ **Parallel Execution**
- **Multi-Level Parallelization**: Test-level and browser-level parallel execution
- **Worker-Specific Data Distribution**: Isolated test data for each parallel worker
- **Smart Resource Management**: Automatic driver cleanup and connection pooling -->

### 🌐 **Cross-Browser Support**
- **Browser Compatibility**: Chrome, Firefox, Edge with automatic driver management
- **WebDriver Manager Integration**: Automatic driver downloads and updates
- **Mobile Testing**: Device emulation and responsive testing capabilities

### 📊 **Rich Reporting**
- **HTML Reports**: Detailed test execution reports with screenshots
- **Allure Integration**: Advanced reporting with test history and trends
- **Automatic Screenshots**: Capture on failure and key test steps
- **Structured Logs**: Comprehensive logging with different levels

### 🔧 **Enterprise Features**
- **Configuration Management**: Environment-specific settings and credentials
- **Security Testing**: Built-in security validation markers and keywords
- **Performance Monitoring**: Response time tracking and performance assertions
- **Database Integration**: Support for test data cleanup and validation

## 🏛️ Architecture

```
PyTestSuite_Pro/
├── config/                    # Environment and browser configurations
│   ├── environment.py         # Environment-specific settings (dev, staging, prod)
│   ├── browser_config.py      # Browser configurations and capabilities
│   └── __init__.py           # Configuration exports
├── core/                      # Core framework components
│   ├── driver_manager.py      # WebDriver management with parallel support
│   ├── assertions.py          # Advanced assertion strategies (hard/soft/warning)
│   ├── base_test.py           # Base test classes (UITest, APITest, IntegrationTest)
│   ├── base_page.py           # Base page object model
│   └── __init__.py           # Core exports
├── pages/                     # Page Object Models
│   ├── login_page.py          # Login page implementation
│   ├── dashboard_page.py      # Dashboard page implementation  
│   ├── common_components.py   # Shared page components
│   └── __init__.py           # Page exports
├── keywords/                  # Reusable action keywords (Keyword-Driven Testing)
│   ├── web_actions.py         # High-level web interaction keywords
│   ├── api_actions.py         # API testing keywords with authentication
│   ├── data_actions.py        # Test data management keywords
│   ├── assertion_keywords.py  # Custom assertion combinations
│   └── __init__.py           # Keywords exports
├── tests/                     # Test cases organized by type
│   ├── ui/                    # User interface tests
│   │   └── test_login.py      # Login functionality tests
│   ├── api/                   # API endpoint tests
│   │   └── test_user_api.py   # User API tests
│   ├── integration/           # End-to-end integration tests
│   │   └── test_user_workflow.py # Complete user workflows
│   └── __init__.py           # Test package initialization
├── test_data/                 # External test data (Data-Driven Testing)
│   ├── json/                  # JSON test data files
│   │   ├── api_test_data.json # API test datasets
│   │   └── users.json         # User test data
│   ├── csv/                   # CSV test data files
│   │   └── user_credentials.csv # User credentials for testing
│   ├── yaml/                  # YAML configuration files
│   │   ├── environment_dev.yaml # Development environment config
│   │   └── environment_staging.yaml # Staging environment config
│   └── ...                    # Additional data formats
├── reports/                   # Test execution reports and artifacts
│   ├── logs/                  # Test execution logs
│   ├── screenshots/           # Automated screenshots
│   ├── page_sources/          # Page source captures
│   └── *.html                 # HTML test reports
├── drivers/                   # WebDriver executables
├── .github/workflows/         # GitHub Actions CI/CD
│   └── test-automation.yml    # Comprehensive CI/CD pipeline
├── requirements.txt           # Python dependencies
├── pytest.ini               # Pytest configuration with markers
├── conftest.py              # Pytest fixtures and configuration
├── Jenkinsfile              # Jenkins pipeline configuration
├── setup.py                 # Package installation configuration
└── README.md                # This documentation
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd PyTestSuite_Pro

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Set your target environment
export TEST_ENV=dev  # or staging, prod

# Optional: Set browser preference
export BROWSER=chrome  # or firefox, edge
```

### 3. Run Your First Test
```bash
# Run smoke tests
pytest -m smoke

# Run with specific browser
pytest -m smoke --browser=chrome

# Run with parallel execution
pytest -m regression -n auto

# Generate HTML report
pytest -m smoke --html=reports/smoke_report.html
```

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- **pip** package manager
- **Git**

### Dependencies Overview

The framework uses these key technologies:

**Core Testing Framework:**
- `pytest==7.4.3` - Test framework
- `pytest-html==4.1.1` - HTML reporting
- `pytest-xdist==3.5.0` - Parallel execution
- `pytest-parallel==0.1.1` - Additional parallel support
- `pytest-rerunfailures==12.0` - Test retry functionality

**WebDriver & Automation:**
- `selenium==4.16.0` - Web automation
- `webdriver-manager==4.0.1` - Automatic driver management

**API Testing:**
- `requests==2.31.0` - HTTP requests
- `requests-oauthlib==1.3.1` - OAuth authentication

**Data Management:**
- `pandas==2.1.4` - Data manipulation
- `PyYAML==6.0.1` - YAML configuration
- `faker==20.1.0` - Test data generation
- `jsonschema==4.20.0` - JSON validation

**Reporting & Utilities:**
- `allure-pytest==2.13.2` - Advanced reporting
- `colorlog==6.8.0` - Enhanced logging
- `Pillow==10.1.0` - Image processing

### Installation Steps

1. **Clone Repository**
   ```bash
   git clone <your-repository-url>
   cd PyTestSuite_Pro
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install as Package** (Optional)
   ```bash
   pip install -e .
   ```

5. **Verify Installation**
   ```bash
   pytest --version
   python -c "from selenium import webdriver; print('Selenium installed successfully')"
   ```

## ⚙️ Configuration

### Environment Configuration

Edit `config/environment.py` to customize environment settings:

```python
# Example environment configuration
environments = {
    'dev': EnvironmentConfig(
        name='development',
        base_url='https://httpbin.org',
        api_base_url='https://httpbin.org',
        username='test_user@example.com',
        password='test_password123',
        timeout=10,
        headless=False,
        screenshot_on_failure=True
    ),
    'staging': EnvironmentConfig(
        name='staging',
        base_url='https://staging-app.example.com',
        api_base_url='https://staging-api.example.com/v1',
        username='staging_user@example.com',
        password='staging_password123',
        timeout=15,
        headless=True
    )
}
```

### Browser Configuration

Customize browser settings in `config/browser_config.py`:

```python
# Chrome configuration
BROWSER_CONFIGS = {
    'chrome_debug': BrowserCapabilities(
        browser_name='chrome',
        headless=False,
        window_size=(1920, 1080),
        arguments=['--start-maximized'],
        prefs={'profile.default_content_setting_values.notifications': 2}
    ),
    'chrome_headless': BrowserCapabilities(
        browser_name='chrome',
        headless=True,
        arguments=['--no-sandbox', '--disable-dev-shm-usage']
    )
}
```

### Pytest Configuration

Key settings in `pytest.ini`:

```ini
[pytest]
# Test discovery
python_files = test_*.py *_test.py
testpaths = tests

# Essential markers
markers =
    smoke: Quick smoke tests for critical functionality
    regression: Full regression test suite
    critical: Critical business functionality tests
    ui: User interface tests
    api: API endpoint tests
    integration: Integration tests
    performance: Performance and load tests
    
# Reporting
addopts = --html=reports/report.html --self-contained-html -v
```

## 💡 Usage Examples

### Basic Test Execution

```bash
# Run all smoke tests
pytest -m smoke

# Run specific test types
pytest -m "ui and critical"
pytest -m "api and not slow"

# Run tests with specific browser
pytest tests/ui/ --browser=firefox

# Run with custom environment
pytest -m regression --env=staging
```

### Parallel Execution

```bash
# Auto-detect CPU cores
pytest -m regression -n auto

# Specify number of workers
pytest -m regression -n 4

# Distribute by test scope
pytest -m regression -n auto --dist=loadscope
```

### Advanced Filtering

```bash
# Run critical and high priority tests
pytest -m "critical or high"

# Exclude slow tests
pytest -m "regression and not slow"

# Environment-specific tests
pytest -m "smoke and not skip_parallel" -n auto
```

### Reporting

```bash
# Generate HTML report
pytest -m smoke --html=reports/smoke_report.html

# Generate Allure report
pytest -m regression --alluredir=reports/allure-results
allure serve reports/allure-results

# Custom report location
pytest --html=custom_reports/my_report.html --self-contained-html
```

## 🗂️ Test Organization

### Test Structure

```python
class TestLogin(UITest):
    """Login functionality test suite"""
    
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.ui
    def test_valid_login_success(self):
        """Test successful login with valid credentials"""
        # Using keywords for readable test logic
        self.web_actions.navigate_to_login()
        result = self.web_actions.login_user("testuser", "password")
        
        # Hard assertion for critical functionality
        assertion_manager.hard_assert(
            result, 
            "Login must succeed with valid credentials"
        )
    
    @pytest.mark.regression
    @pytest.mark.medium
    @pytest.mark.ui
    def test_invalid_credentials_error(self):
        """Test login failure with invalid credentials"""
        # Test implementation using keywords
        pass
```

### Marker Usage Guidelines

| Marker | Usage | When to Use |
|--------|--------|-------------|
| `smoke` | Quick validation tests | Critical functionality, build verification |
| `regression` | Comprehensive test suite | Full feature validation, release testing |
| `critical` | Must-pass functionality | Core business features, blocking issues |
| `high` | Important features | Major functionality, user-facing features |
| `medium` | Standard features | Regular functionality validation |
| `low` | Nice-to-have features | Edge cases, minor functionality |
| `ui` | User interface tests | Frontend validation, user experience |
| `api` | API endpoint tests | Backend services, data validation |
| `integration` | End-to-end tests | Complete user workflows |
| `database` | Database tests | Data persistence, cleanup |
| `performance` | Performance tests | Response times, load testing |
| `security` | Security tests | Authentication, authorization |
| `cross_browser` | Multi-browser tests | Browser compatibility |
| `mobile` | Mobile tests | Mobile-specific functionality |
| `fast` | Quick tests | Rapid feedback during development |
| `slow` | Long-running tests | Comprehensive validation |
| `flaky` | Unstable tests | Tests that may occasionally fail |
| `skip_parallel` | Sequential tests | Tests that can't run in parallel |
| `test_data` | Data-driven tests | Tests using external data files |

## 🎯 Assertion Strategies

The framework provides three levels of assertions:

### Hard Assertions
Use for critical functionality that must work:
```python
def test_user_login(self):
    login_success = self.login_page.login("user", "password")
    
    # Critical assertion - test fails immediately if this fails
    assertion_manager.hard_assert(
        login_success,
        "Login must succeed with valid credentials"
    )
```

### Soft Assertions
Use for UI validations and multiple related checks:
```python
def test_form_layout(self):
    # Collect multiple UI validation failures
    assertion_manager.soft_assert(
        self.page.is_element_visible(self.page.USERNAME_FIELD),
        "Username field should be visible"
    )
    
    assertion_manager.soft_assert(
        self.page.is_element_visible(self.page.PASSWORD_FIELD),
        "Password field should be visible"
    )
    
    # Test fails at end if any soft assertions failed
```

### Warning Assertions
Use for performance checks and non-critical features:
```python
def test_page_performance(self):
    start_time = time.time()
    self.page.load()
    load_time = time.time() - start_time
    
    # Warning - logged but doesn't fail test
    assertion_manager.warning_assert(
        load_time < 3.0,
        f"Page should load under 3s (actual: {load_time:.2f}s)"
    )
```

## 🔑 Keywords System

The framework's keywords system provides high-level, reusable actions:

### WebActions Keywords
```python
class WebActions:
    def navigate_to_login(self):
        """Navigate to login page"""
        
    def login_user(self, username, password):
        """Perform user login with credentials"""
        
    def fill_form_field(self, locator, value):
        """Fill form field with value"""
        
    def click_element(self, locator):
        """Click on element with wait"""
```

### APIActions Keywords
```python
class APIActions:
    def get_request(self, endpoint, headers=None):
        """Perform GET request with logging"""
        
    def post_request(self, endpoint, json_data=None):
        """Perform POST request with validation"""
        
    def verify_response_status(self, response, expected_status):
        """Verify API response status code"""
```

### DataActions Keywords
```python
class DataActions:
    def load_json_data(self, filename):
        """Load test data from JSON file"""
        
    def generate_user_data(self):
        """Generate fake user data using Faker"""
        
    def get_test_credentials(self, user_type):
        """Get credentials from data files"""
```

## ⚡ Parallel Execution

### Configuration

Enable parallel execution in `pytest.ini`:

```ini
# Use with command line options:
# pytest -n auto          # Auto-detect CPU cores
# pytest -n 4             # Use 4 workers
# pytest --dist=loadscope # Distribute by test scope
```

### Best Practices

1. **Data Isolation**: Framework provides unique test data per worker
   ```python
   def test_user_creation(self):
       # Framework automatically generates unique data per worker
       user_data = self.data_actions.generate_user_data()
       unique_email = f"{user_data['email']}.worker{os.getpid()}"
   ```

2. **Resource Management**: Automatic driver cleanup
   ```python
   # Framework handles this automatically
   def setup_method(self):
       self.driver = get_driver()  # Worker-specific driver
   
   def teardown_method(self):
       quit_driver()  # Automatic cleanup
   ```

3. **Thread-Safe Operations**: Built-in session management
   ```python
   def test_api_call(self):
       response = self.api_actions.get_request("/users")  # Thread-safe
   ```

## 🚀 CI/CD Integration

### GitHub Actions

The framework includes a comprehensive GitHub Actions workflow with:

**Multi-Stage Pipeline:**
- **Smoke Tests**: Quick validation (15 min timeout)
- **API Tests**: Backend validation with mock services (20 min)
- **UI Tests**: Cross-browser testing (Chrome, Firefox, Edge) (45 min)
- **Integration Tests**: Full workflow validation (60 min)
- **Parallel Tests**: Performance validation (30 min)
- **Performance Tests**: Load testing (conditional)
- **Security Tests**: Security validation (conditional)
- **Nightly Regression**: Complete test suite (120 min)

**Key Features:**
- Automatic artifact collection (reports, screenshots, logs)
- Cross-browser matrix testing
- Environment-specific configurations
- Failure notifications and issue creation
- Test result summaries

### Jenkins Integration

Use the provided `Jenkinsfile` for Jenkins pipeline with parameters:
- `TEST_SUITE`: smoke, regression, api, ui, integration, all
- `ENVIRONMENT`: dev, staging, prod
- `BROWSER`: chrome, firefox, edge, all
- `PARALLEL_EXECUTION`: true/false

### Docker Support

Create containerized execution:

```dockerfile
FROM python:3.9

WORKDIR /tests
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install browsers for UI testing
RUN apt-get update && apt-get install -y \
    chromium-browser firefox-esr

COPY . .
CMD ["pytest", "-m", "smoke", "--headless"]
```

## 📊 Reporting

### HTML Reports
- Detailed test execution reports with pytest-html
- Automatic screenshot capture on failures
- Test execution timings and statistics
- Self-contained reports for easy sharing

### Allure Reports
- Advanced reporting with test history and trends
- Rich test documentation with steps and attachments
- Performance metrics and statistics
- Integration with CI/CD pipelines

### Logging
- Structured logging with different levels (DEBUG, INFO, WARNING, ERROR)
- Separate log files for different components
- Console and file logging with configurable formats
- Test execution traceability

## 📋 Best Practices

### 🏗️ Framework Usage

1. **Test Organization**
   - Group tests by functionality in separate classes
   - Use descriptive test names that explain the scenario
   - Apply appropriate markers for test categorization

2. **Page Objects**
   - Keep page objects focused on single pages/components
   - Use descriptive locator names
   - Implement page-specific assertion methods

3. **Keywords Usage**
   - Prefer keywords over direct Selenium calls
   - Create custom keywords for repeated business logic
   - Keep keywords atomic and focused on single actions

4. **Data Management**
   - Use external data files for test data
   - Generate unique data for parallel execution
   - Clean up test data after execution

### 🎯 Assertion Strategy

1. **Hard Assertions**: Core functionality, login, data submission
2. **Soft Assertions**: UI elements, form validation, visual checks
3. **Warning Assertions**: Performance, non-critical features

### 🔄 Test Execution

1. **Local Development**
   ```bash
   # Quick feedback during development
   pytest -m smoke --maxfail=1
   
   # Specific test debugging
   pytest tests/ui/test_login.py::TestLogin::test_valid_login -v -s
   ```

2. **CI/CD Pipeline**
   ```bash
   # Staged execution for comprehensive coverage
   pytest -m smoke && \
   pytest -m "regression and not slow" -n auto && \
   pytest -m "integration"
   ```

## 🔍 Troubleshooting

### Common Issues

#### 1. **WebDriver Issues**

**Problem**: `TypeError: __init__() got an unexpected keyword argument 'executable_path'`
```bash
# Solution: Update to Selenium 4+ compatible driver manager
# The framework handles this automatically, but if you encounter issues:
pip install --upgrade selenium webdriver-manager
```

**Problem**: Browser crashes or hangs
```python
# Solution: Use framework's built-in stability options
# These are automatically applied in browser_config.py
```

#### 2. **Parallel Execution Issues**

**Problem**: Tests interfere with each other
```python
# Solution: Framework provides automatic data isolation
# Each worker gets unique test data automatically
```

**Problem**: Resource conflicts
```python
# Solution: Framework handles automatic cleanup
# Custom cleanup can be added in teardown_method
```

#### 3. **Environment Issues**

**Problem**: Environment configuration not loaded
```bash
# Solution: Verify environment variable
export TEST_ENV=dev
python -c "import os; print(os.getenv('TEST_ENV'))"
```

### Debug Mode

Enable debug logging:

```python
# In pytest.ini (already configured)
log_cli = true
log_cli_level = DEBUG
```

### Performance Debugging

Profile test execution:

```bash
# Use built-in timing in reports
pytest -m smoke --html=reports/timing_report.html
```

## 📚 Additional Resources

### Framework Components
- **Configuration**: Environment-specific settings in `config/`
- **Core**: Base classes and utilities in `core/`
- **Keywords**: Action libraries in `keywords/`
- **Pages**: Page object models in `pages/`
- **Tests**: Test implementations in `tests/`

### External Resources
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Pattern](https://martinfowler.com/bliki/PageObject.html)

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup
```bash
# Fork and clone the repository
git clone <your-fork-url>
cd PyTestSuite_Pro

# Create development branch
git checkout -b feature/your-feature-name

# Install dependencies
pip install -r requirements.txt
```

### Code Standards
- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Add type hints for better code clarity
- **Documentation**: Update docstrings and README for new features
- **Tests**: Add tests for new functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📊 Framework Statistics

- **Total Lines of Code**: ~3,500+
- **Core Modules**: 15+ main components
- **Test Coverage**: Comprehensive framework coverage
- **Supported Browsers**: Chrome, Firefox, Edge
- **Python Versions**: 3.8+
- **Parallel Workers**: Auto-scaling based on CPU cores
- **Test Markers**: 15+ categorization markers

---

## 💡 Quick Tips

**🎯 Getting Started**: Start with `pytest -m smoke` to validate your setup
**⚡ Performance**: Use `pytest -n auto` for faster parallel execution  
**🔍 Debugging**: Use `pytest -v -s` for verbose output and print statements
**📊 Reporting**: Generate reports with `--html=reports/report.html`
**🚀 CI/CD**: The framework includes complete GitHub Actions workflow
**🔑 Keywords**: Use the keywords system for maintainable test code

---

**Happy Testing! 🎉**

For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/your-org/PyTestSuite-Pro).
