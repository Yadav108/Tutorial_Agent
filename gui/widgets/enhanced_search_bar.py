# gui/widgets/enhanced_search_bar.py

import logging
from typing import List, Dict, Any, Optional, Callable
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCompleter,
    QPushButton, QFrame, QLabel, QListWidget, QListWidgetItem,
    QMenu, QCheckBox, QComboBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import (
    Qt, pyqtSignal, QTimer, QStringListModel, QAbstractListModel,
    QModelIndex, QRect, QEvent, QPropertyAnimation, QEasingCurve
)
from PyQt6.QtGui import QIcon, QColor, QFont, QPalette

logger = logging.getLogger('TutorialAgent.SearchBar')


class SearchSuggestionModel(QAbstractListModel):
    """Custom model for search suggestions with rich data."""

    def __init__(self):
        super().__init__()
        self.suggestions: List[Dict[str, Any]] = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.suggestions)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self.suggestions):
            return None

        suggestion = self.suggestions[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return suggestion.get('text', '')
        elif role == Qt.ItemDataRole.ToolTipRole:
            return suggestion.get('description', '')
        elif role == Qt.ItemDataRole.UserRole:
            return suggestion

        return None

    def update_suggestions(self, suggestions: List[Dict[str, Any]]):
        """Update suggestions list."""
        self.beginResetModel()
        self.suggestions = suggestions
        self.endResetModel()


class SearchFilterWidget(QFrame):
    """Widget for search filters and options."""

    filters_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.hide()  # Hidden by default

    def setup_ui(self):
        """Setup filter widget UI."""
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
            }
            QCheckBox {
                font-size: 12px;
                spacing: 5px;
            }
            QComboBox {
                font-size: 12px;
                padding: 4px 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                min-width: 100px;
            }
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #495057;
            }
        """)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Content type filters
        content_label = QLabel("Content Type:")
        layout.addWidget(content_label)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(5)

        self.filter_topics = QCheckBox("Topics")
        self.filter_topics.setChecked(True)
        self.filter_examples = QCheckBox("Examples")
        self.filter_examples.setChecked(True)
        self.filter_exercises = QCheckBox("Exercises")
        self.filter_exercises.setChecked(True)

        content_layout.addWidget(self.filter_topics)
        content_layout.addWidget(self.filter_examples)
        content_layout.addWidget(self.filter_exercises)
        layout.addLayout(content_layout)

        # Language filter
        language_label = QLabel("Language:")
        layout.addWidget(language_label)

        self.language_combo = QComboBox()
        self.language_combo.addItem("All Languages", "all")
        layout.addWidget(self.language_combo)

        # Difficulty filter
        difficulty_label = QLabel("Difficulty:")
        layout.addWidget(difficulty_label)

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["All", "Beginner", "Easy", "Medium", "Hard", "Advanced"])
        layout.addWidget(self.difficulty_combo)

        # Connect signals
        self.filter_topics.toggled.connect(self._emit_filters_changed)
        self.filter_examples.toggled.connect(self._emit_filters_changed)
        self.filter_exercises.toggled.connect(self._emit_filters_changed)
        self.language_combo.currentTextChanged.connect(self._emit_filters_changed)
        self.difficulty_combo.currentTextChanged.connect(self._emit_filters_changed)

    def _emit_filters_changed(self):
        """Emit filters changed signal."""
        filters = {
            'topics': self.filter_topics.isChecked(),
            'examples': self.filter_examples.isChecked(),
            'exercises': self.filter_exercises.isChecked(),
            'language': self.language_combo.currentData(),
            'difficulty': self.difficulty_combo.currentText()
        }
        self.filters_changed.emit(filters)

    def update_languages(self, languages: List[str]):
        """Update available languages in combo box."""
        current_data = self.language_combo.currentData()
        self.language_combo.clear()
        self.language_combo.addItem("All Languages", "all")

        for lang in languages:
            self.language_combo.addItem(lang, lang.lower())

        # Restore selection if possible
        index = self.language_combo.findData(current_data)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)

    def get_current_filters(self) -> Dict[str, Any]:
        """Get current filter settings."""
        return {
            'topics': self.filter_topics.isChecked(),
            'examples': self.filter_examples.isChecked(),
            'exercises': self.filter_exercises.isChecked(),
            'language': self.language_combo.currentData(),
            'difficulty': self.difficulty_combo.currentText()
        }


class EnhancedSearchBar(QWidget):
    """Enhanced search bar with auto-complete, filters, and smart suggestions."""

    search_triggered = pyqtSignal(str, dict)  # query, filters
    suggestion_selected = pyqtSignal(dict)  # suggestion data
    search_cleared = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Search state
        self.search_history: List[str] = []
        self.current_suggestions: List[Dict[str, Any]] = []
        self.search_providers: List[Callable] = []

        # Timers
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._perform_search)

        self.suggestion_timer = QTimer()
        self.suggestion_timer.setSingleShot(True)
        self.suggestion_timer.timeout.connect(self._update_suggestions)

        self.setup_ui()
        self.setup_animations()

        logger.debug("Enhanced search bar initialized")

    def setup_ui(self):
        """Setup the enhanced search bar UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Main search container
        search_container = QFrame()
        search_container.setObjectName("searchContainer")
        search_container.setStyleSheet("""
            QFrame#searchContainer {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 20px;
                padding: 2px;
            }
            QFrame#searchContainer:focus-within {
                border-color: #007bff;
            }
        """)

        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(15, 8, 10, 8)
        search_layout.setSpacing(8)

        # Search icon
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #6c757d;
                background: transparent;
                border: none;
            }
        """)
        search_layout.addWidget(search_icon)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tutorials, topics, examples, and exercises...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: none;
                background: transparent;
                font-size: 14px;
                color: #495057;
                padding: 4px 0;
            }
            QLineEdit:focus {
                outline: none;
            }
        """)
        self.search_input.textChanged.connect(self._on_text_changed)
        self.search_input.returnPressed.connect(self._on_return_pressed)
        search_layout.addWidget(self.search_input, 1)

        # Filter button
        self.filter_button = QPushButton("⚙")
        self.filter_button.setToolTip("Search filters")
        self.filter_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 12px;
                padding: 6px;
                font-size: 14px;
                color: #6c757d;
            }
            QPushButton:hover {
                background: #f8f9fa;
                color: #495057;
            }
            QPushButton:pressed {
                background: #e9ecef;
            }
        """)
        self.filter_button.setFixedSize(24, 24)
        self.filter_button.clicked.connect(self._toggle_filters)
        search_layout.addWidget(self.filter_button)

        # Clear button
        self.clear_button = QPushButton("✕")
        self.clear_button.setToolTip("Clear search")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 12px;
                padding: 6px;
                font-size: 12px;
                color: #6c757d;
            }
            QPushButton:hover {
                background: #f8f9fa;
                color: #dc3545;
            }
        """)
        self.clear_button.setFixedSize(24, 24)
        self.clear_button.clicked.connect(self.clear_search)
        self.clear_button.setVisible(False)
        search_layout.addWidget(self.clear_button)

        layout.addWidget(search_container)

        # Filter widget
        self.filter_widget = SearchFilterWidget()
        self.filter_widget.filters_changed.connect(self._on_filters_changed)
        layout.addWidget(self.filter_widget)

        # Setup auto-complete
        self.setup_completer()

    def setup_completer(self):
        """Setup intelligent auto-complete."""
        self.suggestion_model = SearchSuggestionModel()

        self.completer = QCompleter()
        self.completer.setModel(self.suggestion_model)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setMaxVisibleItems(8)

        # Custom styling for completer popup
        self.completer.popup().setStyleSheet("""
            QListView {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 4px;
                font-size: 13px;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
            }
            QListView::item {
                padding: 8px 12px;
                border-radius: 4px;
                margin: 1px;
            }
            QListView::item:hover {
                background-color: #f5f5f5;
            }
        """)

        self.completer.activated.connect(self._on_suggestion_selected)
        self.search_input.setCompleter(self.completer)

    def setup_animations(self):
        """Setup UI animations."""
        # Filter widget slide animation
        self.filter_animation = QPropertyAnimation(self.filter_widget, b"maximumHeight")
        self.filter_animation.setDuration(300)
        self.filter_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def add_search_provider(self, provider: Callable[[str], List[Dict[str, Any]]]):
        """Add a search suggestion provider function."""
        self.search_providers.append(provider)

    def _on_text_changed(self, text: str):
        """Handle search text changes."""
        # Show/hide clear button
        self.clear_button.setVisible(bool(text.strip()))

        # Update suggestions with delay
        self.suggestion_timer.stop()
        if text.strip():
            self.suggestion_timer.start(300)  # 300ms delay for suggestions

        # Trigger search with delay
        self.search_timer.stop()
        if len(text.strip()) >= 2:  # Start searching after 2 characters
            self.search_timer.start(500)  # 500ms delay for search

    def _on_return_pressed(self):
        """Handle return key press."""
        self._perform_search()

    def _perform_search(self):
        """Perform the actual search."""
        query = self.search_input.text().strip()
        if not query:
            return

        # Add to history
        if query not in self.search_history:
            self.search_history.insert(0, query)
            self.search_history = self.search_history[:20]  # Keep last 20 searches

        # Get current filters
        filters = self.filter_widget.get_current_filters()

        # Emit search signal
        self.search_triggered.emit(query, filters)

        logger.debug(f"Search triggered: '{query}' with filters: {filters}")

    def _update_suggestions(self):
        """Update search suggestions from providers."""
        query = self.search_input.text().strip()
        if not query or len(query) < 2:
            return

        suggestions = []

        # Add search history suggestions
        for history_item in self.search_history:
            if query.lower() in history_item.lower() and history_item != query:
                suggestions.append({
                    'text': history_item,
                    'type': 'history',
                    'description': 'Recent search',
                    'icon': '🕒'
                })

        # Get suggestions from providers
        for provider in self.search_providers:
            try:
                provider_suggestions = provider(query)
                suggestions.extend(provider_suggestions)
            except Exception as e:
                logger.error(f"Error getting suggestions from provider: {e}")

        # Limit and update suggestions
        self.current_suggestions = suggestions[:10]
        self.suggestion_model.update_suggestions(self.current_suggestions)

        logger.debug(f"Updated {len(self.current_suggestions)} suggestions for '{query}'")

    def _on_suggestion_selected(self, text: str):
        """Handle suggestion selection."""
        # Find the selected suggestion
        selected_suggestion = None
        for suggestion in self.current_suggestions:
            if suggestion['text'] == text:
                selected_suggestion = suggestion
                break

        if selected_suggestion:
            # Set the text and perform search
            self.search_input.setText(text)
            self._perform_search()

            # Emit suggestion selected signal
            self.suggestion_selected.emit(selected_suggestion)

    def _toggle_filters(self):
        """Toggle filter widget visibility."""
        if self.filter_widget.isVisible():
            self._hide_filters()
        else:
            self._show_filters()

    def _show_filters(self):
        """Show filter widget with animation."""
        self.filter_widget.show()

        # Calculate target height
        self.filter_widget.adjustSize()
        target_height = self.filter_widget.sizeHint().height()

        # Animate
        self.filter_animation.setStartValue(0)
        self.filter_animation.setEndValue(target_height)
        self.filter_animation.start()

        # Update button style
        self.filter_button.setStyleSheet(self.filter_button.styleSheet() + """
            QPushButton {
                background: #e3f2fd;
                color: #1976d2;
            }
        """)

    def _hide_filters(self):
        """Hide filter widget with animation."""
        current_height = self.filter_widget.height()

        self.filter_animation.setStartValue(current_height)
        self.filter_animation.setEndValue(0)
        self.filter_animation.finished.connect(lambda: self.filter_widget.hide())
        self.filter_animation.start()

        # Reset button style
        self.filter_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 12px;
                padding: 6px;
                font-size: 14px;
                color: #6c757d;
            }
            QPushButton:hover {
                background: #f8f9fa;
                color: #495057;
            }
            QPushButton:pressed {
                background: #e9ecef;
            }
        """)

    def _on_filters_changed(self, filters: Dict[str, Any]):
        """Handle filter changes."""
        # Re-trigger search if there's an active query
        if self.search_input.text().strip():
            self._perform_search()

    def clear_search(self):
        """Clear the search input and emit signal."""
        self.search_input.clear()
        self.clear_button.setVisible(False)
        self._hide_filters()
        self.search_cleared.emit()

    def set_query(self, query: str):
        """Set search query programmatically."""
        self.search_input.setText(query)
        self.clear_button.setVisible(bool(query.strip()))

    def get_query(self) -> str:
        """Get current search query."""
        return self.search_input.text().strip()

    def update_available_languages(self, languages: List[str]):
        """Update available languages for filtering."""
        self.filter_widget.update_languages(languages)

    def focus_search(self):
        """Focus the search input."""
        self.search_input.setFocus()
        self.search_input.selectAll()

    def add_to_history(self, query: str):
        """Add query to search history."""
        if query and query not in self.search_history:
            self.search_history.insert(0, query)
            self.search_history = self.search_history[:20]

    def get_search_history(self) -> List[str]:
        """Get search history."""
        return self.search_history.copy()

    def clear_history(self):
        """Clear search history."""
        self.search_history.clear()


# Example search provider function
def create_default_search_provider(content_manager) -> Callable[[str], List[Dict[str, Any]]]:
    """Create a default search provider using the content manager."""

    def search_provider(query: str) -> List[Dict[str, Any]]:
        suggestions = []

        try:
            # Get search results from content manager
            if hasattr(content_manager, 'search'):
                results = content_manager.search(query)

                for result in results[:5]:  # Limit to top 5 results
                    suggestion = {
                        'text': f"{result['topic']} ({result['language']})",
                        'type': result['type'],
                        'description': f"{result['language']} - {result['topic']}",
                        'icon': '📖' if result['type'] == 'topic' else '💡',
                        'data': result
                    }
                    suggestions.append(suggestion)

        except Exception as e:
            logger.error(f"Error in default search provider: {e}")

        return suggestions

    return search_provider