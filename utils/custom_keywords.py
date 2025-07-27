"""Custom keywords for mobile UI automation."""

from typing import List, Tuple, Optional

from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.logger import logger

LocatorType = Tuple[str, str]


def wait_for_visible(driver: WebDriver, locator: LocatorType, timeout: int = 10, poll_frequency: float = 0.2) -> Optional[WebElement]:
    """Wait for an element to be visible with fluent wait.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (by, value) e.g., ("xpath", "//android.view.View")
        timeout: Maximum time to wait in seconds
        poll_frequency: How often to poll in seconds
        
    Returns:
        WebElement if found and visible
        
    Raises:
        TimeoutException: If element is not visible within timeout
    """
    wait = WebDriverWait(driver, timeout, poll_frequency=poll_frequency)
    element = wait.until(EC.visibility_of_element_located(locator))
    logger.debug(f"Element found and visible: {locator}")
    return element
        

def get_element(driver: WebDriver, locator: LocatorType) -> WebElement:
    """Get a single element, raising an exception if not found.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (by, value)
        
    Returns:
        Found WebElement
        
    Raises:
        NoSuchElementException: If element is not found
    """
    element = driver.find_element(*locator)
    logger.debug(f"Found element: {locator}")
    return element


def get_elements(driver: WebDriver, locator: LocatorType) -> List[WebElement]:
    """Get all matching elements, raising an exception if none found.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (by, value)
        
    Returns:
        List of found WebElements
        
    Raises:
        Exception: If no elements are found
    """
    elements = driver.find_elements(*locator)
    if not elements:
        error_msg = f"No elements found with locator: {locator}"
        logger.error(error_msg)
        raise Exception(error_msg)
        
    logger.debug(f"Found {len(elements)} elements with locator: {locator}")
    return elements

