# utils/error_handler.py

import logging
import traceback
import sys
from typing import Optional, Callable, Any, Dict
from functools import wraps
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QApplication, QWidget, QFrame,
    QProgressBar, QSystemTrayIcon
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QPropertyAnimation, QRect
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont, QColor

logger = logging.getLogger('TutorialAgent.ErrorHandler')


class NotificationLevel:
    """Notification levels for user feedback."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class ToastNotification(QFrame):
    """Toast notification widget for non-intrusive user feedback."""

    def __init__(self, message: str, level: str = NotificationLevel.INFO, duration: int = 3000):
        super().__init__()
        self.level = level
        self.duration = duration
        self.setup_ui()
        self.set_message(message)
        self.setup_animation()

    def setup_ui(self):
        """Setup the notification UI."""
        self.setFixedSize(300, 80)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        # Icon label
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        layout.addWidget(self.icon_label)

        # Message label
        self.message_label = QLabel()
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("color: white; font-size: 12px;")
        layout.addWidget(self.message_label, 1)

        # Close button
        close_button = QPushButton("×")
        close_button.setFixedSize(20, 20)
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }
        """)
        close_button.clicked.connect(self.hide_notification)
        layout.addWidget(close_button)

        # Set level-specific styling
        self.update_style()

    def update_style(self):
        """Update styling based on notification level."""
        styles = {
            NotificationLevel.INFO: {
                'background': 'rgba(52, 152, 219, 0.9)',
                'icon': '🛈'
            },
            NotificationLevel.SUCCESS: {
                'background': 'rgba(46, 204, 113, 0.9)',
                'icon': '✓'
            },
            NotificationLevel.WARNING: {
                'background': 'rgba(241, 196, 15, 0.9)',
                'icon': '⚠'
            },
            NotificationLevel.ERROR: {
                'background': 'rgba(231, 76, 60, 0.9)',
                'icon': '✗'
            }
        }

        style_info = styles.get(self.level, styles[NotificationLevel.INFO])

        self.setStyleSheet(f"""
            QFrame {{
                background: {style_info['background']};
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
        """)

        self.icon_label.setText(style_info['icon'])
        self.icon_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                text-align: center;
            }
        """)

    def set_message(self, message: str):
        """Set the notification message."""
        self.message_label.setText(message)

    def setup_animation(self):
        """Setup slide-in animation."""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)

        # Timer for auto-hide
        self.timer = QTimer()
        self.timer.timeout.connect(self.hide_notification)
        self.timer.setSingleShot(True)

    def show_notification(self, parent_widget: QWidget = None):
        """Show the notification with animation."""
        # Position the notification
        if parent_widget:
            parent_rect = parent_widget.geometry()
            x = parent_rect.right() - self.width() - 20
            y = parent_rect.top() + 20
        else:
            # Use screen geometry
            screen = QApplication.primaryScreen().geometry()
            x = screen.right() - self.width() - 20
            y = screen.top() + 20

        # Start position (off-screen)
        start_rect = QRect(x + self.width(), y, self.width(), self.height())
        end_rect = QRect(x, y, self.width(), self.height())

        self.setGeometry(start_rect)
        self.show()

        # Animate slide-in
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()

        # Start auto-hide timer
        if self.duration > 0:
            self.timer.start(self.duration)

    def hide_notification(self):
        """Hide the notification with animation."""
        current_rect = self.geometry()
        end_rect = QRect(
            current_rect.right(),
            current_rect.y(),
            current_rect.width(),
            current_rect.height()
        )

        self.animation.setStartValue(current_rect)
        self.animation.setEndValue(end_rect)
        self.animation.finished.connect(self.close)
        self.animation.start()


class ErrorDialog(QDialog):
    """Enhanced error dialog with details and reporting options."""

    def __init__(self, title: str, message: str, details: str = None, parent=None):
        super().__init__(parent)
        self.title = title
        self.message = message
        self.details = details
        self.setup_ui()

    def setup_ui(self):
        """Setup the error dialog UI."""
        self.setWindowTitle(self.title)
        self.setMinimumSize(400, 200)
        self.setMaximumSize(600, 400)

        layout = QVBoxLayout(self)

        # Message
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                padding: 10px;
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
        """)
        layout.addWidget(message_label)

        # Details (collapsible)
        if self.details:
            self.details_button = QPushButton("Show Details")
            self.details_button.clicked.connect(self.toggle_details)
            layout.addWidget(self.details_button)

            self.details_text = QTextEdit()
            self.details_text.setPlainText(self.details)
            self.details_text.setVisible(False)
            self.details_text.setMaximumHeight(150)
            self.details_text.setStyleSheet("""
                QTextEdit {
                    background: #2d2d30;
                    color: #d4d4d4;
                    font-family: 'Consolas', 'Courier New', monospace;
                    font-size: 10pt;
                    border: 1px solid #3e3e3e;
                }
            """)
            layout.addWidget(self.details_text)

        # Buttons
        button_layout = QHBoxLayout()

        copy_button = QPushButton("Copy Error")
        copy_button.clicked.connect(self.copy_error)
        button_layout.addWidget(copy_button)

        button_layout.addStretch()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        button_layout.addWidget(ok_button)

        layout.addLayout(button_layout)

        # Styling
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)

    def toggle_details(self):
        """Toggle the visibility of error details."""
        if self.details_text.isVisible():
            self.details_text.setVisible(False)
            self.details_button.setText("Show Details")
        else:
            self.details_text.setVisible(True)
            self.details_button.setText("Hide Details")

        self.adjustSize()

    def copy_error(self):
        """Copy error information to clipboard."""
        error_info = f"""
Error: {self.title}
Message: {self.message}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Details:
{self.details or 'No additional details'}
"""
        clipboard = QApplication.clipboard()
        clipboard.setText(error_info.strip())

        # Show confirmation
        NotificationManager.show_toast(
            "Error information copied to clipboard",
            NotificationLevel.SUCCESS
        )


