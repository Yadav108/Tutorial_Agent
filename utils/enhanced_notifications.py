# utils/enhanced_notifications.py

import logging
from typing import Optional, Union
from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QPushButton, QGraphicsOpacityEffect, QApplication
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPen, QBrush, QFont

logger = logging.getLogger('TutorialAgent.Notifications')


class ToastNotification(QWidget):
    """Modern toast notification widget with animations."""

    closed = pyqtSignal()

    def __init__(self, message: str, notification_type: str = "info", duration: int = 3000, parent=None):
        super().__init__(parent)
        self.notification_type = notification_type
        self.duration = duration

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.setup_ui(message)
        self.setup_animations()

    def setup_ui(self, message: str):
        """Setup the notification UI."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Notification frame
        self.frame = QFrame()
        self.frame.setObjectName("notificationFrame")
        layout.addWidget(self.frame)

        # Frame layout
        frame_layout = QHBoxLayout(self.frame)
        frame_layout.setContentsMargins(20, 15, 20, 15)
        frame_layout.setSpacing(15)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        self.icon_label.setScaledContents(True)
        frame_layout.addWidget(self.icon_label)

        # Message
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setObjectName("messageLabel")
        frame_layout.addWidget(self.message_label, 1)

        # Close button
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.hide_notification)
        frame_layout.addWidget(self.close_button)

        # Apply styles
        self.apply_styles()

        # Set fixed width and auto height
        self.setFixedWidth(400)
        self.adjustSize()

    def apply_styles(self):
        """Apply styles based on notification type."""
        colors = {
            "success": {"bg": "#d4edda", "border": "#c3e6cb", "text": "#155724", "icon": "#28a745"},
            "error": {"bg": "#f8d7da", "border": "#f5c6cb", "text": "#721c24", "icon": "#dc3545"},
            "warning": {"bg": "#fff3cd", "border": "#ffeaa7", "text": "#856404", "icon": "#ffc107"},
            "info": {"bg": "#d1ecf1", "border": "#bee5eb", "text": "#0c5460", "icon": "#17a2b8"}
        }

        color_scheme = colors.get(self.notification_type, colors["info"])

        self.setStyleSheet(f"""
            QFrame#notificationFrame {{
                background-color: {color_scheme["bg"]};
                border: 1px solid {color_scheme["border"]};
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }}
            QLabel#messageLabel {{
                color: {color_scheme["text"]};
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton#closeButton {{
                background: transparent;
                border: none;
                color: {color_scheme["text"]};
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
            }}
            QPushButton#closeButton:hover {{
                background-color: rgba(0, 0, 0, 0.1);
            }}
        """)

        # Set icon
        self.set_icon(color_scheme["icon"])

    def set_icon(self, color: str):
        """Set notification icon based on type."""
        icons = {
            "success": "✓",
            "error": "✗",
            "warning": "⚠",
            "info": "ℹ"
        }

        icon_text = icons.get(self.notification_type, "ℹ")

        # Create icon pixmap
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circle background
        painter.setBrush(QBrush(Qt.GlobalColor.white))
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.drawEllipse(2, 2, 20, 20)

        # Draw icon text
        font = QFont()
        font.setPixelSize(14)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QPen(Qt.GlobalColor.black))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, icon_text)

        painter.end()

        self.icon_label.setPixmap(pixmap)

    def setup_animations(self):
        """Setup entrance and exit animations."""
        # Opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)

        # Slide in animation
        self.slide_animation = QPropertyAnimation(self, b"geometry")
        self.slide_animation.setDuration(300)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Fade in animation
        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Fade out animation
        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out_animation.setDuration(200)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out_animation.finished.connect(self.close)
        self.fade_out_animation.finished.connect(self.closed.emit)

        # Auto-hide timer
        if self.duration > 0:
            self.hide_timer = QTimer()
            self.hide_timer.setSingleShot(True)
            self.hide_timer.timeout.connect(self.hide_notification)

    def show_notification(self, parent_widget=None):
        """Show the notification with animation."""
        # Position the notification
        if parent_widget:
            parent_rect = parent_widget.rect()
            parent_global = parent_widget.mapToGlobal(parent_rect.topRight())

            # Position at top-right of parent
            x = parent_global.x() - self.width() - 20
            y = parent_global.y() + 20
        else:
            # Position at screen top-right
            screen = QApplication.primaryScreen().geometry()
            x = screen.width() - self.width() - 20
            y = 20

        # Set initial position (off-screen)
        start_rect = QRect(x + self.width(), y, self.width(), self.height())
        end_rect = QRect(x, y, self.width(), self.height())

        self.setGeometry(start_rect)
        self.show()

        # Start animations
        self.slide_animation.setStartValue(start_rect)
        self.slide_animation.setEndValue(end_rect)
        self.slide_animation.start()
        self.fade_in_animation.start()

        # Start auto-hide timer
        if hasattr(self, 'hide_timer'):
            self.hide_timer.start(self.duration)

    def hide_notification(self):
        """Hide the notification with animation."""
        if hasattr(self, 'hide_timer'):
            self.hide_timer.stop()
        self.fade_out_animation.start()

    def mousePressEvent(self, event):
        """Close notification on click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.hide_notification()


