from typing import Optional
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from utils.custom_keywords import wait_for_visible, get_text
from utils.logger import logger


class DishDetailScreen:
    # Locators
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        logger.debug("Initialized DishDetailScreen")

    # Screen Action Methods    
