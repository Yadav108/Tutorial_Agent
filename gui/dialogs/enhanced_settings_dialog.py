# gui/dialogs/enhanced_settings_dialog.py

import logging
from typing import Dict, Any, Optional, List, Callable
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QSpinBox, QCheckBox, QComboBox,
    QPushButton, QGroupBox, QSlider, QTextEdit, QColorDialog,
    QFontDialog, QFileDialog, QMessageBox, QProgressBar,
    QScrollArea, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QIcon, QPalette

from config.settings_manager import (
    SettingsManager, ApplicationSettings, ThemeMode,
    LanguagePreference, CodeEditorTheme, get_settings_manager
)

logger = logging.getLogger('TutorialAgent.SettingsDialog')


class SettingsGroup(QGroupBox):
    """Base class for settings groups with consistent styling."""

    def __init__(self, title: str):
        super().__init__(title)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(15, 20, 15, 15)

    def add_setting_row(self, label: str, widget: QWidget, description: str = None) -> QHBoxLayout:
        """Add a setting row with label and widget."""
        row_layout = QHBoxLayout()

        # Label
        label_widget = QLabel(label)
        label_widget.setMinimumWidth(150)
        label_widget.setStyleSheet("font-weight: normal;")
        row_layout.addWidget(label_widget)

        # Widget
        row_layout.addWidget(widget)
        row_layout.addStretch()

        self.layout.addLayout(row_layout)

        # Description
        if description:
            desc_label = QLabel(description)
            desc_label.setStyleSheet("""
                color: #666;
                font-size: 11px;
                font-style: italic;
                margin-left: 150px;
                margin-top: -8px;
            """)
            desc_label.setWordWrap(True)
            self.layout.addWidget(desc_label)

        return row_layout


