"""Custom keywords for mobile UI automation."""

from time import time, sleep
from typing import List, Tuple, Optional

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from utils.logger import logger

LocatorType = Tuple[str, str]


def scroll_down(driver: WebDriver) -> None:
    """Perform a scroll down action on the screen.
    
    Args:
        driver: WebDriver instance to perform the scroll
    """
    window_size = driver.get_window_size()
    screen_height = window_size['height']
    screen_width = window_size['width']
    
    # Calculate scroll positions
    start_y = int(screen_height * 0.7)
    end_y = int(screen_height * 0.3)
    center_x = screen_width // 2

    try:
        # Perform scroll
        driver.swipe(
            start_x=center_x,
            start_y=start_y,
            end_x=center_x,
            end_y=end_y,
            duration=1000
        )
        logger.debug(f"Performed scroll: {start_y} -> {end_y}")
        sleep(1)  # Wait for scroll to complete
    except Exception as e:
        logger.error(f"Error during scroll: {str(e)}")
        raise

def wait_for_visible(driver: WebDriver, locator: LocatorType, 
                   timeout: int = 10, poll_frequency: float = 0.2,
                   is_scrollable: bool = True) -> Optional[WebElement]:
    """Wait for an element to be visible with fluent wait. First tries to find the element without
    scrolling, then scrolls if necessary within the timeout period until the element is found and visible.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (by, value) e.g., ("xpath", "//android.view.View")
        timeout: Maximum time to wait in seconds
        poll_frequency: How often to poll in seconds
        is_scrollable: Whether to scroll to find element if not visible initially
        
    Returns:
        WebElement if found and visible
        
    Raises:
        TimeoutException: If element is not visible within timeout
    """
    start_time = time()
    end_time = start_time + timeout
    attempts = 0
    max_attempts = 10

    while time() < end_time:
        try:
            element = driver.find_element(*locator)
            if element.is_displayed():
                logger.debug(f"Element found and visible: {locator}")
                return element
        except:
            pass

        if not is_scrollable or attempts >= max_attempts:
            sleep(poll_frequency)
            continue

        logger.debug(f"Scroll attempt {attempts + 1}")
        try:
            scroll_down(driver)
            attempts += 1
            sleep(poll_frequency)  # Wait after scroll
        except Exception as e:
            logger.error(f"Failed to scroll: {str(e)}")
            attempts += 1
            sleep(poll_frequency)  # Wait after error

    raise TimeoutException(f"Element not found or not visible after {timeout} seconds: {locator}")


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


def click_element(driver: WebDriver, locator: LocatorType, timeout: int = 10) -> None:
    """Click on an element after ensuring it's visible.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (by, value)
        timeout: Maximum time to wait for element in seconds
        
    Raises:
        TimeoutException: If element is not visible within timeout
    """
    element = wait_for_visible(driver, locator, timeout=timeout)
    element.click()
    logger.debug(f"Clicked element: {locator}")
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
    window_size = driver.get_window_size()
    screen_height = window_size['height']
    screen_width = window_size['width']
    
    # Calculate scroll positions
    start_y = int(screen_height * 0.7)
    end_y = int(screen_height * 0.3)
    center_x = screen_width // 2

    try:
        # Perform scroll
        driver.swipe(
            start_x=center_x,
            start_y=start_y,
            end_x=center_x,
            end_y=end_y,
            duration=1000
        )
        logger.debug(f"Performed scroll: {start_y} -> {end_y}")
        sleep(1)  # Wait for scroll to complete
    except Exception as e:
        logger.error(f"Error during scroll: {str(e)}")
        raise

def swipe_seek_bar(driver: WebDriver, locator: LocatorType, start_percent: float = 0.5, 
                  end_percent: float = 0.95, timeout: int = 10) -> None:
    """Swipe a seek bar from one percentage to another.
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (by, value) for the seek bar
        start_percent: Starting position as a percentage (0.0 to 1.0)
        end_percent: Ending position as a percentage (0.0 to 1.0)
        timeout: Maximum time to wait for element in seconds
        
    Raises:
        TimeoutException: If seek bar element is not found within timeout
        ValueError: If percentages are not between 0 and 1
    """
    if not 0 <= start_percent <= 1 or not 0 <= end_percent <= 1:
        raise ValueError("Percentages must be between 0 and 1")
        
    logger.debug(f"Swiping seek bar from {start_percent*100}% to {end_percent*100}%")
    
    # Wait for seek bar to be visible
    seek_bar = wait_for_visible(driver, locator, timeout=timeout)
    
    # Get the seek bar location and size
    location = seek_bar.location
    size = seek_bar.size
    
    # Calculate start and end points for the swipe
    start_x = location['x'] + (size['width'] * start_percent)
    end_x = location['x'] + (size['width'] * end_percent)
    y = location['y'] + (size['height'] / 2)  # Keep Y at the middle
    
    # Perform the swipe action
    driver.swipe(
        start_x=int(start_x),
        start_y=int(y),
        end_x=int(end_x),
        end_y=int(y),
        duration=500  # Duration in ms, slower for more precise control
    )
    
    logger.debug("Seek bar swipe completed")
