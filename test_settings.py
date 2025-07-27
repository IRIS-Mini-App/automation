"""Test configuration settings for the IRIS mini app automation project."""

# Debug settings
DEBUG_MODE = False  # Set True to enable detailed logging

# App settings
PACKAGE_NAME = "com.example.hnag_ui"
IS_REINSTALL_APP = False  # True to reinstall app, False to only clear data
APK_NAME = "app-release-1.0.apk"

# Device settings
DEVICE_NAME = "emulator-5554"
PLATFORM_VERSION = "16.0"
AVD_NAME = "Pixel 9a API 36.0"

# Appium settings
APPIUM_HOST = "127.0.0.1"
APPIUM_PORT = 4723

# Timeouts (in seconds)
EMULATOR_BOOT_TIMEOUT = 60  # Time to wait for emulator boot
APPIUM_SERVER_TIMEOUT = 30  # Time to wait for Appium server