class NotificationManager:
    """Manages multiple notifications and positioning."""

    def __init__(self):
        self.notifications = []
        self.spacing = 10

    def show_notification(self, message: str, notification_type: str = "info",
                          duration: int = 3000, parent=None):
        """Show a new notification."""
        # Create notification
        notification = ToastNotification(message, notification_type, duration, parent)
        notification.closed.connect(lambda: self._remove_notification(notification))

        # Add to list
        self.notifications.append(notification)

        # Position and show
        self._position_notifications(parent)
        notification.show_notification(parent)

        return notification

    def _remove_notification(self, notification):
        """Remove notification from list and reposition others."""
        if notification in self.notifications:
            self.notifications.remove(notification)
            self._reposition_notifications()

    def _position_notifications(self, parent_widget=None):
        """Position all notifications."""
        if parent_widget:
            parent_rect = parent_widget.rect()
            parent_global = parent_widget.mapToGlobal(parent_rect.topRight())
            base_x = parent_global.x() - 400 - 20  # notification width + margin
            base_y = parent_global.y() + 20
        else:
            screen = QApplication.primaryScreen().geometry()
            base_x = screen.width() - 400 - 20
            base_y = 20

        for i, notification in enumerate(self.notifications):
            y_offset = i * (notification.height() + self.spacing)
            notification.move(base_x, base_y + y_offset)

    def _reposition_notifications(self):
        """Reposition remaining notifications."""
        for i, notification in enumerate(self.notifications):
            current_rect = notification.geometry()
            new_y = 20 + i * (current_rect.height() + self.spacing)

            # Animate to new position
            animation = QPropertyAnimation(notification, b"geometry")
            animation.setDuration(200)
            animation.setStartValue(current_rect)
            animation.setEndValue(QRect(current_rect.x(), new_y, current_rect.width(), current_rect.height()))
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            animation.start()

            # Keep reference to prevent garbage collection
            notification._reposition_animation = animation

    def clear_all(self):
        """Clear all notifications."""
        for notification in self.notifications[:]:
            notification.hide_notification()


# Global notification manager
_notification_manager = NotificationManager()


def show_success(message: str, parent: Optional[QWidget] = None, duration: int = 3000) -> None:
    """Show a success notification."""
    try:
        logger.info(f"Success notification: {message}")
        _notification_manager.show_notification(message, "success", duration, parent)
    except Exception as e:
        logger.error(f"Error showing success notification: {e}")
        # Fallback to message box
        _show_fallback_message("Success", message, QMessageBox.Icon.Information, parent)


def show_error(message: str, parent: Optional[QWidget] = None, duration: int = 5000) -> None:
    """Show an error notification."""
    try:
        logger.error(f"Error notification: {message}")
        _notification_manager.show_notification(message, "error", duration, parent)
    except Exception as e:
        logger.error(f"Error showing error notification: {e}")
        # Fallback to message box
        _show_fallback_message("Error", message, QMessageBox.Icon.Critical, parent)


