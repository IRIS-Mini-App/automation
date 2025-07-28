from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from utils.custom_keywords import wait_for_visible
from utils.logger import logger
from utils.constants import SPLASH_APP_TITLE, SPLASH_APP_SLOGAN

DEFAULT_TIMEOUT = 30  # Default timeout in seconds


class SplashScreen:
    # Locators
    APP_TITLE_TXT = (AppiumBy.ACCESSIBILITY_ID, SPLASH_APP_TITLE)
    APP_SLOGAN_TXT = (AppiumBy.ACCESSIBILITY_ID, SPLASH_APP_SLOGAN)

    def __init__(self, driver: WebDriver):
        self.driver = driver
        logger.info("Navigating to Splash Screen")
        logger.debug("Initialized SplashScreen")
    
    # Screen Action Methods
    def app_title_and_slogan_are_displayed(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Check if the app title and slogan are displayed on the splash screen.

        Args:
            timeout: Maximum time to wait for element in seconds
            
        Returns:
            True if both elements are found and displayed
            
        Raises:
            TimeoutException: If either element is not found or not visible
        """
        wait_for_visible(self.driver, self.APP_TITLE_TXT, timeout=timeout)
        wait_for_visible(self.driver, self.APP_SLOGAN_TXT, timeout=timeout)
        return True
