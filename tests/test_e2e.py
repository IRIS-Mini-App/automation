from appium.webdriver.webdriver import WebDriver
from assertpy import assert_that

from screens.dish_list_screen import DishListScreen
from screens.splash_screen import SplashScreen
from screens.ingredient_selection_screen import IngredientSelectionScreen
from utils.logger import logger


def test_can_navigate_to_splash_screen(driver: WebDriver):
    splash_screen = SplashScreen(driver)
    splash_screen.app_title_and_slogan_are_displayed()
    splash_screen.app_version_is_displayed()

def test_full_flow(driver: WebDriver):
    splash_screen = SplashScreen(driver)
    splash_screen.app_title_and_slogan_are_displayed()

    ingredient_screen = IngredientSelectionScreen(driver)
    ingredient_screen.clear_selections()
    ingredient_screen.select_grain_and_starch("Rice")
    ingredient_screen.verify_ingredients_selected()
    dish_list = ingredient_screen.click_on_find_recipe_button()

    dish_list.dish_list_is_loaded()
    dish_detail = dish_list.click_see_recipe_button()
    
    dish_detail.recipe_details_loaded()

    logger.info("End of test_full_flow")

