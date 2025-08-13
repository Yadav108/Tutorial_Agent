# gui/widgets/enhanced_progress_viewer.py

import logging
from typing import Dict, Optional, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar,
    QScrollArea, QFrame, QHBoxLayout, QGraphicsDropShadowEffect,
    QSizePolicy, QPushButton
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QTimer, QRect
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QLinearGradient

logger = logging.getLogger('TutorialAgent.ProgressViewer')


class AnimatedProgressBar(QProgressBar):
    """Custom progress bar with smooth animations."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(800)  # 800ms animation
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #e9ecef;
                border-radius: 8px;
                text-align: center;
                font-size: 11px;
                font-weight: bold;
                color: #495057;
                min-height: 16px;
                max-height: 16px;
            }
            QProgressBar::chunk {
                border-radius: 8px;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #28a745, stop: 0.5 #20c997, stop: 1 #17a2b8);
            }
        """)

    def setValueAnimated(self, value: int):
        """Set value with smooth animation."""
        self.animation.setStartValue(self.value())
        self.animation.setEndValue(value)
        self.animation.start()


class TopicProgressCard(QFrame):
    """Enhanced topic progress card with better visual design."""

    topic_clicked = pyqtSignal(str)

    def __init__(self, topic: str, progress: int = 0, difficulty: str = "Medium"):
        super().__init__()
        self.topic = topic
        self.progress = progress
        self.difficulty = difficulty
        self.setup_ui()
        self.setup_effects()

    def setup_ui(self):
        """Setup the card UI with enhanced styling."""
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("""
            TopicProgressCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
                margin: 2px;
            }
            TopicProgressCard:hover {
                border: 1px solid #007bff;
                background-color: #f8f9fa;
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 10, 12, 10)

        # Header with topic name and difficulty
        header_layout = QHBoxLayout()

        # Topic name
        self.name_label = QLabel(self.topic)
        self.name_label.setStyleSheet("""
            QLabel {
                color: #212529;
                font-weight: bold;
                font-size: 13px;
                background: transparent;
            }
        """)
        self.name_label.setWordWrap(True)
        header_layout.addWidget(self.name_label, 1)

        # Difficulty badge
        self.difficulty_badge = QLabel(self.difficulty)
        self.difficulty_badge.setStyleSheet(self._get_difficulty_style())
        self.difficulty_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.difficulty_badge.setFixedSize(60, 20)
        header_layout.addWidget(self.difficulty_badge)

        layout.addLayout(header_layout)

        # Progress section
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(8)

        # Progress bar
        self.progress_bar = AnimatedProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(self.progress)
        progress_layout.addWidget(self.progress_bar, 1)

        # Progress percentage
        self.percent_label = QLabel(f"{self.progress}%")
        self.percent_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
                min-width: 35px;
            }
        """)
        self.percent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.percent_label)

        layout.addLayout(progress_layout)

        # Status indicator
        self.status_label = QLabel(self._get_status_text())
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {self._get_status_color()};
                font-size: 11px;
                font-style: italic;
                background: transparent;
            }}
        """)
        layout.addWidget(self.status_label)

    def setup_effects(self):
        """Setup visual effects for the card."""
        # Drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def _get_difficulty_style(self) -> str:
        """Get styling for difficulty badge."""
        colors = {
            "Beginner": "#28a745",
            "Easy": "#28a745",
            "Medium": "#ffc107",
            "Hard": "#dc3545",
            "Advanced": "#6f42c1"
        }
        color = colors.get(self.difficulty, "#6c757d")
        text_color = "white" if self.difficulty in ["Hard", "Advanced"] else "#212529"

        return f"""
            QLabel {{
                background-color: {color};
                color: {text_color};
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 10px;
                font-weight: bold;
            }}
        """

    def _get_status_text(self) -> str:
        """Get status text based on progress."""
        if self.progress == 0:
            return "Not started"
        elif self.progress < 50:
            return "In progress"
        elif self.progress < 100:
            return "Almost complete"
        else:
            return "Completed ✓"

    def _get_status_color(self) -> str:
        """Get status color based on progress."""
        if self.progress == 0:
            return "#6c757d"
        elif self.progress < 50:
            return "#007bff"
        elif self.progress < 100:
            return "#fd7e14"
        else:
            return "#28a745"

    def update_progress(self, value: int):
        """Update progress with animation."""
        self.progress = value
        self.progress_bar.setValueAnimated(value)

        # Update percentage label with animation delay
        QTimer.singleShot(400, lambda: self.percent_label.setText(f"{value}%"))

        # Update status
        QTimer.singleShot(500, self._update_status)

    def _update_status(self):
        """Update status text and color."""
        self.status_label.setText(self._get_status_text())
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {self._get_status_color()};
                font-size: 11px;
                font-style: italic;
                background: transparent;
            }}
        """)

    def mousePressEvent(self, event):
        """Handle mouse press to emit topic clicked signal."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.topic_clicked.emit(self.topic)
        super().mousePressEvent(event)


class ProgressStatistics(QFrame):
    """Widget showing overall progress statistics."""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup statistics UI."""
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("""
            ProgressStatistics {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #667eea, stop: 1 #764ba2);
                border-radius: 12px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel("Learning Statistics")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
        """)
        layout.addWidget(title)

        # Statistics grid
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        # Completed topics
        self.completed_label = self._create_stat_label("0", "Completed")
        stats_layout.addWidget(self.completed_label)

        # In progress
        self.in_progress_label = self._create_stat_label("0", "In Progress")
        stats_layout.addWidget(self.in_progress_label)

        # Total topics
        self.total_label = self._create_stat_label("0", "Total Topics")
        stats_layout.addWidget(self.total_label)

        layout.addLayout(stats_layout)

        # Overall progress bar
        self.overall_progress = AnimatedProgressBar()
        self.overall_progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                text-align: center;
                font-size: 12px;
                font-weight: bold;
                color: white;
                min-height: 16px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #ff6b6b, stop: 1 #ffa726);
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.overall_progress)

    def _create_stat_label(self, value: str, description: str) -> QWidget:
        """Create a statistic label widget."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
            }
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)

        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 11px;
                background: transparent;
            }
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Store value label for updates
        container.value_label = value_label

        return container

    def update_statistics(self, completed: int, in_progress: int, total: int):
        """Update statistics with animation."""
        self.completed_label.value_label.setText(str(completed))
        self.in_progress_label.value_label.setText(str(in_progress))
        self.total_label.value_label.setText(str(total))

        # Update overall progress
        overall_percentage = (completed / total * 100) if total > 0 else 0
        self.overall_progress.setValueAnimated(int(overall_percentage))


class EnhancedProgressViewer(QWidget):
    """Enhanced progress viewer with animations and better UX."""

    topic_selected = pyqtSignal(str)  # Signal when user clicks on a topic

    def __init__(self):
        super().__init__()
        logger.debug("Initializing EnhancedProgressViewer")

        self.topic_cards: Dict[str, TopicProgressCard] = {}
        self.current_language: Optional[str] = None
        self.animation_queue: List[tuple] = []  # Queue for staggered animations

        self.setup_ui()
        self.setup_animation_timer()

    def setup_ui(self):
        """Setup the enhanced UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        # Statistics section
        self.statistics = ProgressStatistics()
        layout.addWidget(self.statistics)

        # Progress section header
        header_layout = QHBoxLayout()

        progress_title = QLabel("Topic Progress")
        progress_title.setStyleSheet("""
            QLabel {
                color: #212529;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(progress_title)

        # Filter/sort button (placeholder for future enhancement)
        self.filter_btn = QPushButton("📊")
        self.filter_btn.setStyleSheet("""
            QPushButton {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #e9ecef;
            }
        """)
        self.filter_btn.setFixedSize(30, 30)
        self.filter_btn.setToolTip("Progress options")
        header_layout.addWidget(self.filter_btn)

        layout.addLayout(header_layout)

        # Scroll area for topic cards
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarNever)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f3f4;
                width: 10px;
                border-radius: 5px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #c1c7cd;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a6ad;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

        # Container for topic cards
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(8)
        self.scroll_layout.setContentsMargins(0, 0, 10, 0)  # Right margin for scrollbar
        self.scroll.setWidget(self.scroll_widget)

        layout.addWidget(self.scroll)

        # Add empty state message (hidden by default)
        self.empty_state = QLabel("Select a language to view progress")
        self.empty_state.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 14px;
                font-style: italic;
                padding: 40px;
                text-align: center;
            }
        """)
        self.empty_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_state.setVisible(False)
        layout.addWidget(self.empty_state)

    def setup_animation_timer(self):
        """Setup timer for staggered animations."""
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._process_animation_queue)
        self.animation_timer.setSingleShot(True)

    def update_progress(self, language: str, topic_progress: Dict[str, int]):
        """Update progress with enhanced animations and statistics."""
        try:
            logger.debug(f"Updating enhanced progress for {language}")
            self.current_language = language

            # Hide empty state
            self.empty_state.setVisible(False)

            # Clear existing cards
            self._clear_progress_cards()

            # Calculate statistics
            completed = sum(1 for p in topic_progress.values() if p >= 100)
            in_progress = sum(1 for p in topic_progress.values() if 0 < p < 100)
            total = len(topic_progress)

            # Update statistics with animation
            self.statistics.update_statistics(completed, in_progress, total)

            # Create new topic cards with staggered animation
            self._create_animated_topic_cards(topic_progress)

            logger.debug(f"Progress update complete: {completed}/{total} topics completed")

        except Exception as e:
            logger.error(f"Error updating enhanced progress: {e}", exc_info=True)
            self._show_error_state(str(e))

    def _clear_progress_cards(self):
        """Clear all progress cards with fade out animation."""
        for card in self.topic_cards.values():
            card.deleteLater()
        self.topic_cards.clear()

        # Clear layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _create_animated_topic_cards(self, topic_progress: Dict[str, int]):
        """Create topic cards with staggered entrance animations."""
        self.animation_queue.clear()

        # Determine difficulty based on topic name (you can enhance this logic)
        difficulty_map = {
            "basics": "Beginner",
            "basic": "Beginner",
            "introduction": "Beginner",
            "advanced": "Advanced",
            "expert": "Advanced",
            "oop": "Medium",
            "object": "Medium",
            "class": "Medium",
            "function": "Easy",
            "variable": "Easy",
            "control": "Medium",
            "loop": "Medium",
            "file": "Medium",
            "error": "Hard",
            "exception": "Hard",
            "database": "Hard",
            "network": "Hard",
            "async": "Advanced",
            "thread": "Advanced"
        }

        for i, (topic, progress) in enumerate(topic_progress.items()):
            # Determine difficulty
            topic_lower = topic.lower()
            difficulty = "Medium"  # default
            for keyword, diff in difficulty_map.items():
                if keyword in topic_lower:
                    difficulty = diff
                    break

            # Create card
            card = TopicProgressCard(topic, 0, difficulty)  # Start with 0 for animation
            card.topic_clicked.connect(self.topic_selected.emit)

            # Add to layout
            self.scroll_layout.addWidget(card)
            self.topic_cards[topic] = card

            # Queue animation with delay
            delay = i * 50  # 50ms delay between cards
            self.animation_queue.append((card, progress, delay))

        # Add stretch
        self.scroll_layout.addStretch()

        # Start animations
        if self.animation_queue:
            self._process_animation_queue()

    def _process_animation_queue(self):
        """Process the animation queue for staggered effects."""
        if not self.animation_queue:
            return

        card, progress, delay = self.animation_queue.pop(0)

        # Schedule the animation
        QTimer.singleShot(delay, lambda: card.update_progress(progress))

        # Continue with next animation
        if self.animation_queue:
            QTimer.singleShot(50, self._process_animation_queue)

    def _show_error_state(self, error: str):
        """Show error state when progress loading fails."""
        self.empty_state.setText(f"Error loading progress:\n{error}")
        self.empty_state.setStyleSheet("""
            QLabel {
                color: #dc3545;
                font-size: 14px;
                padding: 40px;
                text-align: center;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 8px;
                margin: 20px;
            }
        """)
        self.empty_state.setVisible(True)

    def show_empty_state(self):
        """Show empty state when no language is selected."""
        self.empty_state.setText("Select a language to view your progress")
        self.empty_state.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 14px;
                font-style: italic;
                padding: 40px;
                text-align: center;
            }
        """)
        self.empty_state.setVisible(True)

        # Clear any existing content
        self._clear_progress_cards()

    def get_topic_progress(self, topic: str) -> int:
        """Get progress for a specific topic."""
        card = self.topic_cards.get(topic)
        return card.progress if card else 0

    def highlight_topic(self, topic: str):
        """Highlight a specific topic card."""
        card = self.topic_cards.get(topic)
        if card:
            # Scroll to the card
            self.scroll.ensureWidgetVisible(card)

            # Add temporary highlight effect
            original_style = card.styleSheet()
            card.setStyleSheet(original_style + """
                TopicProgressCard {
                    border: 2px solid #007bff;
                    background-color: #e3f2fd;
                }
            """)

            # Remove highlight after 2 seconds
            QTimer.singleShot(2000, lambda: card.setStyleSheet(original_style))