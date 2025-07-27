"""Centralized logging configuration for the automation framework."""

import logging
import os
from datetime import datetime
from typing import Optional, ClassVar

from config.logging_config import LogConfig
from test_settings import DEBUG_MODE


class Logger:
    """Singleton logger class providing centralized logging functionality."""
    
    _instance: ClassVar[Optional['Logger']] = None
    _logger: ClassVar[Optional[logging.Logger]] = None

    def __new__(cls) -> 'Logger':
        """Create or return the singleton logger instance.
        
        Returns:
            Logger: The singleton logger instance
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._setup_logger(debug_mode=DEBUG_MODE)
        return cls._instance

    @classmethod
    def _setup_logger(cls, debug_mode: bool = False) -> None:
        """Configure the logger with file and console handlers.
        
        Args:
            debug_mode: If True, shows all log levels. If False, shows only important logs
        """
        if cls._logger is not None:
            return
            
        # Initialize logger
        cls._logger = logging.getLogger('AppiumAutomation')
        cls._logger.setLevel(logging.DEBUG)
        
        # Set log levels based on mode
        console_level = (LogConfig.DEBUG_CONSOLE_LEVEL 
                        if debug_mode else LogConfig.CONSOLE_LOG_LEVEL)
        file_level = (LogConfig.DEBUG_FILE_LEVEL 
                     if debug_mode else LogConfig.FILE_LOG_LEVEL)
        
        # Set up log directory
        logs_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            LogConfig.LOG_DIRECTORY
        )
        os.makedirs(logs_dir, exist_ok=True)
        
        # Configure file handler
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        mode_suffix = '_debug' if debug_mode else ''
        log_file = os.path.join(
            logs_dir, 
            f'{LogConfig.LOG_FILE_PREFIX}{mode_suffix}_{timestamp}.log'
        )
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(file_level)
        
        # Configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        
        # Set up formatter
        formatter = logging.Formatter(
            LogConfig.LOG_FORMAT,
            LogConfig.DATE_FORMAT
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        cls._logger.addHandler(file_handler)
        cls._logger.addHandler(console_handler)

    @classmethod
    def debug(cls, message):
        """Log debug message"""
        if cls._logger is None:
            cls._setup_logger()
        cls._logger.debug(message)

    @classmethod
    def info(cls, message):
        """Log info message"""
        if cls._logger is None:
            cls._setup_logger()
        cls._logger.info(message)

    @classmethod
    def warning(cls, message):
        """Log warning message"""
        if cls._logger is None:
            cls._setup_logger()
        cls._logger.warning(message)

    @classmethod
    def error(cls, message):
        """Log error message"""
        if cls._logger is None:
            cls._setup_logger()
        cls._logger.error(message)

# Create global logger instance
logger = Logger()
