# File: Tutorial_Agent/gui/helpers/style_helpers.py

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPalette, QColor
import logging

logger = logging.getLogger(__name__)


def set_dark_theme(widget: QWidget) -> None:
    """Apply dark theme to widget."""
    try:
        dark_palette = QPalette()

        # Set colors for different widget states
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

        widget.setPalette(dark_palette)

        # Apply dark theme stylesheet
        widget.setStyleSheet("""
            QWidget {
                background-color: #1e272e;
                color: #ffffff;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                background-color: #2c3e50;
                color: white;
                border: 1px solid #34495e;
                padding: 5px;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #2c3e50;
                color: white;
                border: 1px solid #34495e;
                border-radius: 4px;
            }
            QTabWidget::pane {
                border: 1px solid #34495e;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #2c3e50;
                color: white;
                padding: 8px 16px;
                border: 1px solid #34495e;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
            }
        """)

    except Exception as e:
        logger.error(f"Error setting dark theme: {str(e)}")
        raise


def set_light_theme(widget: QWidget) -> None:
    """Apply light theme to widget."""
    try:
        light_palette = QPalette()

        # Set colors for different widget states
        light_palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(233, 233, 233))
        light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
        light_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

        widget.setPalette(light_palette)

        # Apply light theme stylesheet
        widget.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                padding: 5px;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                color: #2c3e50;
                padding: 8px 16px;
                border: 1px solid #bdc3c7;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
        """)

    except Exception as e:
        logger.error(f"Error setting light theme: {str(e)}")
        raise