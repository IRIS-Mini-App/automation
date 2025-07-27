"""Tests for the recipe input flow."""

from appium.webdriver.webdriver import WebDriver
from assertpy import assert_that

from screens.ingredient_selection_screen import IngredientSelectionScreen
from utils.constants import INGREDIENT_SELECTION_TITLE
from utils.logger import logger


def test_valid_input_flow(driver: WebDriver):
    """Test valid input flow for recipe ingredients.
    
    Args:
        driver: WebDriver instance for the test
    """
    logger.info("Starting test_valid_input_flow")
    
    ingredients_screen = IngredientSelectionScreen(driver)
    title = ingredients_screen.get_screen_title()
    expected_title = INGREDIENT_SELECTION_TITLE
    
    assert_that(title, "Screen title")\
        .is_not_none()\
        .is_type_of(str)\
        .is_length(len(expected_title))\
        .contains(expected_title)

    logger.info("Screen title verified successfully")
