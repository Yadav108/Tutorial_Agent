# gui/widgets/language_card.py

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QProgressBar,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QIcon
import logging

logger = logging.getLogger('TutorialAgent')


class LanguageCard(QFrame):
    """Custom card widget for language selection."""

    clicked = pyqtSignal(str)  # Signal emitted when card is clicked

    def __init__(self, language: str, description: str, icon: str = None, color: str = "#3498db"):
        super().__init__()
        try:
            logger.debug(f"Creating LanguageCard for {language}")
            self.language = language
            self.icon_path = icon
            self.color = color
            self.is_selected = False
            self.setup_ui(description)
        except Exception as e:
            logger.error(f"Error initializing LanguageCard: {str(e)}", exc_info=True)
            raise

    def setup_ui(self, description: str):
        """Initialize the card's user interface."""
        try:
            # Set frame properties
            self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
            self.setStyleSheet(self._get_style())

            # Add shadow effect
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(0, 0, 0, 50))
            shadow.setOffset(0, 2)
            self.setGraphicsEffect(shadow)

            # Main layout
            layout = QVBoxLayout(self)
            layout.setSpacing(10)
            layout.setContentsMargins(20, 20, 20, 20)

            # Icon container
            icon_container = QFrame()
            icon_container.setFixedSize(50, 50)
            icon_container.setStyleSheet(f"""
                background-color: {self.color};
                border-radius: 12px;
                padding: 5px;
            """)
            icon_layout = QVBoxLayout(icon_container)
            icon_layout.setContentsMargins(5, 5, 5, 5)

            # Icon or letter
            if self.icon_path:
                icon_label = QLabel()
                icon = QIcon(self.icon_path)
                if not icon.isNull():
                    pixmap = icon.pixmap(32, 32)
                    icon_label.setPixmap(pixmap)
                else:
                    logger.warning(f"Could not load icon from {self.icon_path}")
                    icon_label.setText(self.language[0].upper())
                    icon_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
            else:
                icon_label = QLabel(self.language[0].upper())
                icon_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")

            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_layout.addWidget(icon_label)
            layout.addWidget(icon_container, alignment=Qt.AlignmentFlag.AlignCenter)

            # Language name
            name_label = QLabel(self.language)
            name_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(name_label)

            # Description
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setStyleSheet("color: #7f8c8d; font-size: 13px;")
            layout.addWidget(desc_label)

            # Progress bar
            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    background-color: #ecf0f1;
                    border-radius: 7px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #2ecc71;
                    border-radius: 7px;
                }
            """)
            layout.addWidget(self.progress_bar)

            # Set fixed size
            self.setFixedSize(280, 200)

        except Exception as e:
            logger.error(f"Error setting up LanguageCard UI: {str(e)}", exc_info=True)
            raise

    def _get_style(self) -> str:
        """Get the card's style based on selection state."""
        return f"""
            QFrame {{
                background-color: {'#f0f6fc' if self.is_selected else 'white'};
                border: {f'2px solid {self.color}' if self.is_selected else 'none'};
                border-radius: 15px;
                margin: 8px;
            }}
            QFrame:hover {{
                background-color: #f8f9fa;
                border: 2px solid {self.color};
            }}
        """

    def setSelected(self, selected: bool):
        """Set the card's selection state."""
        try:
            logger.debug(f"Setting {self.language} card selection state to {selected}")
            self.is_selected = selected
            self.setStyleSheet(self._get_style())
        except Exception as e:
            logger.error(f"Error setting card selection: {str(e)}", exc_info=True)

    def set_progress(self, value: int):
        """Update the progress bar value."""
        try:
            logger.debug(f"Setting {self.language} card progress to {value}")
            self.progress_bar.setValue(value)
        except Exception as e:
            logger.error(f"Error setting progress: {str(e)}", exc_info=True)

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                logger.debug(f"Language card clicked: {self.language}")
                self.clicked.emit(self.language)
            super().mousePressEvent(event)
        except Exception as e:
            logger.error(f"Error handling mouse press: {str(e)}", exc_info=True)

    def enterEvent(self, event):
        """Handle mouse enter events."""
        try:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            super().enterEvent(event)
        except Exception as e:
            logger.error(f"Error handling enter event: {str(e)}", exc_info=True)

    def leaveEvent(self, event):
        """Handle mouse leave events."""
        try:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            super().leaveEvent(event)
        except Exception as e:
            logger.error(f"Error handling leave event: {str(e)}", exc_info=True)