# utils/simple_notifications.py

from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QPushButton, QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer
import logging

logger = logging.getLogger('TutorialAgent.Notifications')


class SimpleToast(QFrame):
    """Simple toast notification for testing."""

    def __init__(self, message: str, toast_type: str = "success"):
        super().__init__()
        self.message = message
        self.toast_type = toast_type
        self.setup_ui()

    def setup_ui(self):
        """Setup the toast UI."""
        self.setFixedSize(300, 60)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        # Message label
        self.message_label = QLabel(self.message)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label, 1)

        # Close button
        close_button = QPushButton("×")
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Set style based on type
        self.update_style()

        # Auto-hide timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.setSingleShot(True)

    def update_style(self):
        """Update styling based on toast type."""
        if self.toast_type == "success":
            bg_color = "#28a745"  # Green
            icon = "✓"
        elif self.toast_type == "error":
            bg_color = "#dc3545"  # Red
            icon = "✗"
        else:  # info
            bg_color = "#17a2b8"  # Blue
            icon = "🛈"

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            QLabel {{
                color: white;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton {{
                background: transparent;
                color: white;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }}
        """)

        # Add icon to message
        self.message_label.setText(f"{icon} {self.message}")

    def show_toast(self, parent_widget: QWidget = None):
        """Show the toast notification."""
        # Position the toast
        if parent_widget:
            parent_rect = parent_widget.geometry()
            x = parent_rect.right() - self.width() - 20
            y = parent_rect.top() + 20
        else:
            # Use screen geometry
            screen = QApplication.primaryScreen().geometry()
            x = screen.right() - self.width() - 20
            y = screen.top() + 100

        self.move(x, y)
        self.show()
        self.raise_()

        # Auto-hide after 3 seconds
        self.timer.start(3000)


# Global toast storage to prevent garbage collection
_active_toasts = []


def show_success(message: str, parent: QWidget = None):
    """Show success toast notification."""
    toast = SimpleToast(message, "success")
    toast.show_toast(parent)
    _active_toasts.append(toast)

    # Clean up reference after 4 seconds
    QTimer.singleShot(4000, lambda: _cleanup_toast(toast))

    logger.info(f"Success: {message}")


def show_error(message: str, parent: QWidget = None):
    """Show error toast notification."""
    toast = SimpleToast(message, "error")
    toast.show_toast(parent)
    _active_toasts.append(toast)

    # Clean up reference after 4 seconds
    QTimer.singleShot(4000, lambda: _cleanup_toast(toast))

    logger.error(f"Error: {message}")


def _cleanup_toast(toast):
    """Remove toast from active list."""
    if toast in _active_toasts:
        _active_toasts.remove(toast)