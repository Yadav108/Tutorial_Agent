from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPixmap


class ConfirmationDialog(QDialog):
    """
    A customizable confirmation dialog for important actions
    Supports different confirmation types: warning, danger, info
    """

    WARNING = "warning"
    DANGER = "danger"
    INFO = "info"

    def __init__(self, title: str, message: str,
                 confirmation_type: str = WARNING,
                 parent=None,
                 ok_text: str = "OK",
                 cancel_text: str = "Cancel",
                 show_checkbox: bool = False,
                 checkbox_text: str = "Don't show this again"):
        super().__init__(parent)
        self.title = title
        self.message = message
        self.confirmation_type = confirmation_type
        self.ok_text = ok_text
        self.cancel_text = cancel_text
        self.show_checkbox = show_checkbox
        self.checkbox_text = checkbox_text
        self.checkbox_checked = False

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(self.title)
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QFrame {
                border: none;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Header with icon and title
        header_frame = self._create_header()
        layout.addWidget(header_frame)

        # Message content
        content_frame = self._create_content()
        layout.addWidget(content_frame)

        # Don't show again checkbox
        if self.show_checkbox:
            self.checkbox = QCheckBox(self.checkbox_text)
            self.checkbox.setStyleSheet("""
                QCheckBox {
                    color: #6c757d;
                }
            """)
            self.checkbox.stateChanged.connect(self._on_checkbox_changed)
            layout.addWidget(self.checkbox)

        # Buttons
        button_layout = self._create_buttons()
        layout.addLayout(button_layout)

    def _create_header(self) -> QFrame:
        """Create the header section with icon and title"""
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {self._get_header_color()};
                padding: 15px;
            }}
        """)
        header_layout = QHBoxLayout(header)

        # Icon
        icon_label = QLabel()
        icon = self._get_icon()
        icon_label.setPixmap(icon.pixmap(32, 32))
        header_layout.addWidget(icon_label)

        # Title
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        return header

    def _create_content(self) -> QFrame:
        """Create the content section with message"""
        content = QFrame()
        content.setStyleSheet("""
            QFrame {
                background: white;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content)

        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("color: #2c3e50;")
        message_label.setFont(QFont("Arial", 11))
        content_layout.addWidget(message_label)

        return content

    def _create_buttons(self) -> QHBoxLayout:
        """Create the button section"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # Cancel button
        self.cancel_button = QPushButton(self.cancel_text)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        # OK button
        self.ok_button = QPushButton(self.ok_text)
        self.ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._get_button_color()};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 80px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self._get_button_hover_color()};
            }}
        """)
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        return button_layout

    def _get_header_color(self) -> str:
        """Get header background color based on type"""
        colors = {
            self.WARNING: "#f39c12",
            self.DANGER: "#e74c3c",
            self.INFO: "#3498db"
        }
        return colors.get(self.confirmation_type, colors[self.WARNING])

    def _get_button_color(self) -> str:
        """Get OK button color based on type"""
        colors = {
            self.WARNING: "#f39c12",
            self.DANGER: "#e74c3c",
            self.INFO: "#3498db"
        }
        return colors.get(self.confirmation_type, colors[self.WARNING])

    def _get_button_hover_color(self) -> str:
        """Get OK button hover color based on type"""
        colors = {
            self.WARNING: "#e67e22",
            self.DANGER: "#c0392b",
            self.INFO: "#2980b9"
        }
        return colors.get(self.confirmation_type, colors[self.WARNING])

    def _get_icon(self) -> QIcon:
        """Get appropriate icon based on type"""
        icons = {
            self.WARNING: "warning.png",
            self.DANGER: "danger.png",
            self.INFO: "info.png"
        }
        return QIcon(f"assets/images/{icons.get(self.confirmation_type, 'warning.png')}")

    def _on_checkbox_changed(self, state):
        """Handle checkbox state change"""
        self.checkbox_checked = bool(state)

    def exec(self) -> tuple:
        """Execute the dialog and return result with checkbox state"""
        result = super().exec()
        return (result == QDialog.DialogCode.Accepted, self.checkbox_checked)


class ConfirmationDialogBuilder:
    """Builder class for creating confirmation dialogs"""

    def __init__(self):
        self.title = ""
        self.message = ""
        self.confirmation_type = ConfirmationDialog.WARNING
        self.ok_text = "OK"
        self.cancel_text = "Cancel"
        self.show_checkbox = False
        self.checkbox_text = "Don't show this again"
        self.parent = None

    def set_title(self, title: str):
        self.title = title
        return self

    def set_message(self, message: str):
        self.message = message
        return self

    def set_type(self, confirmation_type: str):
        self.confirmation_type = confirmation_type
        return self

    def set_ok_text(self, text: str):
        self.ok_text = text
        return self

    def set_cancel_text(self, text: str):
        self.cancel_text = text
        return self

    def add_checkbox(self, text: str = "Don't show this again"):
        self.show_checkbox = True
        self.checkbox_text = text
        return self

    def set_parent(self, parent):
        self.parent = parent
        return self

    def build(self) -> ConfirmationDialog:
        """Create and return the confirmation dialog"""
        return ConfirmationDialog(
            title=self.title,
            message=self.message,
            confirmation_type=self.confirmation_type,
            parent=self.parent,
            ok_text=self.ok_text,
            cancel_text=self.cancel_text,
            show_checkbox=self.show_checkbox,
            checkbox_text=self.checkbox_text
        )


# Example usage:
def show_delete_confirmation(parent=None) -> tuple:
    """Show a delete confirmation dialog"""
    dialog = (ConfirmationDialogBuilder()
              .set_title("Confirm Delete")
              .set_message("Are you sure you want to delete this item? This action cannot be undone.")
              .set_type(ConfirmationDialog.DANGER)
              .set_ok_text("Delete")
              .set_cancel_text("Keep")
              .add_checkbox("Don't ask me again")
              .set_parent(parent)
              .build())

    return dialog.exec()


def show_exit_confirmation(parent=None) -> tuple:
    """Show an exit confirmation dialog"""
    dialog = (ConfirmationDialogBuilder()
              .set_title("Exit Application")
              .set_message("Do you want to save your changes before exiting?")
              .set_type(ConfirmationDialog.WARNING)
              .set_ok_text("Save and Exit")
              .set_cancel_text("Exit without Saving")
              .set_parent(parent)
              .build())

    return dialog.exec()


def show_update_confirmation(parent=None) -> tuple:
    """Show an update confirmation dialog"""
    dialog = (ConfirmationDialogBuilder()
              .set_title("Update Available")
              .set_message("A new version is available. Would you like to update now?")
              .set_type(ConfirmationDialog.INFO)
              .set_ok_text("Update Now")
              .set_cancel_text("Later")
              .add_checkbox("Automatically install updates")
              .set_parent(parent)
              .build())

    return dialog.exec()