class EditorSettingsTab(QScrollArea):
    """Editor settings tab."""

    settings_changed = pyqtSignal()

    def __init__(self, settings_manager: SettingsManager):
        super().__init__()
        self.settings_manager = settings_manager
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarNever)

        # Main widget
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Font settings
        self.setup_font_settings(layout)

        # Appearance settings
        self.setup_appearance_settings(layout)

        # Behavior settings
        self.setup_behavior_settings(layout)

        # Advanced settings
        self.setup_advanced_settings(layout)

        layout.addStretch()
        self.setWidget(main_widget)

    def setup_font_settings(self, layout: QVBoxLayout):
        """Setup font-related settings."""
        group = SettingsGroup("Font & Display")

        # Font family
        self.font_combo = QComboBox()
        self.font_combo.addItems([
            "Consolas", "Monaco", "Menlo", "Courier New",
            "JetBrains Mono", "Fira Code", "Source Code Pro"
        ])
        self.font_combo.setCurrentText(self.settings_manager.get('editor.font_family'))
        self.font_combo.currentTextChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Font Family:",
            self.font_combo,
            "Choose a monospace font for the code editor"
        )

        # Font size
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 32)
        self.font_size_spin.setValue(self.settings_manager.get('editor.font_size'))
        self.font_size_spin.valueChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Font Size:",
            self.font_size_spin,
            "Editor font size in points"
        )

        # Font preview
        self.font_preview = QTextEdit()
        self.font_preview.setMaximumHeight(100)
        self.font_preview.setPlainText("def hello_world():\n    print('Hello, World!')\n    return True")
        self.font_preview.setReadOnly(True)
        self._update_font_preview()
        group.layout.addWidget(QLabel("Preview:"))
        group.layout.addWidget(self.font_preview)

        layout.addWidget(group)

    def setup_appearance_settings(self, layout: QVBoxLayout):
        """Setup appearance settings."""
        group = SettingsGroup("Appearance")

        # Editor theme
        self.theme_combo = QComboBox()
        for theme in CodeEditorTheme:
            self.theme_combo.addItem(theme.value.replace('_', ' ').title(), theme)

        current_theme = self.settings_manager.get('editor.theme')
        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        self.theme_combo.currentIndexChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Editor Theme:",
            self.theme_combo,
            "Color scheme for the code editor"
        )

        # Line numbers
        self.line_numbers_check = QCheckBox()
        self.line_numbers_check.setChecked(self.settings_manager.get('editor.show_line_numbers'))
        self.line_numbers_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Show Line Numbers:",
            self.line_numbers_check,
            "Display line numbers in the editor margin"
        )

        # Word wrap
        self.word_wrap_check = QCheckBox()
        self.word_wrap_check.setChecked(self.settings_manager.get('editor.word_wrap'))
        self.word_wrap_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Word Wrap:",
            self.word_wrap_check,
            "Wrap long lines instead of showing horizontal scrollbar"
        )

        # Highlight current line
        self.highlight_line_check = QCheckBox()
        self.highlight_line_check.setChecked(self.settings_manager.get('editor.highlight_current_line'))
        self.highlight_line_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Highlight Current Line:",
            self.highlight_line_check,
            "Highlight the line where the cursor is located"
        )

        layout.addWidget(group)

    def setup_behavior_settings(self, layout: QVBoxLayout):
        """Setup behavior settings."""
        group = SettingsGroup("Behavior")

        # Tab size
        self.tab_size_spin = QSpinBox()
        self.tab_size_spin.setRange(1, 8)
        self.tab_size_spin.setValue(self.settings_manager.get('editor.tab_size'))
        self.tab_size_spin.valueChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Tab Size:",
            self.tab_size_spin,
            "Number of spaces per tab character"
        )

        # Auto indent
        self.auto_indent_check = QCheckBox()
        self.auto_indent_check.setChecked(self.settings_manager.get('editor.auto_indent'))
        self.auto_indent_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Auto Indent:",
            self.auto_indent_check,
            "Automatically indent new lines"
        )

        # Auto save interval
        self.auto_save_spin = QSpinBox()
        self.auto_save_spin.setRange(5, 300)
        self.auto_save_spin.setSuffix(" seconds")
        self.auto_save_spin.setValue(self.settings_manager.get('editor.auto_save_interval'))
        self.auto_save_spin.valueChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Auto Save:",
            self.auto_save_spin,
            "Automatically save code changes after this interval"
        )

        # Auto complete
        self.auto_complete_check = QCheckBox()
        self.auto_complete_check.setChecked(self.settings_manager.get('editor.enable_auto_complete'))
        self.auto_complete_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Auto Complete:",
            self.auto_complete_check,
            "Show code completion suggestions while typing"
        )

        layout.addWidget(group)

    def setup_advanced_settings(self, layout: QVBoxLayout):
        """Setup advanced settings."""
        group = SettingsGroup("Advanced")

        # Syntax highlighting
        self.syntax_highlight_check = QCheckBox()
        self.syntax_highlight_check.setChecked(self.settings_manager.get('editor.enable_syntax_highlighting'))
        self.syntax_highlight_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Syntax Highlighting:",
            self.syntax_highlight_check,
            "Highlight code syntax with colors"
        )

        # Code folding
        self.code_folding_check = QCheckBox()
        self.code_folding_check.setChecked(self.settings_manager.get('editor.enable_code_folding'))
        self.code_folding_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Code Folding:",
            self.code_folding_check,
            "Allow collapsing and expanding code blocks"
        )

        # Show whitespace
        self.whitespace_check = QCheckBox()
        self.whitespace_check.setChecked(self.settings_manager.get('editor.show_whitespace'))
        self.whitespace_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Show Whitespace:",
            self.whitespace_check,
            "Display dots for spaces and arrows for tabs"
        )

        layout.addWidget(group)

    def _on_setting_changed(self):
        """Handle setting changes."""
        self._update_font_preview()
        self.settings_changed.emit()

    def _update_font_preview(self):
        """Update font preview."""
        font = QFont(self.font_combo.currentText(), self.font_size_spin.value())
        self.font_preview.setFont(font)

    def apply_settings(self):
        """Apply settings to the manager."""
        self.settings_manager.set('editor.font_family', self.font_combo.currentText())
        self.settings_manager.set('editor.font_size', self.font_size_spin.value())
        self.settings_manager.set('editor.theme', self.theme_combo.currentData())
        self.settings_manager.set('editor.show_line_numbers', self.line_numbers_check.isChecked())
        self.settings_manager.set('editor.word_wrap', self.word_wrap_check.isChecked())
        self.settings_manager.set('editor.highlight_current_line', self.highlight_line_check.isChecked())
        self.settings_manager.set('editor.tab_size', self.tab_size_spin.value())
        self.settings_manager.set('editor.auto_indent', self.auto_indent_check.isChecked())
        self.settings_manager.set('editor.auto_save_interval', self.auto_save_spin.value())
        self.settings_manager.set('editor.enable_auto_complete', self.auto_complete_check.isChecked())
        self.settings_manager.set('editor.enable_syntax_highlighting', self.syntax_highlight_check.isChecked())
        self.settings_manager.set('editor.enable_code_folding', self.code_folding_check.isChecked())
        self.settings_manager.set('editor.show_whitespace', self.whitespace_check.isChecked())


