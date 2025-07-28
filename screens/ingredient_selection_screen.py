from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from screens.dish_list_screen import DishListScreen
from utils.custom_keywords import wait_for_visible, click_element, swipe_seek_bar
from utils.logger import logger

DEFAULT_TIMEOUT = 30  # Default timeout in seconds

class IngredientSelectionScreen:
    # Locators
    TITLE = (AppiumBy.XPATH, "//android.view.View[contains(@text, 'Select') or contains(@content-desc, 'Select')]")
    SEEK_BAR = (AppiumBy.XPATH, "//android.widget.SeekBar[@content-desc='50%']")
    FIND_RECIPES_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Find Recipes")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        logger.info("Navigating to Ingredient Selection Screen")
        logger.debug("Initialized IngredientSelectionScreen")

    # Screen Action Methods
    def get_screen_title(self, timeout: int = DEFAULT_TIMEOUT) -> str:
        """Get the title text from the ingredient selection screen header.
        
        Args:
            timeout: Maximum time to wait for element in seconds
            
        Returns:
            The title text if found, None otherwise
            
        Raises:
            TimeoutException: If title element is not found within timeout
        """
        logger.debug("Getting ingredients screen title")
        element = wait_for_visible(self.driver, self.TITLE, timeout=timeout)
        screen_title = element.get_attribute("content-desc")
        logger.debug(f"Found screen title: {screen_title}")
        return screen_title
    
    def select_max_calories(self, timeout: int = DEFAULT_TIMEOUT):
        """Set the seek bar to the maximum calories by performing a swipe action.
        
        Args:
            timeout: Maximum time to wait for element in seconds
            
        Raises:
            TimeoutException: If seek bar element is not found within timeout
        """
        logger.debug("Setting seek bar to maximum calories")
        swipe_seek_bar(self.driver, self.SEEK_BAR, timeout=timeout)
        logger.debug("Seek bar set to maximum calories")

    def select_meat(self, meat: str, timeout: int = DEFAULT_TIMEOUT):
        """Select a meat ingredient by its content description.

        Args:
            meat: The content description of the meat ingredient to select
            timeout: Maximum time to wait for element in seconds
            
        Raises:
            TimeoutException: If meat element is not found within timeout
        """
        logger.debug(f"Selecting meat: {meat}")
        locator = (AppiumBy.XPATH, f"//android.view.View[contains(@content-desc, '{meat}')]")
        click_element(self.driver, locator, timeout=timeout)
        logger.debug(f"Meat '{meat}' selected")

    def select_vegetable(self, vegetable: str, timeout: int = DEFAULT_TIMEOUT):
        """Select a vegetable ingredient by its content description.

        Args:
            vegetable: The content description of the vegetable ingredient to select
            timeout: Maximum time to wait for element in seconds

        Raises:
            TimeoutException: If vegetable element is not found within timeout
        """
        logger.debug(f"Selecting vegetable: {vegetable}")
        locator = (AppiumBy.XPATH, f"//android.view.View[contains(@content-desc, '{vegetable}')]")
        click_element(self.driver, locator, timeout=timeout)
        logger.debug(f"Vegetable '{vegetable}' selected")

    def select_grain_and_starch(self, grain_and_starch: str, timeout: int = DEFAULT_TIMEOUT):
        """Select the Grain & Starch ingredient.

        Args:
            grain_and_starch: The name of the grain/starch ingredient to select
            timeout: Maximum time to wait for element in seconds

        Raises:
            TimeoutException: If Grains & Starches element is not found within timeout
        """
        logger.debug(f"Selecting Grain & Starch: {grain_and_starch}")
        
        # Dùng xpath với contains để tìm element theo content-desc
        locator = (AppiumBy.XPATH, f"//android.view.View[contains(@content-desc, '{grain_and_starch}')]")
        logger.debug(f"Looking for element with content-desc containing: {grain_and_starch}")
        
        click_element(self.driver, locator, timeout=timeout)
        logger.debug(f"Grain & Starch '{grain_and_starch}' selected")

    def click_on_find_recipe_button(self, timeout: int = DEFAULT_TIMEOUT) -> DishListScreen:
        """Click the 'Find Recipe' button to search for recipes based on selected ingredients.

        Args:
            timeout: Maximum time to wait for element in seconds

        Raises:
            TimeoutException: If 'Find Recipe' button is not found within timeout
        """
        logger.debug("Clicking on 'Find Recipe' button")
        click_element(self.driver, self.FIND_RECIPES_BUTTON, timeout=timeout)
        logger.debug("'Find Recipe' button clicked")

        return DishListScreen(self.driver)
