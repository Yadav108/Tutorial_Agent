#gui\widgets\content_viewer.py
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTextEdit, QScrollArea, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt

# Configure logger
logger = logging.getLogger('TutorialAgent')


class ContentViewer(QWidget):
    """Widget for viewing tutorial content."""

    run_example = pyqtSignal(str)  # Signal when user wants to run example code
    start_exercise = pyqtSignal(dict)  # Signal when user starts an exercise

    def __init__(self):
        super().__init__()
        logger.debug("Initializing ContentViewer")
        self._setup_ui()

    def _setup_ui(self):
        """Initialize the user interface."""
        try:
            self.content_layout = QVBoxLayout(self)
            self.content_layout.setContentsMargins(20, 20, 20, 20)
            self.content_layout.setSpacing(20)

            # Initialize UI elements that will be referenced
            self.title_label = QLabel()
            self.title_label.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 24px;
                    font-weight: bold;
                }
            """)
            self.content_layout.addWidget(self.title_label)

            self.description_label = QLabel()
            self.description_label.setWordWrap(True)
            self.description_label.setStyleSheet("""
                QLabel {
                    color: #34495e;
                    font-size: 16px;
                }
            """)
            self.content_layout.addWidget(self.description_label)

            # Create a scroll area for topic sections
            self.scroll = QScrollArea()
            self.scroll.setWidgetResizable(True)
            self.scroll.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background-color: white;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #f1f2f6;
                    width: 10px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #c8cbd0;
                    border-radius: 5px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #a0a4ad;
                }
            """)

            # Create container widget for scroll area
            self.scroll_content = QWidget()
            self.scroll_layout = QVBoxLayout(self.scroll_content)
            self.scroll_layout.setContentsMargins(0, 0, 0, 0)
            self.scroll_layout.setSpacing(20)
            self.scroll.setWidget(self.scroll_content)

            self.content_layout.addWidget(self.scroll)

            logger.debug("ContentViewer UI setup complete")

        except Exception as e:
            logger.error(f"Error setting up ContentViewer UI: {str(e)}", exc_info=True)
            raise

    def clear_content(self):
        """Clear all content from the viewer."""
        try:
            logger.debug("Clearing content viewer")
            # Clear title and description
            self.title_label.setText("")
            self.description_label.setText("")

            # Clear scroll area content
            while self.scroll_layout.count():
                item = self.scroll_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        except Exception as e:
            logger.error(f"Error clearing content: {str(e)}", exc_info=True)

    def show_error_message(self, message: str):
        """Show error message dialog."""
        try:
            logger.debug(f"Showing error message: {message}")
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Icon.Warning)
            error_dialog.setText(message)
            error_dialog.setWindowTitle("Error")
            error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_dialog.exec()
        except Exception as e:
            logger.error(f"Error showing error message: {str(e)}", exc_info=True)

    def load_content(self, content_data: dict):
        """Load content into the viewer."""
        try:
            logger.debug("Loading content into viewer")

            # Clear current content
            self.clear_content()

            if not isinstance(content_data, dict):
                raise ValueError("Content data must be a dictionary")

            # Load title and description
            self.title_label.setText(content_data.get('title', 'Untitled'))
            self.description_label.setText(content_data.get('description', ''))

            # Load topics
            topics = content_data.get('topics', [])
            if not isinstance(topics, list):
                raise ValueError("Topics must be a list")

            for topic_data in topics:
                if not isinstance(topic_data, dict):
                    logger.error(f"Invalid topic data format: {topic_data}")
                    continue

                logger.debug(f"Loading content for topic: {topic_data.get('title', 'Untitled')}")

                # Create topic section
                topic_section = self.create_topic_section(
                    title=topic_data.get('title', 'Untitled'),
                    description=topic_data.get('description', ''),
                    content=topic_data.get('content', ''),
                    examples=topic_data.get('examples', []),
                    exercises=topic_data.get('exercises', [])
                )
                self.scroll_layout.addWidget(topic_section)

            logger.debug("Content loaded successfully")

        except Exception as e:
            logger.error(f"Error loading content: {str(e)}", exc_info=True)
            self.show_error_message("Failed to load content")

    def create_topic_section(self, title: str, description: str, content: str,
                             examples: list, exercises: list) -> QWidget:
        """Create a widget containing a topic's content."""
        try:
            section = QWidget()
            layout = QVBoxLayout(section)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)

            # Topic title
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 20px;
                    font-weight: bold;
                }
            """)
            layout.addWidget(title_label)

            # Topic description
            if description:
                desc_label = QLabel(description)
                desc_label.setWordWrap(True)
                desc_label.setStyleSheet("""
                    QLabel {
                        color: #34495e;
                        font-size: 14px;
                    }
                """)
                layout.addWidget(desc_label)

            # Topic content (using Markdown)
            if content:
                content_widget = QTextEdit()
                content_widget.setReadOnly(True)
                content_widget.setMarkdown(content)
                content_widget.setStyleSheet("""
                    QTextEdit {
                        border: none;
                        background-color: #f8f9fa;
                        padding: 10px;
                        border-radius: 5px;
                    }
                """)
                content_widget.setMinimumHeight(100)
                layout.addWidget(content_widget)

            # Examples section
            if examples:
                examples_widget = self._create_examples_section(examples)
                layout.addWidget(examples_widget)

            # Exercises section
            if exercises:
                exercises_widget = self._create_exercises_section(exercises)
                layout.addWidget(exercises_widget)

            # Add some spacing at the bottom
            layout.addSpacing(20)

            return section

        except Exception as e:
            logger.error(f"Error creating topic section: {str(e)}", exc_info=True)
            return QWidget()

    def _create_examples_section(self, examples: list) -> QWidget:
        """Create a widget containing example code snippets."""
        try:
            section = QWidget()
            layout = QVBoxLayout(section)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(15)

            title = QLabel("Examples")
            title.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 18px;
                    font-weight: bold;
                }
            """)
            layout.addWidget(title)

            for example in examples:
                if not isinstance(example, dict):
                    continue

                frame = QFrame()
                frame.setFrameStyle(QFrame.Shape.Box)
                frame.setStyleSheet("""
                    QFrame {
                        border: 1px solid #dcdde1;
                        border-radius: 5px;
                        background-color: white;
                        padding: 10px;
                    }
                """)

                frame_layout = QVBoxLayout(frame)
                frame_layout.setSpacing(10)

                # Example title
                ex_title = QLabel(example.get('title', 'Untitled Example'))
                ex_title.setStyleSheet("font-weight: bold; color: #2c3e50;")
                frame_layout.addWidget(ex_title)

                # Example code
                if 'code' in example:
                    code_edit = QTextEdit()
                    code_edit.setReadOnly(True)
                    code_edit.setPlainText(example['code'])
                    code_edit.setStyleSheet("""
                        QTextEdit {
                            font-family: monospace;
                            background-color: #f8f9fa;
                            border: none;
                            border-radius: 3px;
                        }
                    """)
                    code_edit.setMinimumHeight(100)
                    frame_layout.addWidget(code_edit)

                    # Run button
                    run_btn = QPushButton("Run Example")
                    run_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #2ecc71;
                            color: white;
                            border: none;
                            padding: 5px 15px;
                            border-radius: 3px;
                        }
                        QPushButton:hover {
                            background-color: #27ae60;
                        }
                    """)
                    run_btn.clicked.connect(lambda checked, code=example['code']:
                                            self.run_example.emit(code))
                    frame_layout.addWidget(run_btn, alignment=Qt.AlignmentFlag.AlignRight)

                # Example explanation
                if 'explanation' in example:
                    explanation = QLabel(example['explanation'])
                    explanation.setWordWrap(True)
                    explanation.setStyleSheet("color: #34495e;")
                    frame_layout.addWidget(explanation)

                layout.addWidget(frame)

            return section

        except Exception as e:
            logger.error(f"Error creating examples section: {str(e)}", exc_info=True)
            return QWidget()

    def _create_exercises_section(self, exercises: list) -> QWidget:
        """Create a widget containing coding exercises."""
        try:
            section = QWidget()
            layout = QVBoxLayout(section)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(15)

            title = QLabel("Exercises")
            title.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 18px;
                    font-weight: bold;
                }
            """)
            layout.addWidget(title)

            for exercise in exercises:
                if not isinstance(exercise, dict):
                    continue

                frame = QFrame()
                frame.setFrameStyle(QFrame.Shape.Box)
                frame.setStyleSheet("""
                    QFrame {
                        border: 1px solid #dcdde1;
                        border-radius: 5px;
                        background-color: white;
                        padding: 10px;
                    }
                """)

                frame_layout = QVBoxLayout(frame)
                frame_layout.setSpacing(10)

                # Exercise title and difficulty
                header_layout = QHBoxLayout()
                ex_title = QLabel(exercise.get('title', 'Untitled Exercise'))
                ex_title.setStyleSheet("font-weight: bold; color: #2c3e50;")
                header_layout.addWidget(ex_title)

                if 'difficulty' in exercise:
                    difficulty = QLabel(exercise['difficulty'])
                    difficulty.setStyleSheet("""
                        padding: 2px 8px;
                        background-color: #3498db;
                        color: white;
                        border-radius: 10px;
                    """)
                    header_layout.addWidget(difficulty)

                header_layout.addStretch()
                frame_layout.addLayout(header_layout)

                # Exercise description
                if 'description' in exercise:
                    description = QLabel(exercise['description'])
                    description.setWordWrap(True)
                    description.setStyleSheet("color: #34495e;")
                    frame_layout.addWidget(description)

                # Start button
                start_btn = QPushButton("Start Exercise")
                start_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        padding: 5px 15px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                start_btn.clicked.connect(lambda checked, ex=exercise:
                                          self.start_exercise.emit(ex))
                frame_layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignRight)

                layout.addWidget(frame)

            return section

        except Exception as e:
            logger.error(f"Error creating exercises section: {str(e)}", exc_info=True)
            return QWidget()