class UISettingsTab(QScrollArea):
    """UI settings tab."""

    settings_changed = pyqtSignal()

    def __init__(self, settings_manager: SettingsManager):
        super().__init__()
        self.settings_manager = settings_manager
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarNever)

        # Main widget
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Theme settings
        self.setup_theme_settings(layout)

        # Window settings
        self.setup_window_settings(layout)

        # Notification settings
        self.setup_notification_settings(layout)

        layout.addStretch()
        self.setWidget(main_widget)

    def setup_theme_settings(self, layout: QVBoxLayout):
        """Setup theme settings."""
        group = SettingsGroup("Theme & Appearance")

        # UI Theme
        self.ui_theme_combo = QComboBox()
        for theme in ThemeMode:
            self.ui_theme_combo.addItem(theme.value.title(), theme)

        current_theme = self.settings_manager.get('ui.theme')
        index = self.ui_theme_combo.findData(current_theme)
        if index >= 0:
            self.ui_theme_combo.setCurrentIndex(index)

        self.ui_theme_combo.currentIndexChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Application Theme:",
            self.ui_theme_combo,
            "Light, dark, or follow system theme"
        )

        # Language
        self.language_combo = QComboBox()
        for lang in LanguagePreference:
            self.language_combo.addItem(lang.value.upper(), lang)

        current_lang = self.settings_manager.get('ui.language')
        index = self.language_combo.findData(current_lang)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)

        self.language_combo.currentIndexChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Interface Language:",
            self.language_combo,
            "Language for the user interface"
        )

        # Animations
        self.animations_check = QCheckBox()
        self.animations_check.setChecked(self.settings_manager.get('ui.animation_enabled'))
        self.animations_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Enable Animations:",
            self.animations_check,
            "Use smooth animations for UI transitions"
        )

        # Compact mode
        self.compact_mode_check = QCheckBox()
        self.compact_mode_check.setChecked(self.settings_manager.get('ui.compact_mode'))
        self.compact_mode_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Compact Mode:",
            self.compact_mode_check,
            "Use smaller spacing and controls to fit more content"
        )

        layout.addWidget(group)

    def setup_window_settings(self, layout: QVBoxLayout):
        """Setup window settings."""
        group = SettingsGroup("Window & Layout")

        # Show welcome screen
        self.welcome_screen_check = QCheckBox()
        self.welcome_screen_check.setChecked(self.settings_manager.get('ui.show_welcome_screen'))
        self.welcome_screen_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Show Welcome Screen:",
            self.welcome_screen_check,
            "Display welcome screen when starting the application"
        )

        # Auto-hide sidebar
        self.auto_hide_sidebar_check = QCheckBox()
        self.auto_hide_sidebar_check.setChecked(self.settings_manager.get('ui.auto_hide_sidebar'))
        self.auto_hide_sidebar_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Auto-hide Sidebar:",
            self.auto_hide_sidebar_check,
            "Automatically hide sidebar when not in use"
        )

        # Sidebar width
        self.sidebar_width_spin = QSpinBox()
        self.sidebar_width_spin.setRange(200, 500)
        self.sidebar_width_spin.setSuffix(" px")
        self.sidebar_width_spin.setValue(self.settings_manager.get('ui.sidebar_width'))
        self.sidebar_width_spin.valueChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Sidebar Width:",
            self.sidebar_width_spin,
            "Width of the sidebar in pixels"
        )

        # Content splitter ratio
        self.splitter_ratio_slider = QSlider(Qt.Orientation.Horizontal)
        self.splitter_ratio_slider.setRange(30, 90)
        self.splitter_ratio_slider.setValue(int(self.settings_manager.get('ui.content_splitter_ratio') * 100))
        self.splitter_ratio_slider.valueChanged.connect(self._on_setting_changed)

        ratio_layout = QHBoxLayout()
        ratio_layout.addWidget(self.splitter_ratio_slider)
        self.ratio_label = QLabel(f"{self.splitter_ratio_slider.value()}%")
        self.ratio_label.setMinimumWidth(40)
        ratio_layout.addWidget(self.ratio_label)

        group.add_setting_row(
            "Content/Editor Ratio:",
            ratio_layout,
            "Ratio between content viewer and code editor"
        )

        layout.addWidget(group)

    def setup_notification_settings(self, layout: QVBoxLayout):
        """Setup notification settings."""
        group = SettingsGroup("Notifications")

        # Enable notifications
        self.notifications_check = QCheckBox()
        self.notifications_check.setChecked(self.settings_manager.get('ui.notification_enabled'))
        self.notifications_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Enable Notifications:",
            self.notifications_check,
            "Show popup notifications for events"
        )

        # Notification duration
        self.notification_duration_spin = QSpinBox()
        self.notification_duration_spin.setRange(1000, 10000)
        self.notification_duration_spin.setSuffix(" ms")
        self.notification_duration_spin.setValue(self.settings_manager.get('ui.notification_duration'))
        self.notification_duration_spin.valueChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Notification Duration:",
            self.notification_duration_spin,
            "How long notifications stay visible"
        )

        layout.addWidget(group)

    def _on_setting_changed(self):
        """Handle setting changes."""
        # Update ratio label
        if hasattr(self, 'ratio_label'):
            self.ratio_label.setText(f"{self.splitter_ratio_slider.value()}%")

        self.settings_changed.emit()

    def apply_settings(self):
        """Apply settings to the manager."""
        self.settings_manager.set('ui.theme', self.ui_theme_combo.currentData())
        self.settings_manager.set('ui.language', self.language_combo.currentData())
        self.settings_manager.set('ui.animation_enabled', self.animations_check.isChecked())
        self.settings_manager.set('ui.compact_mode', self.compact_mode_check.isChecked())
        self.settings_manager.set('ui.show_welcome_screen', self.welcome_screen_check.isChecked())
        self.settings_manager.set('ui.auto_hide_sidebar', self.auto_hide_sidebar_check.isChecked())
        self.settings_manager.set('ui.sidebar_width', self.sidebar_width_spin.value())
        self.settings_manager.set('ui.content_splitter_ratio', self.splitter_ratio_slider.value() / 100.0)
        self.settings_manager.set('ui.notification_enabled', self.notifications_check.isChecked())
        self.settings_manager.set('ui.notification_duration', self.notification_duration_spin.value())


