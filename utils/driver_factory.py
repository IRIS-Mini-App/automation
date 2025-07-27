"""WebDriver factory for creating Appium driver instances."""

import os
import subprocess
import time
from typing import Dict

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException

from utils.logger import logger
from test_settings import (
    PACKAGE_NAME,
    PLATFORM_VERSION,
    DEVICE_NAME,
    APPIUM_HOST,
    APPIUM_PORT,
    APK_NAME
)


def get_driver_options(apk_path: str) -> UiAutomator2Options:
    """Get Appium driver options configuration.
    
    Args:
        apk_path: Full path to the APK file
        
    Returns:
        UiAutomator2Options instance with configured capabilities
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = PLATFORM_VERSION
    options.device_name = DEVICE_NAME
    options.app = apk_path
    options.automation_name = "UiAutomator2"
    options.new_command_timeout = 120
    options.auto_grant_permissions = True
    options.adb_exec_timeout = 120000
    return options


def verify_device_connection() -> None:
    """Verify ADB device connection.
    
    Raises:
        RuntimeError: If no Android devices are connected
        Exception: For other ADB connection failures
    """
    try:
        adb_devices = subprocess.check_output(
            ['adb', 'devices'], 
            universal_newlines=True
        ).strip()
        
        if "device" not in adb_devices:
            logger.error("No connected devices found")
            raise RuntimeError("No Android devices connected")
            
        logger.debug(f"ADB devices:\n{adb_devices}")
            
    except Exception as e:
        logger.error(f"ADB connection failed: {e}")
        raise


def manage_app_installation(reinstall_app: bool) -> None:
    """Manage app installation state based on configuration.
    
    Args:
        reinstall_app: Whether to reinstall the app or just clear data
    """
    if reinstall_app:
        logger.debug(f"Uninstalling package: {PACKAGE_NAME}")
        try:
            subprocess.run(['adb', 'uninstall', PACKAGE_NAME], check=True)
            logger.debug(f"Successfully uninstalled {PACKAGE_NAME}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to uninstall {PACKAGE_NAME}: {e}")
    else:
        logger.debug(f"Clearing app data: {PACKAGE_NAME}")
        try:
            subprocess.run(['adb', 'shell', 'pm', 'clear', PACKAGE_NAME], check=True)
            logger.debug(f"Successfully cleared data for {PACKAGE_NAME}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to clear data for {PACKAGE_NAME}: {e}")


def create_driver(reinstall_app: bool = False) -> WebDriver:
    """Create and configure an Appium WebDriver instance.
    
    Args:
        reinstall_app: Whether to reinstall the app or just clear data
        
    Returns:
        Configured WebDriver instance
        
    Raises:
        FileNotFoundError: If APK file is not found
        WebDriverException: If driver creation fails
    """
    apk_path = os.path.join(os.getcwd(), 'apks', APK_NAME)
    if not os.path.exists(apk_path):
        raise FileNotFoundError(f"APK not found at {apk_path}")
    
    logger.debug(f"APK path: {apk_path}")
    
    verify_device_connection()
    manage_app_installation(reinstall_app)
    
    try:
        # Create driver with modern options approach
        options = get_driver_options(apk_path)
        driver = webdriver.Remote(
            command_executor=f'http://{APPIUM_HOST}:{APPIUM_PORT}',
            options=options
        )
        logger.debug("Successfully created Appium driver")
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to create driver: {e}")
        raise
