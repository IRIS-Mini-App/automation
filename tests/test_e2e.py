from appium.webdriver.webdriver import WebDriver
from assertpy import assert_that

from screens.splash_screen import SplashScreen
from utils.logger import logger


def test_can_navigate_to_splash_screen(driver: WebDriver):
    logger.debug("Starting test_can_navigate_to_splash_screen")

    splash_screen = SplashScreen(driver)
    assert_that(splash_screen.app_title_and_slogan_are_displayed(), 
                "App title and slogan are displayed").is_true()

    logger.debug("Screen title verified successfully")
