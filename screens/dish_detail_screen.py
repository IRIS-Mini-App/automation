from appium.webdriver.webdriver import WebDriver
from utils.custom_keywords import click_element, wait_for_visible
from utils.logger import logger
from appium.webdriver.common.appiumby import AppiumBy

DEFAULT_TIMEOUT = 30  # Default timeout in seconds


class DishDetailScreen:
    """Page object for the Dish Detail screen."""
    SAVE_RECIPE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Save Recipe")
    INSTRUCTIONS_TEXT = (AppiumBy.XPATH, "//android.view.View[@content-desc='Instructions']")
    DISH = (AppiumBy.CLASS_NAME, "android.widget.ImageView")

    def __init__(self, driver: WebDriver):
        """Initialize the dish detail screen.
        
        Args:
            driver: The WebDriver instance to control the screen
        """
        self.driver = driver
        logger.info("Navigating to Dish Detail Screen")
        logger.debug("Initialized DishDetailScreen")

    # Screen Action Methods
    def dish_detail_screen_is_displayed(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Check if the dish detail screen is displayed.

        Args:
            timeout: Maximum time to wait for element in seconds

        Returns:
            True if dish detail screen is displayed, False otherwise
        """
        wait_for_visible(self.driver, self.SAVE_RECIPE_BUTTON, timeout=timeout)
        return True
    
    def instructions_is_displayed(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Check if the instructions text is displayed.

        Args:
            timeout: Maximum time to wait for element in seconds

        Returns:
            True if instructions text is displayed, False otherwise
        """
        wait_for_visible(self.driver, self.INSTRUCTIONS_TEXT, timeout=timeout)
        return True
    
    def click_save_recipe_button(self, timeout: int = DEFAULT_TIMEOUT):
        """Click the 'Save Recipe' button.

        Args:
            timeout: Maximum time to wait for element in seconds
        """
        click_element(self.driver, self.SAVE_RECIPE_BUTTON, timeout=timeout)

    def get_dish_name(self, timeout: int = DEFAULT_TIMEOUT) -> str:
        """Get the dish name from the dish detail screen.

        Args:
            timeout: Maximum time to wait for element in seconds

        Returns:
            The dish name if found, None otherwise
        """
        dish_name = wait_for_visible(self.driver, self.DISH, timeout=timeout).get_attribute("content-desc")
        logger.debug(f"Found dish name: {dish_name}")
        return dish_name

    def add_to_favorites_success_message_is_displayed(self, dish_name: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Check if the success message after adding a dish to favorites is displayed.

        Args:
            dish_name: The name of the dish to check in the success message
            timeout: Maximum time to wait for element in seconds

        Returns:
            True if success message is displayed, False otherwise
        """
        success_message_locator = (AppiumBy.XPATH, f"//android.view.View[@content-desc='{dish_name} added to favorites']")
        return wait_for_visible(self.driver, success_message_locator, timeout=timeout) is not None
