# utils/__init__.py

"""
Utilities package for Tutorial Agent application.

This package contains various utility modules for the Tutorial Agent application,
including enhanced notifications, logging helpers, and other common functionality.
"""

import logging

# Package metadata
__version__ = "1.0.0"
__author__ = "Tutorial Agent Team"

# Setup package-level logger
logger = logging.getLogger(__name__)

# Import commonly used utilities for easy access
try:
    from .enhanced_notifications import (
        show_success, show_error, show_warning, show_info,
        clear_all_notifications, show_confirmation, NotificationContext
    )

    # Make notification functions available at package level
    __all__ = [
        'show_success', 'show_error', 'show_warning', 'show_info',
        'clear_all_notifications', 'show_confirmation', 'NotificationContext'
    ]

    logger.debug("Enhanced notifications module loaded successfully")

except ImportError as e:
    logger.warning(f"Could not import enhanced_notifications: {e}")
    # Provide fallback functions if the enhanced notifications fail
    __all__ = []


def get_version():
    """Get the package version."""
    return __version__


def setup_logging(level=logging.INFO):
    """Setup basic logging for the utils package."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


logger.info(f"Utils package v{__version__} initialized")