class LearningSettingsTab(QScrollArea):
    """Learning settings tab."""

    settings_changed = pyqtSignal()

    def __init__(self, settings_manager: SettingsManager):
        super().__init__()
        self.settings_manager = settings_manager
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarNever)

        # Main widget
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Progress settings
        self.setup_progress_settings(layout)

        # Learning preferences
        self.setup_learning_preferences(layout)

        # Goals and reminders
        self.setup_goals_settings(layout)

        layout.addStretch()
        self.setWidget(main_widget)

    def setup_progress_settings(self, layout: QVBoxLayout):
        """Setup progress tracking settings."""
        group = SettingsGroup("Progress Tracking")

        # Auto-save progress
        self.auto_save_progress_check = QCheckBox()
        self.auto_save_progress_check.setChecked(self.settings_manager.get('learning.auto_save_progress'))
        self.auto_save_progress_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Auto-save Progress:",
            self.auto_save_progress_check,
            "Automatically save your learning progress"
        )

        # Progress notifications
        self.progress_notifications_check = QCheckBox()
        self.progress_notifications_check.setChecked(self.settings_manager.get('learning.show_progress_notifications'))
        self.progress_notifications_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Progress Notifications:",
            self.progress_notifications_check,
            "Show notifications when you complete topics or exercises"
        )

        # Achievements
        self.achievements_check = QCheckBox()
        self.achievements_check.setChecked(self.settings_manager.get('learning.enable_achievements'))
        self.achievements_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Enable Achievements:",
            self.achievements_check,
            "Unlock achievements as you learn and practice"
        )

        # Streak tracking
        self.streak_tracking_check = QCheckBox()
        self.streak_tracking_check.setChecked(self.settings_manager.get('learning.streak_tracking'))
        self.streak_tracking_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Streak Tracking:",
            self.streak_tracking_check,
            "Track consecutive days of learning"
        )

        layout.addWidget(group)

    def setup_learning_preferences(self, layout: QVBoxLayout):
        """Setup learning preferences."""
        group = SettingsGroup("Learning Preferences")

        # Difficulty preference
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Adaptive", "Beginner", "Intermediate", "Advanced"])
        current_diff = self.settings_manager.get('learning.difficulty_preference')
        index = self.difficulty_combo.findText(current_diff.title())
        if index >= 0:
            self.difficulty_combo.setCurrentIndex(index)
        self.difficulty_combo.currentTextChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Difficulty Level:",
            self.difficulty_combo,
            "Preferred difficulty level for exercises and content"
        )

        # Show hints
        self.show_hints_check = QCheckBox()
        self.show_hints_check.setChecked(self.settings_manager.get('learning.show_hints'))
        self.show_hints_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Show Hints:",
            self.show_hints_check,
            "Display helpful hints during exercises"
        )

        # Auto-advance topics
        self.auto_advance_check = QCheckBox()
        self.auto_advance_check.setChecked(self.settings_manager.get('learning.auto_advance_topics'))
        self.auto_advance_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Auto-advance Topics:",
            self.auto_advance_check,
            "Automatically move to next topic when current one is completed"
        )

        layout.addWidget(group)

    def setup_goals_settings(self, layout: QVBoxLayout):
        """Setup goals and reminders."""
        group = SettingsGroup("Goals & Reminders")

        # Daily goal
        self.daily_goal_spin = QSpinBox()
        self.daily_goal_spin.setRange(10, 480)
        self.daily_goal_spin.setSuffix(" minutes")
        self.daily_goal_spin.setValue(self.settings_manager.get('learning.daily_goal_minutes'))
        self.daily_goal_spin.valueChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Daily Goal:",
            self.daily_goal_spin,
            "Target minutes of learning per day"
        )

        # Weekly goal
        self.weekly_goal_spin = QSpinBox()
        self.weekly_goal_spin.setRange(1, 40)
        self.weekly_goal_spin.setSuffix(" hours")
        self.weekly_goal_spin.setValue(self.settings_manager.get('learning.weekly_goal_hours'))
        self.weekly_goal_spin.valueChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Weekly Goal:",
            self.weekly_goal_spin,
            "Target hours of learning per week"
        )

        # Practice reminders
        self.reminders_check = QCheckBox()
        self.reminders_check.setChecked(self.settings_manager.get('learning.practice_reminders'))
        self.reminders_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Practice Reminders:",
            self.reminders_check,
            "Get reminded to practice if you haven't learned recently"
        )

        layout.addWidget(group)

    def _on_setting_changed(self):
        """Handle setting changes."""
        self.settings_changed.emit()

    def apply_settings(self):
        """Apply settings to the manager."""
        self.settings_manager.set('learning.auto_save_progress', self.auto_save_progress_check.isChecked())
        self.settings_manager.set('learning.show_progress_notifications', self.progress_notifications_check.isChecked())
        self.settings_manager.set('learning.enable_achievements', self.achievements_check.isChecked())
        self.settings_manager.set('learning.streak_tracking', self.streak_tracking_check.isChecked())
        self.settings_manager.set('learning.difficulty_preference', self.difficulty_combo.currentText().lower())
        self.settings_manager.set('learning.show_hints', self.show_hints_check.isChecked())
        self.settings_manager.set('learning.auto_advance_topics', self.auto_advance_check.isChecked())
        self.settings_manager.set('learning.daily_goal_minutes', self.daily_goal_spin.value())
        self.settings_manager.set('learning.weekly_goal_hours', self.weekly_goal_spin.value())
        self.settings_manager.set('learning.practice_reminders', self.reminders_check.isChecked())


