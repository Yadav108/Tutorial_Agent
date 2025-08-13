# config/settings_manager.py

import logging
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import threading
from functools import wraps

logger = logging.getLogger('TutorialAgent.Settings')


class ThemeMode(Enum):
    """Theme mode options."""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"  # System preference


class LanguagePreference(Enum):
    """UI language preferences."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    JAPANESE = "ja"


class CodeEditorTheme(Enum):
    """Code editor theme options."""
    VS_CODE_DARK = "vscode_dark"
    VS_CODE_LIGHT = "vscode_light"
    MONOKAI = "monokai"
    GITHUB = "github"
    DRACULA = "dracula"
    MATERIAL = "material"


@dataclass
class EditorSettings:
    """Code editor specific settings."""
    font_family: str = "Consolas"
    font_size: int = 12
    theme: CodeEditorTheme = CodeEditorTheme.VS_CODE_DARK
    show_line_numbers: bool = True
    word_wrap: bool = False
    tab_size: int = 4
    auto_indent: bool = True
    highlight_current_line: bool = True
    show_whitespace: bool = False
    auto_save_interval: int = 30  # seconds
    enable_auto_complete: bool = True
    enable_syntax_highlighting: bool = True
    enable_code_folding: bool = True

    def validate(self):
        """Validate editor settings."""
        if self.font_size < 8 or self.font_size > 32:
            raise ValueError("Font size must be between 8 and 32")

        if self.tab_size < 1 or self.tab_size > 8:
            raise ValueError("Tab size must be between 1 and 8")

        if self.auto_save_interval < 5 or self.auto_save_interval > 300:
            raise ValueError("Auto-save interval must be between 5 and 300 seconds")


@dataclass
class UISettings:
    """User interface settings."""
    theme: ThemeMode = ThemeMode.LIGHT
    language: LanguagePreference = LanguagePreference.ENGLISH
    window_maximized: bool = False
    window_width: int = 1400
    window_height: int = 900
    window_x: int = 100
    window_y: int = 100
    sidebar_width: int = 350
    content_splitter_ratio: float = 0.7  # Content viewer vs code editor
    show_welcome_screen: bool = True
    animation_enabled: bool = True
    notification_enabled: bool = True
    notification_duration: int = 3000  # milliseconds
    auto_hide_sidebar: bool = False
    compact_mode: bool = False

    def validate(self):
        """Validate UI settings."""
        if self.window_width < 800 or self.window_width > 3840:
            raise ValueError("Window width must be between 800 and 3840")

        if self.window_height < 600 or self.window_height > 2160:
            raise ValueError("Window height must be between 600 and 2160")

        if self.sidebar_width < 200 or self.sidebar_width > 500:
            raise ValueError("Sidebar width must be between 200 and 500")

        if not 0.3 <= self.content_splitter_ratio <= 0.9:
            raise ValueError("Content splitter ratio must be between 0.3 and 0.9")

        if self.notification_duration < 1000 or self.notification_duration > 10000:
            raise ValueError("Notification duration must be between 1000 and 10000 ms")


@dataclass
class LearningSettings:
    """Learning and progress tracking settings."""
    auto_save_progress: bool = True
    show_progress_notifications: bool = True
    enable_achievements: bool = True
    difficulty_preference: str = "adaptive"  # adaptive, beginner, advanced
    preferred_languages: List[str] = field(default_factory=list)
    show_hints: bool = True
    auto_advance_topics: bool = False
    practice_reminders: bool = True
    daily_goal_minutes: int = 30
    weekly_goal_hours: int = 5
    streak_tracking: bool = True

    def validate(self):
        """Validate learning settings."""
        valid_difficulties = ["adaptive", "beginner", "intermediate", "advanced"]
        if self.difficulty_preference not in valid_difficulties:
            raise ValueError(f"Difficulty preference must be one of: {valid_difficulties}")

        if self.daily_goal_minutes < 10 or self.daily_goal_minutes > 480:
            raise ValueError("Daily goal must be between 10 and 480 minutes")

        if self.weekly_goal_hours < 1 or self.weekly_goal_hours > 40:
            raise ValueError("Weekly goal must be between 1 and 40 hours")


@dataclass
class PerformanceSettings:
    """Performance and optimization settings."""
    enable_caching: bool = True
    cache_size_mb: int = 100
    parallel_loading: bool = True
    lazy_loading: bool = True
    preload_next_topic: bool = True
    max_concurrent_operations: int = 4
    enable_performance_monitoring: bool = False
    log_slow_operations: bool = True
    slow_operation_threshold_ms: int = 1000
    memory_cleanup_interval: int = 300  # seconds

    def validate(self):
        """Validate performance settings."""
        if self.cache_size_mb < 10 or self.cache_size_mb > 1000:
            raise ValueError("Cache size must be between 10 and 1000 MB")

        if self.max_concurrent_operations < 1 or self.max_concurrent_operations > 16:
            raise ValueError("Max concurrent operations must be between 1 and 16")

        if self.slow_operation_threshold_ms < 100 or self.slow_operation_threshold_ms > 10000:
            raise ValueError("Slow operation threshold must be between 100 and 10000 ms")


@dataclass
class SecuritySettings:
    """Security and privacy settings."""
    enable_code_validation: bool = True
    allow_network_access: bool = False
    enable_analytics: bool = True
    share_usage_data: bool = False
    auto_backup: bool = True
    backup_interval_hours: int = 24
    max_backup_files: int = 5
    encrypt_user_data: bool = False

    def validate(self):
        """Validate security settings."""
        if self.backup_interval_hours < 1 or self.backup_interval_hours > 168:
            raise ValueError("Backup interval must be between 1 and 168 hours")

        if self.max_backup_files < 1 or self.max_backup_files > 20:
            raise ValueError("Max backup files must be between 1 and 20")


@dataclass
class ApplicationSettings:
    """Main application settings container."""
    editor: EditorSettings = field(default_factory=EditorSettings)
    ui: UISettings = field(default_factory=UISettings)
    learning: LearningSettings = field(default_factory=LearningSettings)
    performance: PerformanceSettings = field(default_factory=PerformanceSettings)
    security: SecuritySettings = field(default_factory=SecuritySettings)

    # Metadata
    version: str = "1.0.0"
    last_updated: str = ""
    custom_settings: Dict[str, Any] = field(default_factory=dict)

    def validate(self):
        """Validate all settings."""
        self.editor.validate()
        self.ui.validate()
        self.learning.validate()
        self.performance.validate()
        self.security.validate()


class SettingsManager:
    """Comprehensive settings management with validation and persistence."""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".tutorial_agent"
        self.config_file = self.config_dir / "settings.json"
        self.backup_file = self.config_dir / "settings_backup.json"

        # Settings instance
        self._settings: Optional[ApplicationSettings] = None

        # Thread safety
        self._lock = threading.RLock()

        # Change callbacks
        self._change_callbacks: Dict[str, List[Callable]] = {}

        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Load settings
        self.load()

        logger.info(f"Settings manager initialized with config: {self.config_file}")

    @property
    def settings(self) -> ApplicationSettings:
        """Get current settings instance."""
        if self._settings is None:
            self._settings = ApplicationSettings()
        return self._settings

    def load(self) -> bool:
        """Load settings from file."""
        try:
            with self._lock:
                if self.config_file.exists():
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Convert data to settings object
                    self._settings = self._dict_to_settings(data)
                    self._settings.validate()

                    logger.info("Settings loaded successfully")
                    return True
                else:
                    # Create default settings
                    self._settings = ApplicationSettings()
                    self.save()
                    logger.info("Created default settings")
                    return True

        except Exception as e:
            logger.error(f"Error loading settings: {e}")

            # Try to load backup
            if self._load_backup():
                return True

            # Fall back to defaults
            self._settings = ApplicationSettings()
            logger.warning("Using default settings due to load error")
            return False

    def _load_backup(self) -> bool:
        """Load settings from backup file."""
        try:
            if self.backup_file.exists():
                with open(self.backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self._settings = self._dict_to_settings(data)
                self._settings.validate()

                logger.info("Settings loaded from backup")
                return True
        except Exception as e:
            logger.error(f"Error loading backup settings: {e}")

        return False

    def save(self) -> bool:
        """Save settings to file."""
        try:
            with self._lock:
                # Create backup of current settings
                if self.config_file.exists():
                    import shutil
                    shutil.copy2(self.config_file, self.backup_file)

                # Save current settings
                data = self._settings_to_dict(self.settings)

                # Write to temporary file first
                temp_file = self.config_file.with_suffix('.tmp')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                # Atomic move
                temp_file.replace(self.config_file)

                logger.debug("Settings saved successfully")
                return True

        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False

    def _dict_to_settings(self, data: Dict[str, Any]) -> ApplicationSettings:
        """Convert dictionary to settings object."""
        # Handle enum conversions
        if 'editor' in data and 'theme' in data['editor']:
            data['editor']['theme'] = CodeEditorTheme(data['editor']['theme'])

        if 'ui' in data:
            if 'theme' in data['ui']:
                data['ui']['theme'] = ThemeMode(data['ui']['theme'])
            if 'language' in data['ui']:
                data['ui']['language'] = LanguagePreference(data['ui']['language'])

        # Create settings objects
        settings = ApplicationSettings()

        if 'editor' in data:
            settings.editor = EditorSettings(**data['editor'])

        if 'ui' in data:
            settings.ui = UISettings(**data['ui'])

        if 'learning' in data:
            settings.learning = LearningSettings(**data['learning'])

        if 'performance' in data:
            settings.performance = PerformanceSettings(**data['performance'])

        if 'security' in data:
            settings.security = SecuritySettings(**data['security'])

        # Copy metadata
        settings.version = data.get('version', '1.0.0')
        settings.last_updated = data.get('last_updated', '')
        settings.custom_settings = data.get('custom_settings', {})

        return settings

    def _settings_to_dict(self, settings: ApplicationSettings) -> Dict[str, Any]:
        """Convert settings object to dictionary."""
        data = asdict(settings)

        # Convert enums to values
        if 'editor' in data and 'theme' in data['editor']:
            data['editor']['theme'] = data['editor']['theme'].value

        if 'ui' in data:
            if 'theme' in data['ui']:
                data['ui']['theme'] = data['ui']['theme'].value
            if 'language' in data['ui']:
                data['ui']['language'] = data['ui']['language'].value

        # Add timestamp
        from datetime import datetime
        data['last_updated'] = datetime.now().isoformat()

        return data

    def get(self, setting_path: str, default: Any = None) -> Any:
        """Get a specific setting by dot notation path."""
        try:
            parts = setting_path.split('.')
            value = self.settings

            for part in parts:
                value = getattr(value, part)

            return value

        except (AttributeError, KeyError):
            return default

    def set(self, setting_path: str, value: Any) -> bool:
        """Set a specific setting by dot notation path."""
        try:
            with self._lock:
                parts = setting_path.split('.')
                target = self.settings

                # Navigate to the parent object
                for part in parts[:-1]:
                    target = getattr(target, part)

                # Set the value
                setattr(target, parts[-1], value)

                # Validate
                self.settings.validate()

                # Save
                success = self.save()

                if success:
                    # Notify callbacks
                    self._notify_callbacks(setting_path, value)

                return success

        except Exception as e:
            logger.error(f"Error setting {setting_path} = {value}: {e}")
            return False

    def register_callback(self, setting_path: str, callback: Callable[[Any], None]):
        """Register a callback for setting changes."""
        if setting_path not in self._change_callbacks:
            self._change_callbacks[setting_path] = []

        self._change_callbacks[setting_path].append(callback)

    def unregister_callback(self, setting_path: str, callback: Callable[[Any], None]):
        """Unregister a callback for setting changes."""
        if setting_path in self._change_callbacks:
            try:
                self._change_callbacks[setting_path].remove(callback)
            except ValueError:
                pass

    def _notify_callbacks(self, setting_path: str, value: Any):
        """Notify callbacks of setting changes."""
        # Exact path callbacks
        if setting_path in self._change_callbacks:
            for callback in self._change_callbacks[setting_path]:
                try:
                    callback(value)
                except Exception as e:
                    logger.error(f"Error in settings callback: {e}")

        # Wildcard callbacks (e.g., "ui.*")
        parts = setting_path.split('.')
        for i in range(len(parts)):
            wildcard_path = '.'.join(parts[:i + 1]) + '.*'
            if wildcard_path in self._change_callbacks:
                for callback in self._change_callbacks[wildcard_path]:
                    try:
                        callback(value)
                    except Exception as e:
                        logger.error(f"Error in settings wildcard callback: {e}")

    def reset_to_defaults(self, section: Optional[str] = None) -> bool:
        """Reset settings to defaults."""
        try:
            with self._lock:
                if section is None:
                    # Reset all settings
                    self._settings = ApplicationSettings()
                else:
                    # Reset specific section
                    if section == 'editor':
                        self._settings.editor = EditorSettings()
                    elif section == 'ui':
                        self._settings.ui = UISettings()
                    elif section == 'learning':
                        self._settings.learning = LearningSettings()
                    elif section == 'performance':
                        self._settings.performance = PerformanceSettings()
                    elif section == 'security':
                        self._settings.security = SecuritySettings()
                    else:
                        raise ValueError(f"Unknown settings section: {section}")

                return self.save()

        except Exception as e:
            logger.error(f"Error resetting settings: {e}")
            return False

    def export_settings(self, file_path: Path) -> bool:
        """Export settings to a file."""
        try:
            data = self._settings_to_dict(self.settings)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"Settings exported to {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting settings: {e}")
            return False

    def import_settings(self, file_path: Path) -> bool:
        """Import settings from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate by creating settings object
            imported_settings = self._dict_to_settings(data)
            imported_settings.validate()

            # If validation passes, update current settings
            with self._lock:
                self._settings = imported_settings
                success = self.save()

            if success:
                logger.info(f"Settings imported from {file_path}")

            return success

        except Exception as e:
            logger.error(f"Error importing settings: {e}")
            return False

    def get_settings_summary(self) -> Dict[str, Any]:
        """Get a summary of current settings."""
        return {
            'editor': {
                'font_family': self.settings.editor.font_family,
                'font_size': self.settings.editor.font_size,
                'theme': self.settings.editor.theme.value
            },
            'ui': {
                'theme': self.settings.ui.theme.value,
                'language': self.settings.ui.language.value,
                'animations': self.settings.ui.animation_enabled
            },
            'learning': {
                'auto_save': self.settings.learning.auto_save_progress,
                'daily_goal': self.settings.learning.daily_goal_minutes,
                'preferred_languages': self.settings.learning.preferred_languages
            },
            'performance': {
                'caching': self.settings.performance.enable_caching,
                'cache_size': self.settings.performance.cache_size_mb,
                'parallel_loading': self.settings.performance.parallel_loading
            }
        }


# Global settings manager instance
_settings_manager: Optional[SettingsManager] = None


def get_settings_manager() -> SettingsManager:
    """Get the global settings manager instance."""
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager


def get_setting(path: str, default: Any = None) -> Any:
    """Convenience function to get a setting."""
    return get_settings_manager().get(path, default)


def set_setting(path: str, value: Any) -> bool:
    """Convenience function to set a setting."""
    return get_settings_manager().set(path, value)


# Decorator for functions that should react to setting changes
def settings_dependent(setting_path: str):
    """Decorator to automatically call function when setting changes."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Register callback to re-run function when setting changes
            def setting_changed(value):
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in settings-dependent function {func.__name__}: {e}")

            get_settings_manager().register_callback(setting_path, setting_changed)

            return result

        return wrapper

    return decorator