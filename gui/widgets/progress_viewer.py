# gui/widgets/progress_viewer.py

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar,
    QScrollArea, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt

logger = logging.getLogger('TutorialAgent')


class TopicProgressBar(QFrame):
    """Widget showing progress for a single topic."""

    def __init__(self, topic: str, progress: int = 0):
        super().__init__()
        self.topic = topic
        self.setup_ui(progress)

    def setup_ui(self, progress: int):
        self.setStyleSheet("""
            TopicProgressBar {
                background-color: white;
                border-radius: 8px;
                padding: 8px;
                margin: 4px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(8, 8, 8, 8)

        # Topic name with progress percentage
        header_layout = QHBoxLayout()

        name_label = QLabel(self.topic)
        name_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 13px;
            }
        """)
        header_layout.addWidget(name_label)

        percent_label = QLabel(f"{progress}%")
        percent_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 12px;
            }
        """)
        header_layout.addWidget(percent_label, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(header_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #ecf0f1;
                border-radius: 4px;
                text-align: center;
                min-height: 6px;
                max-height: 6px;
            }
            QProgressBar::chunk {
                border-radius: 4px;
                background-color: #2ecc71;
            }
        """)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(progress)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

    def update_progress(self, value: int):
        """Update the progress value."""
        self.progress_bar.setValue(value)
        self.findChild(QLabel, "", options=Qt.FindChildOption.FindChildrenRecursively)[-1].setText(f"{value}%")


class ProgressViewer(QWidget):
    """Widget for viewing learning progress."""

    def __init__(self):
        super().__init__()
        logger.debug("Initializing ProgressViewer")
        self.topic_bars = {}
        self.current_language = None
        self.setup_ui()

    def setup_ui(self):
        try:
            layout = QVBoxLayout(self)
            layout.setSpacing(8)
            layout.setContentsMargins(0, 0, 0, 0)

            # Title section
            title_section = QWidget()
            title_section.setStyleSheet("""
                QWidget {
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    padding: 12px;
                }
            """)
            title_layout = QVBoxLayout(title_section)

            title = QLabel("Learning Progress")
            title.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
            title_layout.addWidget(title)

            # Overall progress
            self.overall_progress = QProgressBar()
            self.overall_progress.setStyleSheet("""
                QProgressBar {
                    border: none;
                    background-color: #ecf0f1;
                    border-radius: 7px;
                    text-align: center;
                    min-height: 14px;
                }
                QProgressBar::chunk {
                    border-radius: 7px;
                    background-color: #2ecc71;
                }
            """)
            self.overall_progress.setRange(0, 100)
            self.overall_progress.setValue(0)
            title_layout.addWidget(self.overall_progress)

            layout.addWidget(title_section)

            # Scroll area for topic progress bars
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background-color: transparent;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #f1f2f6;
                    width: 8px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #c8cbd0;
                    border-radius: 4px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #a0a4ad;
                }
            """)

            # Container for progress bars
            self.progress_container = QWidget()
            self.progress_layout = QVBoxLayout(self.progress_container)
            self.progress_layout.setSpacing(4)
            self.progress_layout.setContentsMargins(0, 0, 0, 0)
            scroll.setWidget(self.progress_container)

            layout.addWidget(scroll)

        except Exception as e:
            logger.error(f"Error setting up ProgressViewer: {str(e)}", exc_info=True)
            raise

    def update_progress(self, language: str, topic_progress: dict):
        """Update progress display for selected language.

        Args:
            language: Name of the programming language
            topic_progress: Dictionary mapping topic names to progress percentages
        """
        try:
            logger.debug(f"Updating progress for {language}")
            self.current_language = language

            # Clear existing progress bars
            self._clear_progress_bars()

            # Update overall progress
            total_progress = sum(topic_progress.values()) / len(topic_progress) if topic_progress else 0
            self.overall_progress.setValue(int(total_progress))

            # Create progress bars for each topic
            for topic, progress in topic_progress.items():
                try:
                    topic_bar = TopicProgressBar(topic, progress)
                    self.progress_layout.addWidget(topic_bar)
                    self.topic_bars[topic] = topic_bar
                except Exception as e:
                    logger.error(f"Error creating progress bar for {topic}: {str(e)}")

            # Add stretch at the end
            self.progress_layout.addStretch()

        except Exception as e:
            logger.error(f"Error updating progress: {str(e)}", exc_info=True)

    def _clear_progress_bars(self):
        """Clear all progress bars."""
        try:
            while self.progress_layout.count():
                item = self.progress_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.topic_bars.clear()
        except Exception as e:
            logger.error(f"Error clearing progress bars: {str(e)}", exc_info=True)

    def _get_sample_progress_data(self, language: str) -> dict:
        """Get sample progress data for demonstration."""
        # This would be replaced with actual data from your content management system
        return {
            "Basic Syntax": 100,
            "Variables & Data Types": 80,
            "Control Flow": 60,
            "Functions": 40,
            "Object-Oriented Programming": 20,
            "File Handling": 0,
            "Error Handling": 0,
            "Libraries & Packages": 0,
            "Testing & Debugging": 0
        }