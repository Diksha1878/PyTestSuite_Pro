"""
Common Page Components

This module contains reusable page components like header, footer, 
navigation menus that are shared across multiple pages.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import List, Dict, Optional

from core import BasePage, assertion_manager


class Header(BasePage):
    """Header component with navigation and user controls"""
    
    # Header container and main elements
    HEADER_CONTAINER = (By.CSS_SELECTOR, "header, .header, .site-header")
    LOGO = (By.CSS_SELECTOR, ".logo, .brand, .site-logo")
    MAIN_NAVIGATION = (By.CSS_SELECTOR, ".main-nav, .primary-nav")
    USER_CONTROLS = (By.CSS_SELECTOR, ".user-controls, .header-actions")
    
    # Navigation links
    HOME_LINK = (By.CSS_SELECTOR, "[data-nav='home'], .nav-home")
    ABOUT_LINK = (By.CSS_SELECTOR, "[data-nav='about'], .nav-about")
    SERVICES_LINK = (By.CSS_SELECTOR, "[data-nav='services'], .nav-services")
    CONTACT_LINK = (By.CSS_SELECTOR, "[data-nav='contact'], .nav-contact")
    DASHBOARD_LINK = (By.CSS_SELECTOR, "[data-nav='dashboard'], .nav-dashboard")
    
    # User controls
    LOGIN_LINK = (By.CSS_SELECTOR, "[data-action='login'], .login-link")
    REGISTER_LINK = (By.CSS_SELECTOR, "[data-action='register'], .register-link")
    USER_AVATAR = (By.CSS_SELECTOR, ".user-avatar, .profile-avatar")
    USER_MENU_TOGGLE = (By.CSS_SELECTOR, ".user-menu-toggle, .profile-dropdown-toggle")
    
    # User dropdown menu
    USER_DROPDOWN = (By.CSS_SELECTOR, ".user-dropdown, .profile-dropdown")
    PROFILE_LINK = (By.CSS_SELECTOR, "[data-action='profile'], .profile-link")
    SETTINGS_LINK = (By.CSS_SELECTOR, "[data-action='settings'], .settings-link")
    LOGOUT_LINK = (By.CSS_SELECTOR, "[data-action='logout'], .logout-link")
    
    # Mobile menu elements
    MOBILE_MENU_TOGGLE = (By.CSS_SELECTOR, ".mobile-menu-toggle, .hamburger-menu")
    MOBILE_MENU = (By.CSS_SELECTOR, ".mobile-menu, .mobile-nav")
    
    def __init__(self, driver: WebDriver = None):
        super().__init__(driver)
    
    # Navigation methods
    def click_logo(self):
        """Click site logo to go to home page"""
        self.click(self.LOGO)
        self.logger.info("Site logo clicked")
    
    def navigate_to_home(self):
        """Navigate to home page"""
        self.click(self.HOME_LINK)
        self.logger.info("Navigated to home page")
    
    def navigate_to_about(self):
        """Navigate to about page"""
        self.click(self.ABOUT_LINK)
        self.logger.info("Navigated to about page")
    
    def navigate_to_services(self):
        """Navigate to services page"""
        self.click(self.SERVICES_LINK)
        self.logger.info("Navigated to services page")
    
    def navigate_to_contact(self):
        """Navigate to contact page"""
        self.click(self.CONTACT_LINK)
        self.logger.info("Navigated to contact page")
    
    def navigate_to_dashboard(self):
        """Navigate to dashboard page"""
        self.click(self.DASHBOARD_LINK)
        self.logger.info("Navigated to dashboard page")
    
    # User control methods
    def click_login(self):
        """Click login link"""
        self.click(self.LOGIN_LINK)
        self.logger.info("Login link clicked")
    
    def click_register(self):
        """Click register link"""
        self.click(self.REGISTER_LINK)
        self.logger.info("Register link clicked")
    
    def open_user_menu(self):
        """Open user dropdown menu"""
        self.click(self.USER_MENU_TOGGLE)
        self.wait_for_element_visible(self.USER_DROPDOWN)
        self.logger.info("User menu opened")
    
    def close_user_menu(self):
        """Close user dropdown menu if open"""
        if self.is_element_visible(self.USER_DROPDOWN):
            # Click outside the menu to close it
            self.click(self.HEADER_CONTAINER)
            self.wait_for_element_invisible(self.USER_DROPDOWN)
            self.logger.info("User menu closed")
    
    def navigate_to_profile(self):
        """Navigate to user profile from header"""
        self.open_user_menu()
        self.click(self.PROFILE_LINK)
        self.logger.info("Navigated to profile from header")
    
    def navigate_to_settings(self):
        """Navigate to settings from header"""
        self.open_user_menu()
        self.click(self.SETTINGS_LINK)
        self.logger.info("Navigated to settings from header")
    
    def logout(self):
        """Logout from header user menu"""
        self.open_user_menu()
        self.click(self.LOGOUT_LINK)
        self.logger.info("Logout clicked from header")
    
    # Mobile menu methods
    def open_mobile_menu(self):
        """Open mobile navigation menu"""
        self.click(self.MOBILE_MENU_TOGGLE)
        self.wait_for_element_visible(self.MOBILE_MENU)
        self.logger.info("Mobile menu opened")
    
    def close_mobile_menu(self):
        """Close mobile navigation menu"""
        if self.is_element_visible(self.MOBILE_MENU):
            self.click(self.MOBILE_MENU_TOGGLE)
            self.wait_for_element_invisible(self.MOBILE_MENU)
            self.logger.info("Mobile menu closed")
    
    # State checking methods
    def is_user_logged_in(self) -> bool:
        """Check if user appears to be logged in based on header elements"""
        return (self.is_element_present(self.USER_AVATAR) or 
                self.is_element_present(self.USER_MENU_TOGGLE))
    
    def is_user_logged_out(self) -> bool:
        """Check if user appears to be logged out based on header elements"""
        return (self.is_element_present(self.LOGIN_LINK) and 
                self.is_element_present(self.REGISTER_LINK))
    
    def get_navigation_links(self) -> List[str]:
        """Get list of visible navigation links"""
        links = []
        nav_elements = self.find_elements(self.MAIN_NAVIGATION)
        
        for nav in nav_elements:
            try:
                link_elements = nav.find_elements(By.TAG_NAME, "a")
                for link in link_elements:
                    if link.is_displayed():
                        links.append(link.text)
            except:
                continue
        
        return links
    
    # Assertion methods
    def assert_header_present(self):
        """Assert that header is present and visible"""
        assertion_manager.assert_true(
            self.is_element_present(self.HEADER_CONTAINER),
            "Header should be present on the page"
        )
        
        assertion_manager.assert_true(
            self.is_element_visible(self.HEADER_CONTAINER),
            "Header should be visible"
        )
    
    def assert_logo_present(self):
        """Assert that site logo is present"""
        assertion_manager.assert_true(
            self.is_element_present(self.LOGO),
            "Site logo should be present in header"
        )
    
    def assert_navigation_present(self):
        """Assert that main navigation is present"""
        assertion_manager.assert_true(
            self.is_element_present(self.MAIN_NAVIGATION),
            "Main navigation should be present in header"
        )
    
    def assert_user_logged_in(self):
        """Assert that user appears to be logged in"""
        assertion_manager.assert_true(
            self.is_user_logged_in(),
            "User should appear to be logged in (avatar/menu present)"
        )
    
    def assert_user_logged_out(self):
        """Assert that user appears to be logged out"""
        assertion_manager.assert_true(
            self.is_user_logged_out(),
            "User should appear to be logged out (login/register links present)"
        )


class Footer(BasePage):
    """Footer component with links and information"""
    
    # Footer container and sections
    FOOTER_CONTAINER = (By.CSS_SELECTOR, "footer, .footer, .site-footer")
    FOOTER_LINKS = (By.CSS_SELECTOR, ".footer-links")
    FOOTER_INFO = (By.CSS_SELECTOR, ".footer-info")
    COPYRIGHT_TEXT = (By.CSS_SELECTOR, ".copyright, .footer-copyright")
    
    # Common footer links
    PRIVACY_LINK = (By.LINK_TEXT, "Privacy Policy")
    TERMS_LINK = (By.LINK_TEXT, "Terms of Service")
    SUPPORT_LINK = (By.LINK_TEXT, "Support")
    FAQ_LINK = (By.LINK_TEXT, "FAQ")
    
    # Social media links
    SOCIAL_LINKS = (By.CSS_SELECTOR, ".social-links")
    FACEBOOK_LINK = (By.CSS_SELECTOR, "[data-social='facebook'], .facebook-link")
    TWITTER_LINK = (By.CSS_SELECTOR, "[data-social='twitter'], .twitter-link")
    LINKEDIN_LINK = (By.CSS_SELECTOR, "[data-social='linkedin'], .linkedin-link")
    
    def __init__(self, driver: WebDriver = None):
        super().__init__(driver)
    
    # Navigation methods
    def click_privacy_policy(self):
        """Click privacy policy link"""
        self.click(self.PRIVACY_LINK)
        self.logger.info("Privacy policy link clicked")
    
    def click_terms_of_service(self):
        """Click terms of service link"""
        self.click(self.TERMS_LINK)
        self.logger.info("Terms of service link clicked")
    
    def click_support(self):
        """Click support link"""
        self.click(self.SUPPORT_LINK)
        self.logger.info("Support link clicked")
    
    def click_faq(self):
        """Click FAQ link"""
        self.click(self.FAQ_LINK)
        self.logger.info("FAQ link clicked")
    
    # Social media methods
    def click_facebook(self):
        """Click Facebook social media link"""
        self.click(self.FACEBOOK_LINK)
        self.logger.info("Facebook link clicked")
    
    def click_twitter(self):
        """Click Twitter social media link"""
        self.click(self.TWITTER_LINK)
        self.logger.info("Twitter link clicked")
    
    def click_linkedin(self):
        """Click LinkedIn social media link"""
        self.click(self.LINKEDIN_LINK)
        self.logger.info("LinkedIn link clicked")
    
    # Information methods
    def get_copyright_text(self) -> str:
        """Get copyright text from footer"""
        if self.is_element_present(self.COPYRIGHT_TEXT):
            return self.get_text(self.COPYRIGHT_TEXT)
        return ""
    
    def get_footer_links(self) -> List[str]:
        """Get list of footer link texts"""
        links = []
        if self.is_element_present(self.FOOTER_LINKS):
            link_elements = self.find_elements((By.CSS_SELECTOR, f"{self.FOOTER_LINKS[1]} a"))
            for link in link_elements:
                links.append(link.text)
        return links
    
    # Assertion methods
    def assert_footer_present(self):
        """Assert that footer is present"""
        assertion_manager.assert_true(
            self.is_element_present(self.FOOTER_CONTAINER),
            "Footer should be present on the page"
        )
    
    def assert_copyright_present(self):
        """Assert that copyright text is present"""
        copyright_text = self.get_copyright_text()
        assertion_manager.assert_true(
            bool(copyright_text),
            "Copyright text should be present in footer"
        )


class NavigationMenu(BasePage):
    """Navigation menu component for sidebar or main navigation"""
    
    # Menu container and items
    MENU_CONTAINER = (By.CSS_SELECTOR, ".navigation-menu, .sidebar-menu, .nav-menu")
    MENU_ITEMS = (By.CSS_SELECTOR, ".menu-item, .nav-item")
    ACTIVE_ITEM = (By.CSS_SELECTOR, ".menu-item.active, .nav-item.active")
    
    # Common menu sections
    DASHBOARD_ITEM = (By.CSS_SELECTOR, "[data-menu='dashboard']")
    USERS_ITEM = (By.CSS_SELECTOR, "[data-menu='users']")
    REPORTS_ITEM = (By.CSS_SELECTOR, "[data-menu='reports']")
    SETTINGS_ITEM = (By.CSS_SELECTOR, "[data-menu='settings']")
    
    # Expandable menu items
    EXPANDABLE_ITEMS = (By.CSS_SELECTOR, ".menu-item.expandable")
    SUBMENU_ITEMS = (By.CSS_SELECTOR, ".submenu-item")
    
    def __init__(self, driver: WebDriver = None):
        super().__init__(driver)
    
    # Navigation methods
    def click_menu_item(self, menu_item_locator: tuple):
        """Click specific menu item"""
        self.click(menu_item_locator)
        self.logger.info(f"Menu item clicked: {menu_item_locator}")
    
    def navigate_to_dashboard(self):
        """Navigate to dashboard via menu"""
        self.click(self.DASHBOARD_ITEM)
        self.logger.info("Navigated to dashboard via menu")
    
    def navigate_to_users(self):
        """Navigate to users section via menu"""
        self.click(self.USERS_ITEM)
        self.logger.info("Navigated to users via menu")
    
    def navigate_to_reports(self):
        """Navigate to reports section via menu"""
        self.click(self.REPORTS_ITEM)
        self.logger.info("Navigated to reports via menu")
    
    def navigate_to_settings(self):
        """Navigate to settings via menu"""
        self.click(self.SETTINGS_ITEM)
        self.logger.info("Navigated to settings via menu")
    
    # Menu state methods
    def get_menu_items(self) -> List[str]:
        """Get list of menu item texts"""
        items = []
        menu_elements = self.find_elements(self.MENU_ITEMS)
        
        for item in menu_elements:
            if item.is_displayed():
                items.append(item.text)
        
        return items
    
    def get_active_menu_item(self) -> str:
        """Get text of currently active menu item"""
        if self.is_element_present(self.ACTIVE_ITEM):
            return self.get_text(self.ACTIVE_ITEM)
        return ""
    
    def expand_menu_item(self, item_locator: tuple):
        """Expand a collapsible menu item"""
        if self.is_element_present(item_locator):
            # Check if item has submenu
            item_element = self.find_element(item_locator)
            if "expandable" in (item_element.get_attribute("class") or ""):
                self.click(item_locator)
                self.logger.info(f"Expanded menu item: {item_locator}")
    
    # Assertion methods
    def assert_menu_present(self):
        """Assert that navigation menu is present"""
        assertion_manager.assert_true(
            self.is_element_present(self.MENU_CONTAINER),
            "Navigation menu should be present"
        )
    
    def assert_menu_item_active(self, expected_item: str):
        """Assert that specific menu item is active"""
        active_item = self.get_active_menu_item()
        assertion_manager.assert_equals(
            active_item.lower(),
            expected_item.lower(),
            f"Menu item '{expected_item}' should be active"
        )
    
    def assert_menu_items_present(self, expected_items: List[str]):
        """Assert that expected menu items are present"""
        menu_items = self.get_menu_items()
        
        for expected_item in expected_items:
            assertion_manager.assert_contains(
                menu_items,
                expected_item,
                f"Menu should contain item '{expected_item}'"
            )