class NotificationManager:
    """Global notification manager."""

    _instance = None
    _notifications = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def show_toast(cls, message: str, level: str = NotificationLevel.INFO,
                   duration: int = 3000, parent: QWidget = None):
        """Show a toast notification."""
        notification = ToastNotification(message, level, duration)
        notification.show_notification(parent)

        # Keep reference to prevent garbage collection
        cls._notifications.append(notification)

        # Clean up after duration + animation time
        QTimer.singleShot(duration + 500, lambda: cls._cleanup_notification(notification))

    @classmethod
    def _cleanup_notification(cls, notification):
        """Clean up notification reference."""
        if notification in cls._notifications:
            cls._notifications.remove(notification)

    @classmethod
    def show_error(cls, title: str, message: str, details: str = None, parent=None):
        """Show an error dialog."""
        dialog = ErrorDialog(title, message, details, parent)
        dialog.exec()

    @classmethod
    def show_system_notification(cls, title: str, message: str, icon_path: str = None):
        """Show system tray notification if available."""
        try:
            if QSystemTrayIcon.isSystemTrayAvailable():
                tray_icon = QSystemTrayIcon()
                if icon_path and Path(icon_path).exists():
                    tray_icon.setIcon(QIcon(icon_path))
                tray_icon.show()
                tray_icon.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 3000)
        except Exception as e:
            logger.debug(f"Could not show system notification: {e}")


