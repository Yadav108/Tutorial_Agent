import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class Settings:
    """
    Application settings management class.
    Handles loading, saving, and accessing application settings.
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize settings

        Args:
            config_file: Optional path to custom config file
        """
        # Set default values
        self._set_defaults()

        # Load configuration
        self.config_file = config_file or self._get_default_config_path()
        self.load()

    def _set_defaults(self):
        """Set default settings values"""
        # Paths
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.CONTENT_DIR = self.BASE_DIR / 'content'
        self.DATA_DIR = self.BASE_DIR / 'data'
        self.CACHE_DIR = self.BASE_DIR / 'cache'
        self.LOG_DIR = self.BASE_DIR / 'logs'

        # Database
        self.DATABASE_URL = 'sqlite:///tutorial_agent.db'

        # Application
        self.DEFAULT_LANGUAGE = 'python'
        self.CONTENT_FONT_SIZE = 12
        self.CODE_FONT_SIZE = 14
        self.DARK_MODE = False
        self.AUTO_SAVE = True
        self.SAVE_INTERVAL = 300  # 5 minutes

        # Editor
        self.CODE_COMPLETION = True
        self.LINE_NUMBERS = True
        self.SYNTAX_HIGHLIGHTING = True
        self.TAB_SIZE = 4
        self.AUTO_INDENT = True

        # Performance
        self.CACHE_SIZE = 100  # MB
        self.MAX_RECENT_FILES = 10

    def _get_default_config_path(self) -> Path:
        """
        Get default configuration file path

        Returns:
            Path to default config file
        """
        return self.BASE_DIR / 'config' / 'settings.yml'

    def load(self):
        """Load settings from configuration file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = yaml.safe_load(f)

                if config_data:
                    self._update_from_dict(config_data)
                    logger.info("Settings loaded successfully")
            else:
                logger.warning(f"Config file not found: {self.config_file}")
                self.save()  # Create default config file

        except Exception as e:
            logger.error(f"Failed to load settings: {str(e)}")

    def save(self):
        """Save current settings to configuration file"""
        try:
            # Create config directory if it doesn't exist
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            # Convert settings to dictionary
            config_data = self._to_dict()

            # Save to file
            with open(self.config_file, 'w') as f:
                yaml.safe_dump(config_data, f, default_flow_style=False)

            logger.info("Settings saved successfully")

        except Exception as e:
            logger.error(f"Failed to save settings: {str(e)}")

    def _update_from_dict(self, data: Dict[str, Any]):
        """
        Update settings from dictionary

        Args:
            data: Dictionary containing settings values
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def _to_dict(self) -> Dict[str, Any]:
        """
        Convert settings to dictionary

        Returns:
            Dictionary containing all settings
        """
        return {
            key: value for key, value in vars(self).items()
            if not key.startswith('_') and key.isupper()
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get setting value

        Args:
            key: Setting key
            default: Default value if setting not found

        Returns:
            Setting value or default
        """
        return getattr(self, key, default)

    def set(self, key: str, value: Any):
        """
        Set setting value

        Args:
            key: Setting key
            value: New value
        """
        setattr(self, key, value)

    def reset(self):
        """Reset all settings to defaults"""
        self._set_defaults()
        self.save()