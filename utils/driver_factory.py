"""WebDriver factory for creating Appium driver instances."""

import os
import subprocess
import time
from typing import Dict

from appium import webdriver
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


def get_capabilities(apk_path: str) -> Dict[str, str]:
    """Get Appium desired capabilities configuration.
    
    Args:
        apk_path: Full path to the APK file
        
    Returns:
        Dictionary of Appium desired capabilities
    """
    return {
        "platformName": "Android",
        "appium:platformVersion": PLATFORM_VERSION,
        "appium:deviceName": DEVICE_NAME,
        "appium:app": apk_path,
        "appium:automationName": "UiAutomator2",
        "appium:newCommandTimeout": 120,
        "appium:autoGrantPermissions": True,
        "appium:adbExecTimeout": 120000
    }


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
            logger.info(f"Successfully uninstalled {PACKAGE_NAME}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to uninstall {PACKAGE_NAME}: {e}")
    else:
        logger.debug(f"Clearing app data: {PACKAGE_NAME}")
        try:
            subprocess.run(['adb', 'shell', 'pm', 'clear', PACKAGE_NAME], check=True)
            logger.info(f"Successfully cleared data for {PACKAGE_NAME}")
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
    current_dir = os.getcwd()
    apk_path = os.path.join(current_dir, "apks", APK_NAME)
    logger.debug(f"APK path: {apk_path}")
    
    if not os.path.exists(apk_path):
        logger.error("APK not found in apks folder")
        raise FileNotFoundError(f"APK file not found: {apk_path}")
    
    verify_device_connection()
    manage_app_installation(reinstall_app)
    
    capabilities = get_capabilities(apk_path)
    appium_url = f"http://{APPIUM_HOST}:{APPIUM_PORT}"
    
    try:
        driver = webdriver.Remote(appium_url, capabilities)
        logger.info("Successfully created Appium driver")
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to create Appium driver: {e}")
        raise
    
    appium_url = f"http://{APPIUM_HOST}:{APPIUM_PORT}"
    logger.info(f"Connecting to Appium server at {appium_url}")
    
    start_time = time.time()
    while time.time() - start_time < 60:
        try:
            driver = WebDriver(
                command_executor=appium_url,
                desired_capabilities=capabilities
            )
            logger.info("WebDriver session started")
            return driver
        except Exception as e:
            logger.debug(f"Session creation retry ({time.time() - start_time:.1f}s): {str(e)}")
            time.sleep(5)
            
    package_name = "com.example.iris"  # Add the correct package name here
    try:
        if reinstall_app:
            logger.info("Reinstalling application...")
            driver.remove_app(package_name)
            driver.install_app(apk_path)
            logger.info("App reinstalled successfully")
        else:
            logger.info("Clearing application data...")
            try:
                driver.execute_script("mobile: shell", {
                    "command": f"pm clear {package_name}"
                })
            except Exception:
                logger.debug("Retrying clear after starting app...")
                driver.start_activity(package_name, ".MainActivity")
                driver.execute_script("mobile: shell", {
                    "command": f"pm clear {package_name}"
                })
                logger.info("App data cleared successfully")

        driver.start_activity(package_name, ".MainActivity")
        return driver
    except TimeoutError:
        logger.error("WebDriver session creation timed out")
        raise TimeoutError("Failed to create WebDriver session within 60s")
        
    except Exception as e:
        logger.error(f"App preparation failed: {str(e)}")
        raise
