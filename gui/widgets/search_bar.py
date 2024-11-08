# gui/widgets/search_bar.py

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit,
    QCompleter, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
import logging

logger = logging.getLogger('TutorialAgent')


class SearchBar(QWidget):
    """Search bar widget with auto-complete."""

    search_triggered = pyqtSignal(str)  # Signal emitted when search is triggered

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Initialize the search bar UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tutorials, topics, or concepts...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 1px solid #dcdde1;
                border-radius: 20px;
                background: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        self.search_input.returnPressed.connect(self.trigger_search)
        layout.addWidget(self.search_input)

        # Search button
        self.search_button = QPushButton()
        self.search_button.setIcon(QIcon("assets/icons/search.png"))
        self.search_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background: #f5f6fa;
                border-radius: 15px;
            }
        """)
        self.search_button.clicked.connect(self.trigger_search)
        layout.addWidget(self.search_button)

        # Setup auto-complete
        self.setup_autocomplete()

    def setup_autocomplete(self):
        """Setup auto-complete functionality."""
        completer = QCompleter(self._get_suggestions())
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.search_input.setCompleter(completer)

    def trigger_search(self):
        """Emit search signal with current query."""
        query = self.search_input.text().strip()
        if query:
            self.search_triggered.emit(query)

    def clear_search(self):
        """Clear the search input."""
        self.search_input.clear()

    def _get_suggestions(self) -> list:
        """Get search suggestions."""
        return [
            "Python basics",
            "Python functions",
            "Python classes",
            "JavaScript variables",
            "JavaScript functions",
            "C# syntax",
            "C# classes",
            "Java basics",
            "Java OOP",
            "Control flow",
            "Data structures",
            "Error handling",
            "File operations",
            "Testing",
            "Debugging"
        ]