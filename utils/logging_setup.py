"""
Comprehensive logging setup for Tutorial Agent

This module provides centralized logging configuration with support for
file and console output, log rotation, and different log levels.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Union
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output."""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        
        return super().format(record)


def setup_logging(
    log_file: Optional[Union[str, Path]] = None,
    level: int = logging.INFO,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    console_output: bool = True,
    colored_console: bool = True,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up comprehensive logging configuration.
    
    Args:
        log_file: Path to log file (optional)
        level: Logging level (default: INFO)
        max_file_size: Maximum size for log files before rotation
        backup_count: Number of backup files to keep
        console_output: Whether to output to console
        colored_console: Whether to use colored output in console
        format_string: Custom format string
    
    Returns:
        Configured root logger
    """
    
    # Default format string
    if format_string is None:
        format_string = (
            '%(asctime)s | %(name)-20s | %(levelname)-8s | '
            '%(filename)s:%(lineno)d | %(message)s'
        )
    
    # Get root logger and clear existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(level)
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        if colored_console and sys.stdout.isatty():
            console_formatter = ColoredFormatter(format_string)
        else:
            console_formatter = logging.Formatter(format_string)
        
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        
        # File formatter (no colors)
        file_formatter = logging.Formatter(format_string)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Set up specific logger levels
    logging.getLogger('TutorialAgent').setLevel(level)
    logging.getLogger('PyQt6').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    # Log the setup
    logger = logging.getLogger('TutorialAgent.LoggingSetup')
    logger.info(f"Logging setup complete - Level: {logging.getLevelName(level)}")
    
    if log_file:
        logger.info(f"Log file: {log_file}")
    
    return root_logger


def configure_logger(
    name: str,
    level: Optional[int] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Configure a specific named logger.
    
    Args:
        name: Logger name
        level: Logging level (optional)
        format_string: Custom format string (optional)
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    if level is not None:
        logger.setLevel(level)
    
    if format_string is not None and logger.handlers:
        formatter = logging.Formatter(format_string)
        for handler in logger.handlers:
            handler.setFormatter(formatter)
    
    return logger


def log_system_info():
    """Log system information for debugging purposes."""
    logger = logging.getLogger('TutorialAgent.SystemInfo')
    
    import platform
    import sys
    
    logger.info("System Information:")
    logger.info(f"  Platform: {platform.platform()}")
    logger.info(f"  Python: {sys.version}")
    logger.info(f"  Architecture: {platform.architecture()}")
    logger.info(f"  Processor: {platform.processor()}")
    
    try:
        import PyQt6.QtCore
        logger.info(f"  PyQt6 Version: {PyQt6.QtCore.QT_VERSION_STR}")
    except ImportError:
        logger.warning("  PyQt6: Not available")


def create_performance_logger() -> logging.Logger:
    """Create a dedicated logger for performance monitoring."""
    perf_logger = logging.getLogger('TutorialAgent.Performance')
    
    # Create a separate handler for performance logs
    perf_handler = logging.StreamHandler()
    perf_handler.setLevel(logging.DEBUG)
    
    # Simple format for performance logs
    perf_formatter = logging.Formatter(
        '%(asctime)s | PERF | %(message)s'
    )
    perf_handler.setFormatter(perf_formatter)
    
    perf_logger.addHandler(perf_handler)
    perf_logger.setLevel(logging.DEBUG)
    perf_logger.propagate = False  # Don't propagate to root logger
    
    return perf_logger


class ContextFilter(logging.Filter):
    """Add context information to log records."""
    
    def __init__(self, context_data: dict):
        super().__init__()
        self.context_data = context_data
    
    def filter(self, record):
        for key, value in self.context_data.items():
            setattr(record, key, value)
        return True


def add_context_to_logger(logger_name: str, context: dict):
    """Add context information to a specific logger."""
    logger = logging.getLogger(logger_name)
    context_filter = ContextFilter(context)
    logger.addFilter(context_filter)


# Example usage and testing
def test_logging():
    """Test the logging setup."""
    # Setup logging
    setup_logging(
        log_file='test_tutorial_agent.log',
        level=logging.DEBUG,
        colored_console=True
    )
    
    # Test different log levels
    logger = logging.getLogger('TutorialAgent.Test')
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Test performance logger
    perf_logger = create_performance_logger()
    perf_logger.info("Performance test message")
    
    # Log system info
    log_system_info()


if __name__ == '__main__':
    test_logging()