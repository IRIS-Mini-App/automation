from typing import Optional
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from utils.custom_keywords import wait_for_visible
from utils.logger import logger


class IngredientSelectionScreen:
    # Locators
    TITLE = (AppiumBy.XPATH, f"//android.view.View[contains(@text, 'Select') or contains(@content-desc, 'Select')]")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        logger.debug("Initialized IngredientSelectionScreen")

    # Screen Action Methods
    def get_screen_title(self, timeout: int = 10) -> str:
        """Get the title text from the ingredient selection screen header.
        
        Args:
            timeout: Maximum time to wait for element in seconds
            
        Returns:
            The title text if found, None otherwise
            
        Raises:
            TimeoutException: If title element is not found within timeout
        """
        logger.debug("Getting ingredients screen title")
        screen_title = wait_for_visible(self.driver, self.TITLE, timeout=timeout).get_attribute("content-desc")
        logger.debug(f"Found screen title: {screen_title}")
        return screen_title
