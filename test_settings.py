"""Test configuration settings for the IRIS mini app automation project."""

from typing import Final

# Debug settings
DEBUG_MODE: Final[bool] = False  # Set True to enable detailed logging

# App settings
PACKAGE_NAME: Final[str] = "com.example.hnag_ui"
IS_REINSTALL_APP: Final[bool] = False  # True to reinstall app, False to only clear data
APK_NAME: Final[str] = "app-release-1.0.apk"

# Device settings
DEVICE_NAME: Final[str] = "emulator-5554"
PLATFORM_VERSION: Final[str] = "16.0"
AVD_NAME: Final[str] = "Pixel 9a API 36.0"

# Appium settings
APPIUM_HOST: Final[str] = "127.0.0.1"
APPIUM_PORT: Final[int] = 4723

# Timeouts (in seconds)
EMULATOR_BOOT_TIMEOUT: Final[int] = 60  # Time to wait for emulator boot
APPIUM_SERVER_TIMEOUT: Final[int] = 30  # Time to wait for Appium server
