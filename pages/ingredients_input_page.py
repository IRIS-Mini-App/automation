"""Page object class for the Ingredients Input screen."""

from typing import Optional, Tuple

from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.webdriver import WebDriver

from utils.custom_keywords import wait_for_visible
from utils.logger import logger


class IngredientsInputPage:
    """Page object representing the Ingredients Input screen.
    
    Attributes:
        INGREDIENTS_PAGE_TITLE_LOCATOR: Locator tuple for the page title element
    """
    
    INGREDIENTS_PAGE_TITLE_LOCATOR: Tuple[str, str] = (
        "xpath",
        "//android.view.View[contains(@text, 'Select') or contains(@content-desc, 'Select')]"
    )

    def __init__(self, driver: WebDriver):
        """Initialize the page object.
        
        Args:
            driver: The WebDriver instance to use
        """
        self.driver = driver
        logger.debug("Initialized IngredientsInputPage")

    def get_ingredients_page_title(self, timeout: int = 10) -> Optional[str]:
        """Get the title text from the ingredients page header.
        
        Args:
            timeout: Maximum time to wait for element in seconds
            
        Returns:
            The title text if found, None otherwise
            
        Raises:
            TimeoutException: If title element is not found within timeout
        """
        logger.debug("Getting ingredients page title")
        element: WebElement = wait_for_visible(
            self.driver,
            self.INGREDIENTS_PAGE_TITLE_LOCATOR,
            timeout=timeout
        )
        
        if element:
            title = element.get_attribute("content-desc")
            logger.debug(f"Found page title: {title}")
            return title
            
        logger.warning("Page title element not found")
        return None
