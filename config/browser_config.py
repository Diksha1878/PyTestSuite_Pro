"""
Browser Configuration Module for PyTestSuite Pro

This module handles browser-specific configurations and capabilities
for Chrome, Firefox, and Edge browsers with support for local and remote execution.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os


@dataclass
class BrowserCapabilities:
    """Browser capabilities configuration"""
    browser_name: str
    version: Optional[str] = None
    platform: Optional[str] = None
    headless: bool = False
    window_size: tuple = (1920, 1080)
    download_dir: Optional[str] = None
    extensions: List[str] = field(default_factory=list)
    prefs: Dict[str, Any] = field(default_factory=dict)
    arguments: List[str] = field(default_factory=list)
    experimental_options: Dict[str, Any] = field(default_factory=dict)
    mobile_emulation: Optional[Dict[str, Any]] = None


class BrowserConfigManager:
    """Manages browser configurations and options"""
    
    def __init__(self):
        self.default_timeout = 10
        self.download_directory = os.path.join(os.getcwd(), "downloads")
        self._ensure_download_directory()
    
    def _ensure_download_directory(self):
        """Create download directory if it doesn't exist"""
        os.makedirs(self.download_directory, exist_ok=True)
    
    def get_chrome_options(self, capabilities: BrowserCapabilities = None) -> ChromeOptions:
        """Configure Chrome browser options"""
        options = ChromeOptions()
        
        if capabilities is None:
            capabilities = self.get_default_chrome_capabilities()
        
        # Basic Chrome arguments
        default_args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-infobars',
            '--disable-notifications',
            '--disable-popup-blocking',
            '--disable-translate',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-features=TranslateUI,BlinkGenPropertyTrees',
            '--remote-debugging-port=9222'
        ]
        
        # Add default arguments
        for arg in default_args:
            options.add_argument(arg)
        
        # Add custom arguments
        for arg in capabilities.arguments:
            options.add_argument(arg)
        
        # Set window size
        if capabilities.window_size:
            options.add_argument(f'--window-size={capabilities.window_size[0]},{capabilities.window_size[1]}')
        
        # Enable headless mode if specified
        if capabilities.headless:
            options.add_argument('--headless')
        
        # Configure download preferences
        download_prefs = {
            'profile.default_content_settings.popups': 0,
            'download.default_directory': capabilities.download_dir or self.download_directory,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        }
        
        # Merge with custom preferences
        prefs = {**download_prefs, **capabilities.prefs}
        options.add_experimental_option('prefs', prefs)
        
        # Add experimental options
        for key, value in capabilities.experimental_options.items():
            options.add_experimental_option(key, value)
        
        # Mobile emulation
        if capabilities.mobile_emulation:
            options.add_experimental_option('mobileEmulation', capabilities.mobile_emulation)
        
        # Add extensions
        for extension in capabilities.extensions:
            options.add_extension(extension)
        
        return options
    
    def get_firefox_options(self, capabilities: BrowserCapabilities = None) -> FirefoxOptions:
        """Configure Firefox browser options"""
        options = FirefoxOptions()
        
        if capabilities is None:
            capabilities = self.get_default_firefox_capabilities()
        
        # Enable headless mode if specified
        if capabilities.headless:
            options.add_argument('--headless')
        
        # Set window size
        if capabilities.window_size:
            options.add_argument(f'--width={capabilities.window_size[0]}')
            options.add_argument(f'--height={capabilities.window_size[1]}')
        
        # Add custom arguments
        for arg in capabilities.arguments:
            options.add_argument(arg)
        
        # Configure preferences
        default_prefs = {
            'browser.download.folderList': 2,
            'browser.download.manager.showWhenStarting': False,
            'browser.download.dir': capabilities.download_dir or self.download_directory,
            'browser.helperApps.neverAsk.saveToDisk': 'application/pdf,application/octet-stream,text/csv',
            'pdfjs.disabled': True
        }
        
        # Merge with custom preferences
        prefs = {**default_prefs, **capabilities.prefs}
        for key, value in prefs.items():
            options.set_preference(key, value)
        
        return options
    
    def get_edge_options(self, capabilities: BrowserCapabilities = None) -> EdgeOptions:
        """Configure Edge browser options"""
        options = EdgeOptions()
        
        if capabilities is None:
            capabilities = self.get_default_edge_capabilities()
        
        # Basic Edge arguments (similar to Chrome)
        default_args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-infobars',
            '--disable-notifications',
            '--disable-popup-blocking'
        ]
        
        # Add default arguments
        for arg in default_args:
            options.add_argument(arg)
        
        # Add custom arguments
        for arg in capabilities.arguments:
            options.add_argument(arg)
        
        # Set window size
        if capabilities.window_size:
            options.add_argument(f'--window-size={capabilities.window_size[0]},{capabilities.window_size[1]}')
        
        # Enable headless mode if specified
        if capabilities.headless:
            options.add_argument('--headless')
        
        # Configure download preferences
        download_prefs = {
            'profile.default_content_settings.popups': 0,
            'download.default_directory': capabilities.download_dir or self.download_directory,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        }
        
        # Merge with custom preferences
        prefs = {**download_prefs, **capabilities.prefs}
        options.add_experimental_option('prefs', prefs)
        
        # Add experimental options
        for key, value in capabilities.experimental_options.items():
            options.add_experimental_option(key, value)
        
        return options
    
    def get_default_chrome_capabilities(self) -> BrowserCapabilities:
        """Get default Chrome browser capabilities"""
        return BrowserCapabilities(
            browser_name='chrome',
            headless=False,
            window_size=(1920, 1080),
            arguments=[
                '--start-maximized',
                '--disable-web-security',
                '--allow-running-insecure-content'
            ],
            prefs={
                'profile.default_content_setting_values.notifications': 2,
                'profile.managed_default_content_settings.images': 2  # Block images for faster loading
            }
        )
    
    def get_default_firefox_capabilities(self) -> BrowserCapabilities:
        """Get default Firefox browser capabilities"""
        return BrowserCapabilities(
            browser_name='firefox',
            headless=False,
            window_size=(1920, 1080),
            prefs={
                'dom.webnotifications.enabled': False,
                'media.volume_scale': '0.0'
            }
        )
    
    def get_default_edge_capabilities(self) -> BrowserCapabilities:
        """Get default Edge browser capabilities"""
        return BrowserCapabilities(
            browser_name='edge',
            headless=False,
            window_size=(1920, 1080),
            arguments=['--start-maximized']
        )
    
    def get_mobile_emulation_config(self, device_name: str) -> Dict[str, Any]:
        """Get mobile emulation configuration for Chrome"""
        mobile_devices = {
            'iPhone 12': {
                'deviceName': 'iPhone 12'
            },
            'iPhone 12 Pro': {
                'deviceName': 'iPhone 12 Pro'
            },
            'Pixel 5': {
                'deviceName': 'Pixel 5'
            },
            'iPad': {
                'deviceName': 'iPad'
            },
            'custom': {
                'deviceMetrics': {
                    'width': 375,
                    'height': 812,
                    'pixelRatio': 3.0
                },
                'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
            }
        }
        
        return mobile_devices.get(device_name, mobile_devices['custom'])


# Global browser config manager instance
browser_config = BrowserConfigManager()

# Predefined browser capability configurations for common scenarios
BROWSER_CONFIGS = {
    'chrome_headless': BrowserCapabilities(
        browser_name='chrome',
        headless=True,
        arguments=['--window-size=1920,1080', '--disable-gpu']
    ),
    
    'chrome_debug': BrowserCapabilities(
        browser_name='chrome',
        headless=False,
        arguments=['--start-maximized', '--remote-debugging-port=9222'],
        experimental_options={'useAutomationExtension': False}
    ),
    
    'firefox_headless': BrowserCapabilities(
        browser_name='firefox',
        headless=True,
        arguments=['--width=1920', '--height=1080']
    ),
    
    'edge_headless': BrowserCapabilities(
        browser_name='edge',
        headless=True,
        arguments=['--window-size=1920,1080', '--disable-gpu']
    ),
    
    'chrome_mobile': BrowserCapabilities(
        browser_name='chrome',
        mobile_emulation={'deviceName': 'iPhone 12'},
        arguments=['--disable-web-security']
    )
}