class PerformanceSettingsTab(QScrollArea):
    """Performance settings tab."""

    settings_changed = pyqtSignal()

    def __init__(self, settings_manager: SettingsManager):
        super().__init__()
        self.settings_manager = settings_manager
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarNever)

        # Main widget
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Caching settings
        self.setup_caching_settings(layout)

        # Loading settings
        self.setup_loading_settings(layout)

        # Monitoring settings
        self.setup_monitoring_settings(layout)

        layout.addStretch()
        self.setWidget(main_widget)

    def setup_caching_settings(self, layout: QVBoxLayout):
        """Setup caching settings."""
        group = SettingsGroup("Caching")

        # Enable caching
        self.enable_caching_check = QCheckBox()
        self.enable_caching_check.setChecked(self.settings_manager.get('performance.enable_caching'))
        self.enable_caching_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Enable Caching:",
            self.enable_caching_check,
            "Cache content in memory for faster access"
        )

        # Cache size
        self.cache_size_spin = QSpinBox()
        self.cache_size_spin.setRange(10, 1000)
        self.cache_size_spin.setSuffix(" MB")
        self.cache_size_spin.setValue(self.settings_manager.get('performance.cache_size_mb'))
        self.cache_size_spin.valueChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Cache Size:",
            self.cache_size_spin,
            "Maximum memory to use for caching"
        )

        layout.addWidget(group)

    def setup_loading_settings(self, layout: QVBoxLayout):
        """Setup loading settings."""
        group = SettingsGroup("Loading & Processing")

        # Parallel loading
        self.parallel_loading_check = QCheckBox()
        self.parallel_loading_check.setChecked(self.settings_manager.get('performance.parallel_loading'))
        self.parallel_loading_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Parallel Loading:",
            self.parallel_loading_check,
            "Load content using multiple threads for better performance"
        )

        # Lazy loading
        self.lazy_loading_check = QCheckBox()
        self.lazy_loading_check.setChecked(self.settings_manager.get('performance.lazy_loading'))
        self.lazy_loading_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Lazy Loading:",
            self.lazy_loading_check,
            "Load content only when needed to reduce startup time"
        )

        # Preload next topic
        self.preload_next_check = QCheckBox()
        self.preload_next_check.setChecked(self.settings_manager.get('performance.preload_next_topic'))
        self.preload_next_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Preload Next Topic:",
            self.preload_next_check,
            "Preload the next topic in the background"
        )

        # Max concurrent operations
        self.max_operations_spin = QSpinBox()
        self.max_operations_spin.setRange(1, 16)
        self.max_operations_spin.setValue(self.settings_manager.get('performance.max_concurrent_operations'))
        self.max_operations_spin.valueChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Max Concurrent Operations:",
            self.max_operations_spin,
            "Maximum number of simultaneous background operations"
        )

        layout.addWidget(group)

    def setup_monitoring_settings(self, layout: QVBoxLayout):
        """Setup monitoring settings."""
        group = SettingsGroup("Performance Monitoring")

        # Enable monitoring
        self.enable_monitoring_check = QCheckBox()
        self.enable_monitoring_check.setChecked(self.settings_manager.get('performance.enable_performance_monitoring'))
        self.enable_monitoring_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Enable Monitoring:",
            self.enable_monitoring_check,
            "Monitor application performance and resource usage"
        )

        # Log slow operations
        self.log_slow_check = QCheckBox()
        self.log_slow_check.setChecked(self.settings_manager.get('performance.log_slow_operations'))
        self.log_slow_check.toggled.connect(self._on_setting_changed)
        group.add_setting_row(
            "Log Slow Operations:",
            self.log_slow_check,
            "Log operations that take longer than the threshold"
        )

        # Slow operation threshold
        self.slow_threshold_spin = QSpinBox()
        self.slow_threshold_spin.setRange(100, 10000)
        self.slow_threshold_spin.setSuffix(" ms")
        self.slow_threshold_spin.setValue(self.settings_manager.get('performance.slow_operation_threshold_ms'))
        self.slow_threshold_spin.valueChanged.connect(self._on_setting_changed)
        group.add_setting_row(
            "Slow Operation Threshold:",
            self.slow_threshold_spin,
            "Operations slower than this will be logged as slow"
        )

        layout.addWidget(group)

    def _on_setting_changed(self):
        """Handle setting changes."""
        self.settings_changed.emit()

    def apply_settings(self):
        """Apply settings to the manager."""
        self.settings_manager.set('performance.enable_caching', self.enable_caching_check.isChecked())
        self.settings_manager.set('performance.cache_size_mb', self.cache_size_spin.value())
        self.settings_manager.set('performance.parallel_loading', self.parallel_loading_check.isChecked())
        self.settings_manager.set('performance.lazy_loading', self.lazy_loading_check.isChecked())
        self.settings_manager.set('performance.preload_next_topic', self.preload_next_check.isChecked())
        self.settings_manager.set('performance.max_concurrent_operations', self.max_operations_spin.value())
        self.settings_manager.set('performance.enable_performance_monitoring', self.enable_monitoring_check.isChecked())
        self.settings_manager.set('performance.log_slow_operations', self.log_slow_check.isChecked())
        self.settings_manager.set('performance.slow_operation_threshold_ms', self.slow_threshold_spin.value())


