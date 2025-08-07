"""
Dashboard Page Object Model

This module contains the DashboardPage class for handling dashboard functionality
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import List, Dict, Optional

from core import BasePage, assertion_manager


class DashboardPage(BasePage):
    """Dashboard page object with common dashboard functionality"""
    
    # Page URL and identifiers
    page_url = "dashboard"
    page_title = "Dashboard - Application"
    
    # Main dashboard locators
    DASHBOARD_CONTAINER = (By.CSS_SELECTOR, ".dashboard-container")
    PAGE_TITLE = (By.CSS_SELECTOR, "h1.page-title")
    USER_WELCOME_MESSAGE = (By.CSS_SELECTOR, ".welcome-message")
    
    # Navigation and menu
    MAIN_MENU = (By.CSS_SELECTOR, ".main-menu")
    USER_MENU = (By.CSS_SELECTOR, ".user-menu")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "[data-action='logout']")
    PROFILE_LINK = (By.CSS_SELECTOR, "[data-action='profile']")
    SETTINGS_LINK = (By.CSS_SELECTOR, "[data-action='settings']")
    
    # Dashboard widgets/cards
    DASHBOARD_WIDGETS = (By.CSS_SELECTOR, ".dashboard-widget")
    STATS_CARD = (By.CSS_SELECTOR, ".stats-card")
    RECENT_ACTIVITY_CARD = (By.CSS_SELECTOR, ".recent-activity")
    QUICK_ACTIONS_CARD = (By.CSS_SELECTOR, ".quick-actions")
    
    # Quick action buttons
    CREATE_NEW_BUTTON = (By.CSS_SELECTOR, "[data-action='create-new']")
    IMPORT_DATA_BUTTON = (By.CSS_SELECTOR, "[data-action='import-data']")
    EXPORT_DATA_BUTTON = (By.CSS_SELECTOR, "[data-action='export-data']")
    VIEW_REPORTS_BUTTON = (By.CSS_SELECTOR, "[data-action='view-reports']")
    
    # Statistics elements
    TOTAL_USERS_STAT = (By.CSS_SELECTOR, "[data-stat='total-users']")
    ACTIVE_SESSIONS_STAT = (By.CSS_SELECTOR, "[data-stat='active-sessions']")
    REVENUE_STAT = (By.CSS_SELECTOR, "[data-stat='revenue']")
    CONVERSION_RATE_STAT = (By.CSS_SELECTOR, "[data-stat='conversion-rate']")
    
    # Recent activity
    ACTIVITY_LIST = (By.CSS_SELECTOR, ".activity-list")
    ACTIVITY_ITEMS = (By.CSS_SELECTOR, ".activity-item")
    ACTIVITY_ITEM_TITLE = (By.CSS_SELECTOR, ".activity-title")
    ACTIVITY_ITEM_TIME = (By.CSS_SELECTOR, ".activity-time")
    
    # Notifications
    NOTIFICATION_BADGE = (By.CSS_SELECTOR, ".notification-badge")
    NOTIFICATION_DROPDOWN = (By.CSS_SELECTOR, ".notification-dropdown")
    NOTIFICATION_ITEMS = (By.CSS_SELECTOR, ".notification-item")
    
    # Search and filters
    SEARCH_INPUT = (By.CSS_SELECTOR, ".search-input")
    FILTER_DROPDOWN = (By.CSS_SELECTOR, ".filter-dropdown")
    DATE_RANGE_PICKER = (By.CSS_SELECTOR, ".date-range-picker")
    
    def __init__(self, driver: WebDriver = None):
        super().__init__(driver)
        self.page_load_element = self.DASHBOARD_CONTAINER
    
    # Navigation methods
    def open_dashboard(self):
        """Navigate to dashboard page"""
        self.open(self.page_url)
        self.wait_for_page_load()
        self.logger.info("Dashboard page opened")
    
    def logout(self):
        """Logout from dashboard"""
        if self.is_element_present(self.USER_MENU):
            self.click(self.USER_MENU)
        
        self.click(self.LOGOUT_BUTTON)
        self.logger.info("Logout initiated from dashboard")
    
    def navigate_to_profile(self):
        """Navigate to user profile"""
        if self.is_element_present(self.USER_MENU):
            self.click(self.USER_MENU)
        
        self.click(self.PROFILE_LINK)
        self.logger.info("Navigated to profile page")
    
    def navigate_to_settings(self):
        """Navigate to settings page"""
        if self.is_element_present(self.USER_MENU):
            self.click(self.USER_MENU)
        
        self.click(self.SETTINGS_LINK)
        self.logger.info("Navigated to settings page")
    
    # Information retrieval methods
    def get_page_title_text(self) -> str:
        """Get dashboard page title text"""
        return self.get_text(self.PAGE_TITLE)
    
    def get_welcome_message(self) -> str:
        """Get user welcome message"""
        if self.is_element_present(self.USER_WELCOME_MESSAGE):
            return self.get_text(self.USER_WELCOME_MESSAGE)
        return ""
    
    def get_username_from_welcome(self) -> str:
        """Extract username from welcome message"""
        welcome_msg = self.get_welcome_message()
        # Assuming format like "Welcome back, John Doe!"
        if "welcome" in welcome_msg.lower():
            parts = welcome_msg.split(",")
            if len(parts) > 1:
                return parts[1].strip().replace("!", "")
        return ""
    
    # Statistics methods
    def get_dashboard_stats(self) -> Dict[str, str]:
        """Get all dashboard statistics"""
        stats = {}
        
        if self.is_element_present(self.TOTAL_USERS_STAT):
            stats['total_users'] = self.get_text(self.TOTAL_USERS_STAT)
        
        if self.is_element_present(self.ACTIVE_SESSIONS_STAT):
            stats['active_sessions'] = self.get_text(self.ACTIVE_SESSIONS_STAT)
        
        if self.is_element_present(self.REVENUE_STAT):
            stats['revenue'] = self.get_text(self.REVENUE_STAT)
        
        if self.is_element_present(self.CONVERSION_RATE_STAT):
            stats['conversion_rate'] = self.get_text(self.CONVERSION_RATE_STAT)
        
        return stats
    
    def get_total_users(self) -> str:
        """Get total users statistic"""
        if self.is_element_present(self.TOTAL_USERS_STAT):
            return self.get_text(self.TOTAL_USERS_STAT)
        return "0"
    
    def get_active_sessions(self) -> str:
        """Get active sessions statistic"""
        if self.is_element_present(self.ACTIVE_SESSIONS_STAT):
            return self.get_text(self.ACTIVE_SESSIONS_STAT)
        return "0"
    
    def get_revenue(self) -> str:
        """Get revenue statistic"""
        if self.is_element_present(self.REVENUE_STAT):
            return self.get_text(self.REVENUE_STAT)
        return "$0"
    
    def get_conversion_rate(self) -> str:
        """Get conversion rate statistic"""
        if self.is_element_present(self.CONVERSION_RATE_STAT):
            return self.get_text(self.CONVERSION_RATE_STAT)
        return "0%"
    
    # Widget and card methods
    def get_widget_count(self) -> int:
        """Get number of dashboard widgets"""
        widgets = self.find_elements(self.DASHBOARD_WIDGETS)
        return len(widgets)
    
    def is_widget_present(self, widget_selector: tuple) -> bool:
        """Check if specific widget is present"""
        return self.is_element_present(widget_selector)
    
    def get_widget_titles(self) -> List[str]:
        """Get titles of all dashboard widgets"""
        titles = []
        widgets = self.find_elements(self.DASHBOARD_WIDGETS)
        
        for widget in widgets:
            try:
                title_element = widget.find_element(By.CSS_SELECTOR, ".widget-title, h3, h4")
                titles.append(title_element.text)
            except:
                titles.append("Untitled Widget")
        
        return titles
    
    # Quick actions methods
    def click_create_new(self):
        """Click create new button"""
        self.click(self.CREATE_NEW_BUTTON)
        self.logger.info("Create new button clicked")
    
    def click_import_data(self):
        """Click import data button"""
        self.click(self.IMPORT_DATA_BUTTON)
        self.logger.info("Import data button clicked")
    
    def click_export_data(self):
        """Click export data button"""
        self.click(self.EXPORT_DATA_BUTTON)
        self.logger.info("Export data button clicked")
    
    def click_view_reports(self):
        """Click view reports button"""
        self.click(self.VIEW_REPORTS_BUTTON)
        self.logger.info("View reports button clicked")
    
    # Activity methods
    def get_recent_activities(self) -> List[Dict[str, str]]:
        """Get list of recent activities"""
        activities = []
        
        if not self.is_element_present(self.ACTIVITY_LIST):
            return activities
        
        activity_items = self.find_elements(self.ACTIVITY_ITEMS)
        
        for item in activity_items:
            try:
                title = item.find_element(By.CSS_SELECTOR, ".activity-title").text
                time = item.find_element(By.CSS_SELECTOR, ".activity-time").text
                
                activities.append({
                    'title': title,
                    'time': time
                })
            except:
                continue
        
        return activities
    
    def get_activity_count(self) -> int:
        """Get count of recent activity items"""
        activities = self.find_elements(self.ACTIVITY_ITEMS)
        return len(activities)
    
    # Notification methods
    def get_notification_count(self) -> int:
        """Get notification count from badge"""
        if self.is_element_present(self.NOTIFICATION_BADGE):
            badge_text = self.get_text(self.NOTIFICATION_BADGE)
            try:
                return int(badge_text)
            except ValueError:
                return 0
        return 0
    
    def click_notifications(self):
        """Click notifications to open dropdown"""
        self.click(self.NOTIFICATION_BADGE)
        self.logger.info("Notifications clicked")
    
    def get_notifications(self) -> List[str]:
        """Get list of notification texts"""
        notifications = []
        
        if self.is_element_present(self.NOTIFICATION_DROPDOWN):
            notification_items = self.find_elements(self.NOTIFICATION_ITEMS)
            for item in notification_items:
                notifications.append(item.text)
        
        return notifications
    
    # Search and filter methods
    def search(self, search_term: str):
        """Perform search on dashboard"""
        self.type(self.SEARCH_INPUT, search_term)
        self.press_key(self.SEARCH_INPUT, Keys.ENTER)
        self.logger.info(f"Searched for: {search_term}")
    
    def clear_search(self):
        """Clear search input"""
        self.clear(self.SEARCH_INPUT)
        self.logger.info("Search cleared")
    
    def select_filter(self, filter_value: str):
        """Select filter from dropdown"""
        self.click(self.FILTER_DROPDOWN)
        filter_option = (By.XPATH, f"//option[text()='{filter_value}']")
        self.click(filter_option)
        self.logger.info(f"Filter selected: {filter_value}")
    
    # Validation and assertion methods
    def assert_dashboard_loaded(self):
        """Assert that dashboard page is properly loaded"""
        assertion_manager.assert_true(
            self.is_element_present(self.DASHBOARD_CONTAINER),
            "Dashboard container should be present"
        )
        
        assertion_manager.assert_true(
            self.is_element_present(self.PAGE_TITLE),
            "Page title should be present"
        )
        
        # Check that essential widgets are present
        assertion_manager.assert_true(
            self.get_widget_count() > 0,
            "At least one dashboard widget should be present"
        )
    
    def assert_welcome_message_contains_user(self, expected_username: str):
        """Assert welcome message contains expected username"""
        welcome_msg = self.get_welcome_message()
        assertion_manager.assert_contains(
            welcome_msg.lower(),
            expected_username.lower(),
            f"Welcome message should contain username '{expected_username}'"
        )
    
    def assert_statistics_present(self):
        """Assert that key statistics are displayed"""
        stats = self.get_dashboard_stats()
        assertion_manager.assert_true(
            len(stats) > 0,
            "Dashboard should display statistics"
        )
        
        # Check that stats have valid values (not empty or zero)
        for stat_name, stat_value in stats.items():
            assertion_manager.assert_true(
                bool(stat_value.strip()),
                f"Statistic '{stat_name}' should have a value"
            )
    
    def assert_quick_actions_available(self):
        """Assert that quick action buttons are available"""
        quick_actions = [
            (self.CREATE_NEW_BUTTON, "Create New"),
            (self.VIEW_REPORTS_BUTTON, "View Reports")
        ]
        
        for locator, action_name in quick_actions:
            if self.is_element_present(locator):
                assertion_manager.assert_true(
                    self.is_element_visible(locator),
                    f"Quick action '{action_name}' should be visible"
                )
    
    def assert_recent_activity_displayed(self):
        """Assert that recent activity section is displayed"""
        assertion_manager.assert_true(
            self.is_element_present(self.RECENT_ACTIVITY_CARD),
            "Recent activity section should be present"
        )
        
        activity_count = self.get_activity_count()
        assertion_manager.assert_greater_than(
            activity_count,
            0,
            "Recent activity should show at least one activity"
        )
    
    # Utility methods
    def wait_for_stats_to_load(self, timeout: int = 10):
        """Wait for dashboard statistics to load"""
        # Wait for at least one stat element to have non-empty text
        from selenium.webdriver.support.ui import WebDriverWait
        
        def stats_loaded(driver):
            stats = self.get_dashboard_stats()
            return len(stats) > 0 and any(value.strip() for value in stats.values())
        
        try:
            WebDriverWait(self.driver, timeout).until(stats_loaded)
            self.logger.info("Dashboard statistics loaded")
        except:
            self.logger.warning("Dashboard statistics load timeout")
    
    def refresh_dashboard(self):
        """Refresh dashboard page"""
        self.refresh()
        self.wait_for_stats_to_load()
        self.logger.info("Dashboard refreshed")
    
    def take_dashboard_screenshot(self, filename: str = None) -> str:
        """Take screenshot of dashboard"""
        if not filename:
            filename = "dashboard_screenshot.png"
        
        return self.take_screenshot(filename)