def show_warning(message: str, parent: Optional[QWidget] = None, duration: int = 4000) -> None:
    """Show a warning notification."""
    try:
        logger.warning(f"Warning notification: {message}")
        _notification_manager.show_notification(message, "warning", duration, parent)
    except Exception as e:
        logger.error(f"Error showing warning notification: {e}")
        # Fallback to message box
        _show_fallback_message("Warning", message, QMessageBox.Icon.Warning, parent)


def show_info(message: str, parent: Optional[QWidget] = None, duration: int = 3000) -> None:
    """Show an info notification."""
    try:
        logger.info(f"Info notification: {message}")
        _notification_manager.show_notification(message, "info", duration, parent)
    except Exception as e:
        logger.error(f"Error showing info notification: {e}")
        # Fallback to message box
        _show_fallback_message("Information", message, QMessageBox.Icon.Information, parent)


def _show_fallback_message(title: str, message: str, icon: QMessageBox.Icon, parent: Optional[QWidget] = None) -> None:
    """Show fallback message box when toast notifications fail."""
    try:
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
    except Exception as e:
        logger.critical(f"Error showing fallback message: {e}")


def clear_all_notifications() -> None:
    """Clear all active notifications."""
    try:
        _notification_manager.clear_all()
    except Exception as e:
        logger.error(f"Error clearing notifications: {e}")


# Additional utility functions for different use cases

def show_loading(message: str = "Loading...", parent: Optional[QWidget] = None) -> ToastNotification:
    """Show a persistent loading notification."""
    return _notification_manager.show_notification(message, "info", 0, parent)  # 0 duration = persistent


def show_progress(message: str, progress: int, parent: Optional[QWidget] = None) -> None:
    """Show a progress notification."""
    progress_message = f"{message} ({progress}%)"
    show_info(progress_message, parent, 2000)


def show_confirmation(message: str, parent: Optional[QWidget] = None) -> bool:
    """Show a confirmation dialog and return user choice."""
    try:
        reply = QMessageBox.question(
            parent,
            "Confirmation",
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
    except Exception as e:
        logger.error(f"Error showing confirmation: {e}")
        return False


def show_custom(title: str, message: str, icon_type: str = "info",
                parent: Optional[QWidget] = None, duration: int = 3000) -> None:
    """Show a custom notification with specified parameters."""
    try:
        _notification_manager.show_notification(message, icon_type, duration, parent)
    except Exception as e:
        logger.error(f"Error showing custom notification: {e}")
        # Fallback
        icon_map = {
            "success": QMessageBox.Icon.Information,
            "error": QMessageBox.Icon.Critical,
            "warning": QMessageBox.Icon.Warning,
            "info": QMessageBox.Icon.Information
        }
        _show_fallback_message(title, message, icon_map.get(icon_type, QMessageBox.Icon.Information), parent)


# Context manager for notifications
class NotificationContext:
    """Context manager for managing notifications during operations."""

    def __init__(self, loading_message: str = "Processing...",
                 success_message: str = "Operation completed successfully",
                 error_message: str = "Operation failed",
                 parent: Optional[QWidget] = None):
        self.loading_message = loading_message
        self.success_message = success_message
        self.error_message = error_message
        self.parent = parent
        self.loading_notification = None

    def __enter__(self):
        self.loading_notification = show_loading(self.loading_message, self.parent)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.loading_notification:
            self.loading_notification.hide_notification()

        if exc_type is None:
            # Success
            show_success(self.success_message, self.parent)
        else:
            # Error occurred
            error_msg = f"{self.error_message}: {str(exc_val)}" if exc_val else self.error_message
            show_error(error_msg, self.parent)

        return False  # Don't suppress exceptions

# Example usage:
# with NotificationContext("Saving file...", "File saved!", "Failed to save file", self):
#     # Your operation here
#     save_file()