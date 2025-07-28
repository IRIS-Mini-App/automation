from time import sleep
from appium.webdriver.webdriver import WebDriver
from screens.dish_detail_screen import DishDetailScreen
from utils.custom_keywords import click_element, wait_for_visible
from utils.logger import logger
from appium.webdriver.common.appiumby import AppiumBy

DEFAULT_TIMEOUT = 30  


class DishListScreen:
    """Page object for the Dish List screen."""
    FOUND_RECIPES_MESSAGE = (AppiumBy.XPATH, "//android.view.View[@content-desc='Found 5 matching recipes']")
    SEE_RECIPE_BUTTON = (AppiumBy.XPATH, "(//android.widget.Button[@content-desc='See Recipe'])[1]")

    def __init__(self, driver: WebDriver):
        """Initialize the dish list screen and wait for it to load.
        
        Args:
            driver: The WebDriver instance to control the screen
            
        Raises:
            TimeoutException: If the screen doesn't load within the default timeout
        """
        self.driver = driver
        logger.info("Waiting for Dish List Screen to load")
        sleep(60)
        logger.info("Navigating to Dish List Screen")
        logger.debug("Initializing DishListScreen")
    
    # Screen Action Methods
    def dish_list_is_loaded(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Check if the dish list is loaded and recipes are found.
        
        Args:
            timeout: Maximum time to wait for element in seconds
            
        Returns:
            True if dish list is loaded, False otherwise
        """
        wait_for_visible(self.driver, self.FOUND_RECIPES_MESSAGE, timeout=timeout)
        logger.debug("Dish list loaded successfully")
        return True
    
    def click_see_recipe_button(self, timeout: int = DEFAULT_TIMEOUT) -> DishDetailScreen:
        """Click the 'See Recipe' button for the first recipe.
        
        Args:
            timeout: Maximum time to wait for element in seconds

        Returns:
            An instance of DishDetailScreen
        """
        logger.debug("Clicking 'See Recipe' button")
        click_element(self.driver, self.SEE_RECIPE_BUTTON, timeout=timeout)
        logger.debug("'See Recipe' button clicked")
        return DishDetailScreen(self.driver)