def handle_exception(func):
    """Decorator for handling exceptions with user-friendly messages."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log the full exception
            logger.error(f"Exception in {func.__name__}: {str(e)}", exc_info=True)

            # Show user-friendly error
            error_title = f"Error in {func.__name__.replace('_', ' ').title()}"
            error_message = get_user_friendly_message(e)
            error_details = traceback.format_exc()

            NotificationManager.show_error(error_title, error_message, error_details)

            # Return None or appropriate default value
            return None

    return wrapper


def get_user_friendly_message(exception: Exception) -> str:
    """Convert technical exceptions to user-friendly messages."""
    error_messages = {
        FileNotFoundError: "A required file was not found. Please check your installation.",
        PermissionError: "Permission denied. Please check file permissions or run as administrator.",
        ConnectionError: "Network connection error. Please check your internet connection.",
        ImportError: "Missing required component. Please reinstall the application.",
        KeyError: "Configuration error. Please check your settings.",
        ValueError: "Invalid input value. Please check your input and try again.",
        TimeoutError: "Operation timed out. Please try again.",
        MemoryError: "Not enough memory to complete the operation.",
        OSError: "System error occurred. Please try again.",
    }

    # Check for specific exception types
    for exc_type, message in error_messages.items():
        if isinstance(exception, exc_type):
            return message

    # Default message
    return "An unexpected error occurred. Please try again or contact support if the problem persists."


class ProgressFeedback(QObject):
    """Progress feedback system for long-running operations."""

    progress_updated = pyqtSignal(int)  # percentage
    status_updated = pyqtSignal(str)  # status message
    completed = pyqtSignal(bool)  # success/failure

    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress_dialog = None
        self.current_progress = 0

    def start_operation(self, title: str, message: str, can_cancel: bool = False):
        """Start a progress operation."""
        self.progress_dialog = self.create_progress_dialog(title, message, can_cancel)
        self.progress_dialog.show()

        # Connect signals
        self.progress_updated.connect(self.progress_dialog.setValue)
        self.status_updated.connect(self.progress_dialog.setLabelText)
        self.completed.connect(self.on_operation_completed)

    def create_progress_dialog(self, title: str, message: str, can_cancel: bool):
        """Create a styled progress dialog."""
        from PyQt6.QtWidgets import QProgressDialog

        dialog = QProgressDialog(message, "Cancel" if can_cancel else None, 0, 100)
        dialog.setWindowTitle(title)
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.setMinimumDuration(1000)  # Show after 1 second

        # Styling
        dialog.setStyleSheet("""
            QProgressDialog {
                background-color: white;
                border: 1px solid #ddd;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
                background: #f8f9fa;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007bff, stop:1 #0056b3);
                border-radius: 3px;
            }
        """)

        return dialog

    def update_progress(self, percentage: int, status: str = None):
        """Update progress."""
        self.current_progress = max(0, min(100, percentage))
        self.progress_updated.emit(self.current_progress)

        if status:
            self.status_updated.emit(status)

    def complete_operation(self, success: bool, message: str = None):
        """Complete the operation."""
        self.completed.emit(success)

        if message:
            level = NotificationLevel.SUCCESS if success else NotificationLevel.ERROR
            NotificationManager.show_toast(message, level)

    def on_operation_completed(self, success: bool):
        """Handle operation completion."""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None


# Global exception handler
def setup_global_exception_handler():
    """Setup global exception handler for unhandled exceptions."""

    def exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # Log the exception
        logger.critical(
            "Unhandled exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

        # Show error dialog
        error_title = "Unexpected Error"
        error_message = get_user_friendly_message(exc_value)
        error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        try:
            NotificationManager.show_error(error_title, error_message, error_details)
        except:
            # Fallback to basic message box if notification system fails
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle(error_title)
            msg.setText(error_message)
            msg.exec()

    sys.excepthook = exception_handler


# Convenience functions
def show_success(message: str, parent: QWidget = None):
    """Show success notification."""
    NotificationManager.show_toast(message, NotificationLevel.SUCCESS, parent=parent)


def show_info(message: str, parent: QWidget = None):
    """Show info notification."""
    NotificationManager.show_toast(message, NotificationLevel.INFO, parent=parent)


def show_warning(message: str, parent: QWidget = None):
    """Show warning notification."""
    NotificationManager.show_toast(message, NotificationLevel.WARNING, parent=parent)


def show_error(message: str, parent: QWidget = None):
    """Show error notification."""
    NotificationManager.show_toast(message, NotificationLevel.ERROR, parent=parent)


# Example usage in your main_window.py:
"""
# At the top of main_window.py, add:
from utils.error_handler import handle_exception, show_success, show_error, setup_global_exception_handler

# In your __init__ method:
setup_global_exception_handler()

# Decorate methods that might fail:
@handle_exception
def on_language_selected(self, language):
    # Your existing code here

    # Add success feedback
    show_success(f"Loaded {language} content successfully")

# For progress operations:
def load_content_with_progress(self):
    progress = ProgressFeedback(self)
    progress.start_operation("Loading Content", "Please wait while content is loaded...")

    # Your loading code here with progress updates
    progress.update_progress(50, "Loading topics...")
    # More loading...
    progress.update_progress(100, "Content loaded successfully")
    progress.complete_operation(True, "Content loaded successfully")
"""