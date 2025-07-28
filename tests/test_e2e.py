from appium.webdriver.webdriver import WebDriver
from assertpy import assert_that

from screens.splash_screen import SplashScreen
from screens.ingredient_selection_screen import IngredientSelectionScreen
from utils.logger import logger


def test_can_navigate_to_splash_screen(driver: WebDriver):
    splash_screen = SplashScreen(driver)
    splash_screen.app_title_and_slogan_are_displayed()

def test_full_flow(driver: WebDriver):
    # Splash screen
    splash_screen = SplashScreen(driver)
    splash_screen.app_title_and_slogan_are_displayed()

    # Ingredient selection screen
    ingredient_screen = IngredientSelectionScreen(driver)
    ingredient_screen.select_max_calories()
    ingredient_screen.select_meat("Beef")
    ingredient_screen.select_vegetable("Tomato") 
    ingredient_screen.select_grain_and_starch("Noodles")
    dish_list_screen = ingredient_screen.click_on_find_recipe_button()

    # Dish list screen
    assert_that(dish_list_screen.dish_list_is_loaded(), "Dish list is not loaded").is_true()
    dish_detail = dish_list_screen.click_see_recipe_button()

    # Dish detail screen
    assert_that(
        dish_detail.dish_detail_screen_is_displayed(),
        "Dish detail screen is not displayed"
    ).is_true()
    dish_name = dish_detail.get_dish_name()
    logger.info(f"Dish name: {dish_name}")
    assert_that(
        dish_detail.instructions_is_displayed(),
        "Instructions are not displayed"
    ).is_true()
    dish_detail.click_save_recipe_button()
    # assert_that(
    #     dish_detail.add_to_favorites_success_message_is_displayed(dish_name),
    #     "Success message is not displayed"
    # ).is_true()

    logger.info("End of test_full_flow")
