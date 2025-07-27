"""PyTest configuration and fixtures for test automation."""

import time
from typing import Generator, Optional

import pytest
from appium.webdriver.webdriver import WebDriver

from utils.driver_factory import create_driver
from utils.appium_launcher import start_appium, stop_appium
from utils.logger import logger
from utils.test_helpers import check_emulator, format_duration
from test_settings import IS_REINSTALL_APP

logger.debug("conftest.py LOADED")

@pytest.fixture(scope="session", autouse=True)
def handle_appium_server(request) -> None:
    """Session fixture to manage Appium server lifecycle.
    
    Args:
        request: PyTest request object for fixture management
    """
    logger.debug("handle_appium_server fixture STARTING")
    check_emulator()
    start_appium()
    logger.debug("handle_appium_server fixture STARTED")
    
    def cleanup() -> None:
        """Clean up Appium server resources."""
        logger.debug("handle_appium_server fixture CLEANING UP") 
        stop_appium()
        logger.debug("handle_appium_server fixture CLEANED UP")
    
    request.addfinalizer(cleanup)

@pytest.fixture
def driver(handle_appium_server, request) -> Generator[WebDriver, None, None]:
    """Create and yield a WebDriver instance for each test.
    
    Yields:
        WebDriver: Configured Appium WebDriver instance
    """
    logger.debug("driver fixture STARTING")
    try:
        test_driver = create_driver()
        
        def cleanup() -> None:
            logger.debug("driver fixture CLEANING UP")
            try:
                if test_driver:
                    test_driver.quit()
            except Exception as e:
                logger.error(f"Failed to quit WebDriver: {e}")
                raise
        
        request.addfinalizer(cleanup)
        yield test_driver
    except Exception as e:
        logger.error(f"Failed to setup test environment: {e}")
        raise

@pytest.fixture(scope="function")
def webdriver(handle_appium_server) -> Generator[WebDriver, None, None]:
    """Create and yield a WebDriver instance with optional app reinstall.
    
    Yields:
        WebDriver: Configured Appium WebDriver instance
    """
    test_driver = create_driver(IS_REINSTALL_APP)
    logger.debug(f"Created driver: {test_driver}")
    yield test_driver
    logger.debug("Quitting driver")
    test_driver.quit()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item) -> None:
    """Set up timing for test execution.
    
    Args:
        item: PyTest item object representing the test
    """
    item._start_time = time.time()
    logger.info(f"Start test: {item.name}")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem) -> None:
    """Log test completion and duration.
    
    Args:
        item: PyTest item object representing the completed test
        nextitem: PyTest item object representing the next test
    """
    start_time = getattr(item, '_start_time', None)
    if start_time:
        duration = time.time() - start_time
        logger.info(f"End test: {item.name}")
        logger.info(f"Total duration: {format_duration(duration)}")
