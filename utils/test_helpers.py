"""Helper functions for test automation."""

import subprocess
import time
from typing import Union, List

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
        ConnectionError: If ADB server is not responding
        TimeoutError: If emulator fails to start within timeout
    """
    try:
        result = subprocess.run(
            ['adb', 'devices'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        devices = [
            line.strip() for line in result.stdout.splitlines()[1:]
            if line.strip()
        ]
        
        if DEVICE_NAME not in result.stdout:
            logger.debug(f"Starting emulator {AVD_NAME}...")
            with subprocess.Popen(['emulator', '-avd', AVD_NAME, '-no-snapshot-load']):
                start_time = time.time()
                while time.time() - start_time < EMULATOR_BOOT_TIMEOUT:
                    result = subprocess.run(
                        ['adb', 'devices'],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    if DEVICE_NAME in result.stdout:
                        logger.debug("Emulator is ready")
                        time.sleep(5)  # Wait for full boot
                        return True
                    time.sleep(2)
                raise TimeoutError(
                    f"Timeout waiting for emulator {AVD_NAME} "
                    f"to start after {EMULATOR_BOOT_TIMEOUT}s"
                )
        
        logger.info(f"Found {len(devices)} connected device(s)")
        for device in devices:
            logger.debug(f"Device: {device}")
        return True
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to check emulator status: {e}")
        raise ConnectionError("ADB server is not responding")

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
