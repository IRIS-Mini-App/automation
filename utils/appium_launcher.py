"""Utility module for managing Appium server lifecycle."""

import os
import shutil
import signal
import subprocess
import threading
import time
from typing import Optional

import requests

from test_settings import (
    APPIUM_HOST,
    APPIUM_PORT,
    APPIUM_SERVER_TIMEOUT
)
from utils.logger import logger


class AppiumServer:
    """Class for managing Appium server lifecycle."""
    
    def __init__(self):
        """Initialize AppiumServer instance."""
        self.process: Optional[subprocess.Popen] = None
        
    def get_process(self) -> Optional[subprocess.Popen]:
        """Get current Appium process."""
        return self.process
        
    def set_process(self, process: Optional[subprocess.Popen]) -> None:
        """Set current Appium process."""
        self.process = process


# Global instance of AppiumServer
appium_server = AppiumServer()


def kill_existing_appium() -> None:
    """Kill any existing Appium processes.
    
    Attempts to terminate any running Appium server processes to avoid port conflicts.
    """
    try:
        subprocess.run(
            ['taskkill', '/F', '/IM', 'node.exe'], 
            capture_output=True,
            check=False
        )
        logger.debug("Successfully killed existing Appium processes")
    except subprocess.SubprocessError as e:
        logger.warning(f"Failed to kill existing Appium process: {e}")


def get_appium_command() -> str:
    """Locate the Appium executable.
    
    Returns:
        str: Path to Appium executable
        
    Raises:
        Exception: If Appium is not installed
    """
    appium_cmd = shutil.which("appium")
    if appium_cmd:
        logger.debug(f"Found Appium in PATH: {appium_cmd}")
        return appium_cmd
        
    fallback = os.path.expanduser("~\\AppData\\Roaming\\npm\\appium.cmd")
    if os.path.exists(fallback):
        logger.debug(f"Found Appium in npm directory: {fallback}")
        return fallback
        
    error_msg = "Appium not found. Please install it globally via: npm install -g appium"
    logger.error(error_msg)
    raise Exception(error_msg)


def wait_for_appium_ready() -> bool:
    """Wait for Appium server to be ready to accept connections.
    
    Returns:
        bool: True if server is ready, False if timeout occurred
    """
    url = f"http://{APPIUM_HOST}:{APPIUM_PORT}/status"
    logger.info(f"Waiting for Appium server at {url}")
    
    start_time = time.time()
    while time.time() - start_time < APPIUM_SERVER_TIMEOUT:
        try:
            elapsed = time.time() - start_time
            logger.debug(f"Attempting connection (Elapsed: {elapsed:.1f}s)")
            
            resp = requests.get(url, timeout=1)
            if resp.status_code == 200 and resp.json()["value"]["ready"]:
                logger.info("Appium server is ready")
                return True
                
            logger.debug(f"Server not ready. Status: {resp.status_code}")
            
        except requests.RequestException as e:
            logger.debug(f"Connection failed: {str(e)}")
            
        time.sleep(0.5)
        
    logger.error(f"Server startup timeout after {APPIUM_SERVER_TIMEOUT}s")
    return False

def start_appium() -> None:
    """Start and configure the Appium server.
    
    Raises:
        Exception: If server fails to start or respond
    """
    logger.info("Starting Appium server...")
    
    # Kill any existing Appium process
    kill_existing_appium()
    logger.debug("Cleaned up existing Appium processes")
    
    if appium_server.get_process():
        logger.debug("Stopping existing Appium server...")
        stop_appium()
    
    try:
        appium_cmd = get_appium_command()
        logger.debug(f"Using Appium path: {appium_cmd}")
        
        shell = appium_cmd.endswith(".cmd") or appium_cmd.endswith(".bat")
        launch_cmd = (f'"{appium_cmd}" --allow-insecure=adb_shell --log-timestamp --debug' 
                     if shell else 
                     [appium_cmd, "--allow-insecure=adb_shell", "--log-timestamp", "--debug"])
        logger.debug(f"Launch command: {launch_cmd}")
        
        logger.debug("Creating Appium process...")
        process = subprocess.Popen(
            launch_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
            universal_newlines=True,  
            bufsize=1  
        )
        appium_server.set_process(process)
        
        if process and process.pid:
            logger.debug(f"Appium process created with PID: {process.pid}")
        
        logger.debug("Waiting for Appium process to stabilize...")
        
        def log_output() -> None:
            """Log Appium server output in background thread."""
            while process and process.stdout:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    logger.debug(f"[APPIUM] {line.strip()}")
        
        output_thread = threading.Thread(target=log_output, daemon=True)
        output_thread.start()
        
        time.sleep(5)  # Allow process to stabilize
        
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            logger.error(f"Appium STDOUT: {stdout.decode(errors='ignore')}")
            logger.error(f"Appium STDERR: {stderr.decode(errors='ignore')}")
            raise Exception("Appium crashed immediately after starting")

        if wait_for_appium_ready():
            logger.debug("✅ Appium server is up and running!")
            try:
                resp = requests.get(f"http://{APPIUM_HOST}:{APPIUM_PORT}/status", timeout=3)
                logger.debug(f"Raw status response: {resp.text}")
                version = resp.json()['value']['build']['version']
                logger.debug(f"Appium version: {version}")
            except Exception as e:
                logger.warning(f"Couldn't fetch Appium version: {e}")
        else:
            raise Exception("Appium server did not respond in time")
            
    except Exception as e:
        logger.error(f"Failed to start Appium: {str(e)}")
        if appium_server.get_process():
            appium_server.get_process().kill()
        raise

def stop_appium() -> None:
    """Stop the running Appium server gracefully."""
    process = appium_server.get_process()
    if process:
        logger.info("Stopping Appium server...")
        os.kill(process.pid, signal.SIGTERM)
        appium_server.set_process(None)
        logger.info("Appium server stopped")
