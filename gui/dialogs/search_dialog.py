from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTreeWidget, QTreeWidgetItem,
    QLabel, QFrame, QComboBox, QCheckBox,
    QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont
from services.content_service import ContentService


class SearchDialog(QDialog):
    def __init__(self, content_service: ContentService, parent=None):
        super().__init__(parent)
        self.content_service = content_service
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Search Tutorial Content")
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QFrame {
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Search header
        self.setup_search_header(layout)

        # Search filters
        self.setup_search_filters(layout)

        # Results area
        self.setup_results_area(layout)

        # Buttons
        self.setup_buttons(layout)

    def setup_search_header(self, layout):
        """Setup search input area"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                padding: 15px;
                background: #3498db;
                border: none;
            }
        """)
        header_layout = QVBoxLayout(header_frame)

        # Title
        title = QLabel("Search Tutorials")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)

        # Search input
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for topics, concepts, or keywords...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: none;
                border-radius: 4px;
                background: white;
                font-size: 14px;
            }
        """)
        self.search_input.textChanged.connect(self.on_search_text_changed)
        search_layout.addWidget(self.search_input)

        search_button = QPushButton("Search")
        search_button.setIcon(QIcon("assets/images/search.png"))
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        search_button.clicked.connect(self.perform_search)
        search_layout.addWidget(search_button)

        header_layout.addLayout(search_layout)
        layout.addWidget(header_frame)

    def setup_search_filters(self, layout):
        """Setup search filter options"""
        filters_frame = QFrame()
        filters_frame.setStyleSheet("""
            QFrame {
                padding: 10px;
            }
        """)
        filters_layout = QHBoxLayout(filters_frame)

        # Language filter
        lang_layout = QVBoxLayout()
        lang_label = QLabel("Language:")
        lang_label.setStyleSheet("color: #2c3e50;")
        lang_layout.addWidget(lang_label)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["All Languages", "Python", "C++", "C#", "Java"])
        self.language_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
        lang_layout.addWidget(self.language_combo)
        filters_layout.addLayout(lang_layout)

        # Difficulty filter
        difficulty_layout = QVBoxLayout()
        diff_label = QLabel("Difficulty:")
        diff_label.setStyleSheet("color: #2c3e50;")
        difficulty_layout.addWidget(diff_label)

        self.difficulty_group = QButtonGroup()
        diff_frame = QFrame()
        diff_box_layout = QHBoxLayout(diff_frame)

        difficulties = ["All", "Beginner", "Intermediate", "Advanced"]
        for i, diff in enumerate(difficulties):
            radio = QRadioButton(diff)
            radio.setStyleSheet("color: #2c3e50;")
            self.difficulty_group.addButton(radio, i)
            diff_box_layout.addWidget(radio)

        self.difficulty_group.button(0).setChecked(True)
        difficulty_layout.addWidget(diff_frame)
        filters_layout.addLayout(difficulty_layout)

        # Content type filter
        type_layout = QVBoxLayout()
        type_label = QLabel("Content Type:")
        type_label.setStyleSheet("color: #2c3e50;")
        type_layout.addWidget(type_label)

        self.type_checks = []
        type_frame = QFrame()
        type_box_layout = QHBoxLayout(type_frame)

        types = ["Tutorials", "Exercises", "Projects", "Quizzes"]
        for type_name in types:
            check = QCheckBox(type_name)
            check.setStyleSheet("color: #2c3e50;")
            check.setChecked(True)
            self.type_checks.append(check)
            type_box_layout.addWidget(check)

        type_layout.addWidget(type_frame)
        filters_layout.addLayout(type_layout)

        layout.addWidget(filters_frame)

    def setup_results_area(self, layout):
        """Setup search results area"""
        # Results count
        self.results_count = QLabel("0 results found")
        self.results_count.setStyleSheet("color: #7f8c8d; padding: 5px;")
        layout.addWidget(self.results_count)

        # Results tree
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["Title", "Type", "Language", "Difficulty"])
        self.results_tree.setColumnWidth(0, 300)
        self.results_tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #dee2e6;
                background: white;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background: #3498db;
                color: white;
            }
        """)
        self.results_tree.itemDoubleClicked.connect(self.on_result_selected)
        layout.addWidget(self.results_tree)

    def setup_buttons(self, layout):
        """Setup dialog buttons"""
        button_layout = QHBoxLayout()

        # Clear filters button
        clear_button = QPushButton("Clear Filters")
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        clear_button.clicked.connect(self.clear_filters)
        button_layout.addWidget(clear_button)

        button_layout.addStretch()

        # Close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

    def on_search_text_changed(self, text):
        """Handle search text changes"""
        # Reset the timer to prevent immediate search
        self.search_timer.stop()
        self.search_timer.start(300)  # Wait 300ms before searching

    def perform_search(self):
        """Execute the search"""
        search_text = self.search_input.text()
        language = self.language_combo.currentText()
        difficulty = self.difficulty_group.checkedButton().text()
        content_types = [check.text() for check in self.type_checks if check.isChecked()]

        # Clear previous results
        self.results_tree.clear()

        if not search_text:
            self.results_count.setText("Enter search terms to begin")
            return

        # Get search results
        results = self.content_service.search_content(
            query=search_text,
            language=None if language == "All Languages" else language.lower(),
            difficulty=None if difficulty == "All" else difficulty.lower()
        )

        # Filter by content type
        results = [r for r in results if r['type'] in content_types]

        # Update results count
        self.results_count.setText(f"{len(results)} results found")

        # Populate results tree
        for result in results:
            item = QTreeWidgetItem([
                result['title'],
                result['type'],
                result['language'].title(),
                result.get('difficulty', 'N/A')
            ])
            item.setData(0, Qt.ItemDataRole.UserRole, result)
            self.results_tree.addTopLevelItem(item)

    def on_result_selected(self, item, column):
        """Handle result selection"""
        result_data = item.data(0, Qt.ItemDataRole.UserRole)
        self.accept()
        # Emit signal or callback to open selected content
        self.parent().load_content(result_data)

    def clear_filters(self):
        """Reset all filters to default values"""
        self.language_combo.setCurrentIndex(0)
        self.difficulty_group.button(0).setChecked(True)
        for check in self.type_checks:
            check.setChecked(True)
        self.perform_search()

    def get_search_term(self) -> str:
        """Get the current search term"""
        return self.search_input.text()