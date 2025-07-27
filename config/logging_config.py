"""Logging configuration for the test automation framework."""

import logging
from typing import Dict, Final

from test_settings import DEBUG_MODE


class LogConfig:
    """Centralized logging configuration."""
    
    # Standard environment log levels (when DEBUG_MODE is False)
    CONSOLE_LOG_LEVEL: Final[int] = logging.INFO
    FILE_LOG_LEVEL: Final[int] = logging.INFO
    
    # Debug environment log levels (when DEBUG_MODE is True)
    DEBUG_CONSOLE_LEVEL: Final[int] = logging.DEBUG
    DEBUG_FILE_LEVEL: Final[int] = logging.DEBUG
    
    # Log format configuration
    LOG_FORMAT: Final[str] = '%(asctime)s - %(levelname)s - [%(module)s] - %(message)s'
    DATE_FORMAT: Final[str] = '%Y-%m-%d %H:%M:%S'
    
    # Log file configuration
    LOG_FILE_PREFIX: Final[str] = 'test_execution'
    LOG_DIRECTORY: Final[str] = 'logs'
    
    # Log level mapping
    LOG_LEVELS: Final[Dict[str, int]] = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    @classmethod
    def get_log_level(cls, level_name: str) -> int:
        """Convert log level name to logging level number.
        
        Args:
            level_name: The name of the log level (e.g., 'DEBUG', 'INFO')
            
        Returns:
            The corresponding logging level number, defaults to INFO if invalid
        """
        return cls.LOG_LEVELS.get(level_name.upper(), logging.INFO)
