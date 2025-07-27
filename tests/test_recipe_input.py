"""Test suite for the recipe input functionality."""



from appium.webdriver.webdriver import WebDriver
from assertpy import assert_that

from pages.ingredients_input_page import IngredientsInputPage
from utils.logger import logger


def test_valid_input_flow(driver: WebDriver) -> None:
    """Test the basic input flow with valid data.
    
    This test verifies:
    1. Page loads successfully
    2. Title is displayed correctly
    3. Title contains expected text
    
    Args:
        driver: WebDriver fixture
    """
    logger.info("Starting test_valid_input_flow")
    
    # Initialize page object
    ingredients_page = IngredientsInputPage(driver)
    
    # Get and verify page title
    title = ingredients_page.get_ingredients_page_title()
    expected_title = 'Select Main Ingredients'
    
    assert_that(title, "Page title")\
        .is_not_none()\
        .is_type_of(str)\
        .contains(expected_title)\
        .is_length(len(expected_title))
        
    logger.info("Page title verified successfully")
