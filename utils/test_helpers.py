"""Helper functions for test automation."""

import subprocess
import time
import ast
import difflib
import os
from typing import List, Dict, Any

from utils.logger import logger
from test_settings import (
    DEVICE_NAME,
    AVD_NAME,
    EMULATOR_BOOT_TIMEOUT
)

class ScreenValidator:
    """Validate test files against screen class methods."""
    
    def __init__(self):
        self.validation_result = {"errors": None, "validated": False}
        
    def validate_all_test_files(self) -> None:
        """Validate all test files and screen classes for potential issues."""
        from screens import (
            dish_list_screen, 
            dish_detail_screen, 
            ingredient_selection_screen, 
            splash_screen
        )
        
        screens = {
            'DishListScreen': dish_list_screen.DishListScreen,
            'DishDetailScreen': dish_detail_screen.DishDetailScreen,
            'IngredientSelectionScreen': ingredient_selection_screen.IngredientSelectionScreen,
            'SplashScreen': splash_screen.SplashScreen
        }
        
        validation_errors = []
        test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests')
        
        def find_closest_method(wrong_method: str, available_methods: list) -> str:
            """Find the closest matching method name using string similarity."""
            if not available_methods:
                return ""
            closest = difflib.get_close_matches(wrong_method, available_methods, n=1, cutoff=0.6)
            return closest[0] if closest else ""
        
        for test_file in os.listdir(test_dir):
            if not test_file.endswith('.py'):
                continue
                
            file_path = os.path.join(test_dir, test_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                tree = ast.parse(content)
                var_to_screen = {}
                file_errors = []
                
                # First walk: collect variable assignments
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and isinstance(node.value, ast.Call):
                                if isinstance(node.value.func, ast.Name):
                                    screen_name = node.value.func.id
                                    if screen_name in screens:
                                        var_to_screen[target.id] = screen_name
                                        
                # Second walk: analyze method calls
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name):
                            var_name = node.func.value.id
                            method_name = node.func.attr
                            
                            if var_name in var_to_screen:
                                screen_name = var_to_screen[var_name]
                                screen_class = screens[screen_name]
                                
                                if not hasattr(screen_class, method_name):
                                    line_no = getattr(node, 'lineno', '?')
                                    col_offset = getattr(node, 'col_offset', 0)
                                    
                                    available_methods = [m for m in dir(screen_class) 
                                                      if not m.startswith('_')]
                                    closest_match = find_closest_method(method_name, available_methods)
                                    
                                    suggestion = f"\n   💡 Did you mean: {closest_match}?" if closest_match else ""
                                    
                                    error = {
                                        'file': test_file,
                                        'line': line_no,
                                        'column': col_offset,
                                        'screen': screen_name,
                                        'method': method_name,
                                        'suggestion': suggestion
                                    }
                                    file_errors.append(error)
                                    
                if file_errors:
                    validation_errors.append({
                        'file': test_file,
                        'errors': file_errors
                    })
                                    
            except Exception as e:
                validation_errors.append({
                    'file': test_file,
                    'errors': [{
                        'file': test_file,
                        'error': f"Failed to analyze file: {str(e)}"
                    }]
                })
                    
        self.validation_result["validated"] = True
        self.validation_result["errors"] = validation_errors
        
    def format_validation_errors(self) -> str:
        """Format validation errors into a readable message."""
        validation_errors = self.validation_result["errors"]
        if not validation_errors:
            return None
            
        error_msg = [
            "\n\033[1;31m═══════════════════════════════════════════\033[0m",
            "\033[1;31m❌ Test Validation Failed\033[0m",
            "\033[1;31m═══════════════════════════════════════════\033[0m"
        ]
        
        for file_error in validation_errors:
            file_name = file_error['file']
            error_msg.append(f"\n\033[1;36m📄 File: {file_name}\033[0m")
            
            for err in file_error['errors']:
                if 'error' in err:  # File analysis error
                    error_msg.append(f"  \033[1;33m⚠️  {err['error']}\033[0m")
                else:
                    line_info = f"\033[1;37mLine {err['line']}:\033[0m"
                    method_info = f"\033[1;31m{err['method']}\033[0m"
                    screen_info = f"\033[1;36m{err['screen']}\033[0m"
                    
                    error_msg.append(
                        f"  ❌ {line_info} Invalid method '{method_info}' "
                        f"called on {screen_info}"
                    )
                    
                    if err['suggestion']:
                        suggestion = err['suggestion'].replace(
                            "Did you mean: ", 
                            "\033[1;32mDid you mean: \033[1;37m"
                        ) + "\033[0m"
                        error_msg.append(f"     {suggestion}")
                    
        error_msg.append("\033[1;31m═══════════════════════════════════════════\033[0m\n")
        return '\n'.join(error_msg)

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
        
        logger.debug(f"Found {len(devices)} connected device(s)")
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
    if m > 0:
        return f"{m}m {s:.2f}s"
    return f"{s:.2f}s"
