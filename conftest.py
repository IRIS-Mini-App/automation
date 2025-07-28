"""PyTest configuration and fixtures for test automation."""

import time
from typing import Generator
import pytest

import pytest
from appium.webdriver.webdriver import WebDriver

from utils.driver_factory import create_driver
from utils.appium_launcher import start_appium, stop_appium
from utils.logger import logger
from utils.test_helpers import check_emulator, format_duration, ScreenValidator
from test_settings import IS_REINSTALL_APP

logger.debug("conftest.py LOADED")

# Global validator instance
screen_validator = ScreenValidator()

@pytest.fixture(scope="session", autouse=True)
def validate_code(request) -> None:
    """Session fixture to validate code before any tests run."""
    logger.debug("Starting code validation...")
    try:
        screen_validator.validate_all_test_files()
        if screen_validator.validation_result["errors"]:
            error_msg = screen_validator.format_validation_errors()
            if error_msg:  # Only fail if we have an actual error message
                pytest.fail(str(error_msg))
    except Exception as e:
        logger.error(f"Failed to validate test files: {str(e)}")
        raise
    logger.debug("Code validation completed successfully")

@pytest.fixture(scope="session", autouse=True)
def handle_appium_server(validate_code, request) -> None:
    """Session fixture to manage Appium server lifecycle.
    Args:
        validate_code: Previous fixture that validates code
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
def driver(request) -> Generator[WebDriver, None, None]:
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
            except (ConnectionError, TimeoutError) as e:
                logger.error(f"Failed to quit WebDriver: {e}")
                raise
        
        request.addfinalizer(cleanup)
        yield test_driver
    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Failed to setup test environment: {e}")
        raise

@pytest.fixture(scope="function")
def webdriver() -> Generator[WebDriver, None, None]:
    """Create and yield a WebDriver instance with optional app reinstall.
    Yields:
        WebDriver: Configured Appium WebDriver instance
    """
    test_driver = create_driver(IS_REINSTALL_APP)
    logger.debug(f"Created driver: {test_driver}")
    try:
        yield test_driver
    finally:
        logger.debug("Quitting driver")
        test_driver.quit()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Set up timing for test execution.
    Args:
        item: PyTest item object representing the test
    """
    item.start_time = time.time()
    logger.info(f"Start test: {item.name}")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item) -> None:
    """Log test completion and duration.
    Args:
        item: PyTest item object representing the completed test
    """
    start_time = getattr(item, 'start_time', None)
    if start_time:
        duration = time.time() - start_time
        logger.info(f"End test: {item.name}")
        logger.info(f"Total duration: {format_duration(duration)}")