class EnhancedSettingsDialog(QDialog):
    """Enhanced settings dialog with tabbed interface and validation."""

    settings_applied = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_manager = get_settings_manager()
        self.has_changes = False

        self.setWindowTitle("Settings")
        self.setMinimumSize(800, 600)
        self.setModal(True)

        self.setup_ui()
        self.setup_animations()

        # Track changes
        self.settings_tabs = []

    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Application Settings")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                margin-top: -1px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                border: 1px solid #c0c0c0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            QTabBar::tab:hover {
                background: #e0e0e0;
            }
        """)

        # Add tabs
        self.editor_tab = EditorSettingsTab(self.settings_manager)
        self.editor_tab.settings_changed.connect(self._on_settings_changed)
        self.tab_widget.addTab(self.editor_tab, "Editor")
        self.settings_tabs.append(self.editor_tab)

        self.ui_tab = UISettingsTab(self.settings_manager)
        self.ui_tab.settings_changed.connect(self._on_settings_changed)
        self.tab_widget.addTab(self.ui_tab, "Interface")
        self.settings_tabs.append(self.ui_tab)

        self.learning_tab = LearningSettingsTab(self.settings_manager)
        self.learning_tab.settings_changed.connect(self._on_settings_changed)
        self.tab_widget.addTab(self.learning_tab, "Learning")
        self.settings_tabs.append(self.learning_tab)

        self.performance_tab = PerformanceSettingsTab(self.settings_manager)
        self.performance_tab.settings_changed.connect(self._on_settings_changed)
        self.tab_widget.addTab(self.performance_tab, "Performance")
        self.settings_tabs.append(self.performance_tab)

        layout.addWidget(self.tab_widget)

        # Status bar for changes
        self.status_frame = QFrame()
        self.status_frame.setStyleSheet("""
            QFrame {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        self.status_frame.setVisible(False)

        status_layout = QHBoxLayout(self.status_frame)
        status_layout.setContentsMargins(12, 8, 12, 8)

        self.status_label = QLabel("Settings have been modified. Click Apply to save changes.")
        self.status_label.setStyleSheet("color: #856404; font-weight: bold;")
        status_layout.addWidget(self.status_label)

        layout.addWidget(self.status_frame)

        # Buttons
        self.setup_buttons(layout)

    def setup_buttons(self, layout: QVBoxLayout):
        """Setup dialog buttons."""
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # Reset button
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.clicked.connect(self.reset_settings)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        button_layout.addWidget(self.reset_button)

        button_layout.addSpacing(10)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        button_layout.addWidget(self.cancel_button)

        # Apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        self.apply_button.setEnabled(False)
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        button_layout.addWidget(self.apply_button)

        # OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept_settings)
        self.ok_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        button_layout.addWidget(self.ok_button)

        layout.addLayout(button_layout)

    def setup_animations(self):
        """Setup UI animations."""
        self.status_animation = QPropertyAnimation(self.status_frame, b"maximumHeight")
        self.status_animation.setDuration(300)
        self.status_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _on_settings_changed(self):
        """Handle settings changes."""
        self.has_changes = True
        self.apply_button.setEnabled(True)
        self._show_status_bar()

    def _show_status_bar(self):
        """Show status bar with animation."""
        if not self.status_frame.isVisible():
            self.status_frame.show()
            self.status_frame.setMaximumHeight(0)

            target_height = self.status_frame.sizeHint().height()
            self.status_animation.setStartValue(0)
            self.status_animation.setEndValue(target_height)
            self.status_animation.start()

    def _hide_status_bar(self):
        """Hide status bar with animation."""
        if self.status_frame.isVisible():
            current_height = self.status_frame.height()
            self.status_animation.setStartValue(current_height)
            self.status_animation.setEndValue(0)
            self.status_animation.finished.connect(lambda: self.status_frame.hide())
            self.status_animation.start()

    def apply_settings(self):
        """Apply all settings."""
        try:
            # Apply settings from all tabs
            for tab in self.settings_tabs:
                tab.apply_settings()

            self.has_changes = False
            self.apply_button.setEnabled(False)
            self._hide_status_bar()

            # Emit signal
            self.settings_applied.emit()

            # Show success message
            from utils.enhanced_notifications import show_success
            show_success("Settings applied successfully!", self)

        except Exception as e:
            logger.error(f"Error applying settings: {e}")
            QMessageBox.critical(self, "Error", f"Failed to apply settings:\n{str(e)}")

    def accept_settings(self):
        """Apply settings and close dialog."""
        if self.has_changes:
            self.apply_settings()
        self.accept()

    def reset_settings(self):
        """Reset settings to defaults."""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to their default values?\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.settings_manager.reset_to_defaults()
                self.accept()

                # Show restart message
                QMessageBox.information(
                    self,
                    "Settings Reset",
                    "Settings have been reset to defaults.\n"
                    "Please restart the application for all changes to take effect."
                )

            except Exception as e:
                logger.error(f"Error resetting settings: {e}")
                QMessageBox.critical(self, "Error", f"Failed to reset settings:\n{str(e)}")

    def closeEvent(self, event):
        """Handle dialog close."""
        if self.has_changes:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to apply them before closing?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save
            )

            if reply == QMessageBox.StandardButton.Save:
                self.apply_settings()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()