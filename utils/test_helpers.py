"""Utility functions for test automation."""

import subprocess
import time

from utils.logger import logger
from test_settings import (
    DEVICE_NAME,
    AVD_NAME,
    EMULATOR_BOOT_TIMEOUT
)

def check_emulator() -> bool:
    """Ensure Android emulator is running.
    
    Returns:
        bool: True if emulator is running successfully
        
    Raises:
        Exception: If emulator fails to start within timeout
    """
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    if DEVICE_NAME not in result.stdout:
        logger.debug(f"Starting emulator {AVD_NAME}...")
        subprocess.Popen(['emulator', '-avd', AVD_NAME, '-no-snapshot-load'])
        
        start_time = time.time()
        while time.time() - start_time < EMULATOR_BOOT_TIMEOUT:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            if DEVICE_NAME in result.stdout:
                logger.debug("Emulator is ready")
                time.sleep(5)  # Wait for full boot
                return True
            time.sleep(2)
        raise Exception(f"Timeout waiting for emulator {AVD_NAME} to start after {EMULATOR_BOOT_TIMEOUT}s")
    
    logger.debug(f"Emulator {DEVICE_NAME} is already running")
    return True

def format_duration(seconds: float) -> str:
    """Format duration in seconds to a human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "1h 2m 3.45s")
    """
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    
    if h > 0:
        return f"{h}h {m}m {s:.2f}s"
    elif m > 0:
        return f"{m}m {s:.2f}s"
    return f"{s:.2f}s"
