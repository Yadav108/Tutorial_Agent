# gui/dialogs/tutorial_dialog.py

import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QWidget, QScrollArea,
    QCheckBox, QProgressBar, QTextEdit, QApplication
)
from PyQt6.QtCore import (
    Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve,
    QPoint, QRect, QSequentialAnimationGroup, QParallelAnimationGroup
)
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath, QIcon, QPixmap

logger = logging.getLogger('TutorialAgent.TutorialDialog')


@dataclass
class TutorialStep:
    """Single step in a tutorial."""
    number: int
    title: str
    content: str
    tip: str = ""
    highlight_element: Optional[str] = None  # CSS selector or widget name
    action_required: bool = False
    validation_func: Optional[Callable] = None
    auto_advance: bool = True
    duration: int = 0  # 0 means no auto-advance


class TutorialOverlay(QWidget):
    """Overlay widget that highlights specific UI elements."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self.highlight_rect = QRect()
        self.highlight_radius = 8

    def set_highlight_rect(self, rect: QRect):
        """Set the rectangle to highlight."""
        self.highlight_rect = rect
        self.update()

    def paintEvent(self, event):
        """Paint the overlay with highlight."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dark overlay
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))

        # Clear highlight area
        if not self.highlight_rect.isEmpty():
            # Create path for highlight
            highlight_path = QPainterPath()
            highlight_path.addRoundedRect(self.highlight_rect, self.highlight_radius, self.highlight_radius)

            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillPath(highlight_path, QColor(0, 0, 0, 0))

            # Draw highlight border
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            painter.setPen(QColor(0, 123, 255, 200))
            painter.drawPath(highlight_path)


class TutorialTooltip(QFrame):
    """Tooltip widget for tutorial steps."""

    next_clicked = pyqtSignal()
    previous_clicked = pyqtSignal()
    skip_clicked = pyqtSignal()
    close_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_animations()

        # Position and sizing
        self.setFixedWidth(350)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

    def setup_ui(self):
        """Setup tooltip UI."""
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #007bff;
                border-radius: 12px;
                padding: 0;
            }
        """)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()

        self.step_number_label = QLabel("1")
        self.step_number_label.setStyleSheet("""
            QLabel {
                background-color: #007bff;
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
                min-width: 30px;
                max-width: 30px;
                min-height: 30px;
                max-height: 30px;
                text-align: center;
                padding: 0;
            }
        """)
        self.step_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.step_number_label)

        self.title_label = QLabel("Tutorial Step")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #212529;
                margin-left: 10px;
            }
        """)
        header_layout.addWidget(self.title_label, 1)

        # Close button
        self.close_button = QPushButton("×")
        self.close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #6c757d;
                font-size: 20px;
                font-weight: bold;
                padding: 0;
                min-width: 24px;
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
            }
            QPushButton:hover {
                color: #dc3545;
                background: #f8f9fa;
                border-radius: 12px;
            }
        """)
        self.close_button.clicked.connect(self.close_clicked.emit)
        header_layout.addWidget(self.close_button)

        layout.addLayout(header_layout)

        # Content
        self.content_label = QLabel()
        self.content_label.setWordWrap(True)
        self.content_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 14px;
                line-height: 1.4;
            }
        """)
        layout.addWidget(self.content_label)

        # Tip (optional)
        self.tip_frame = QFrame()
        self.tip_frame.setStyleSheet("""
            QFrame {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 6px;
                padding: 8px 12px;
            }
        """)
        tip_layout = QHBoxLayout(self.tip_frame)
        tip_layout.setContentsMargins(8, 8, 8, 8)

        tip_icon = QLabel("💡")
        tip_icon.setStyleSheet("font-size: 16px;")
        tip_layout.addWidget(tip_icon)

        self.tip_label = QLabel()
        self.tip_label.setWordWrap(True)
        self.tip_label.setStyleSheet("""
            QLabel {
                color: #856404;
                font-size: 13px;
                font-style: italic;
            }
        """)
        tip_layout.addWidget(self.tip_label, 1)

        layout.addWidget(self.tip_frame)
        self.tip_frame.setVisible(False)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #e9ecef;
                border-radius: 4px;
                text-align: center;
                font-size: 12px;
                height: 8px;
            }
            QProgressBar::chunk {
                background-color: #007bff;
                border-radius: 4px;
            }
        """)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

        # Navigation buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.skip_button = QPushButton("Skip Tutorial")
        self.skip_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #6c757d;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #f8f9fa;
                color: #495057;
            }
        """)
        self.skip_button.clicked.connect(self.skip_clicked.emit)
        button_layout.addWidget(self.skip_button)

        button_layout.addStretch()

        self.previous_button = QPushButton("Previous")
        self.previous_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:disabled {
                background-color: #adb5bd;
            }
        """)
        self.previous_button.clicked.connect(self.previous_clicked.emit)
        button_layout.addWidget(self.previous_button)

        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.next_button.clicked.connect(self.next_clicked.emit)
        button_layout.addWidget(self.next_button)

        layout.addLayout(button_layout)

    def setup_animations(self):
        """Setup animations for the tooltip."""
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.move_animation = QPropertyAnimation(self, b"pos")
        self.move_animation.setDuration(400)
        self.move_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def update_step(self, step: TutorialStep, current_step: int, total_steps: int):
        """Update tooltip with step information."""
        self.step_number_label.setText(str(step.number))
        self.title_label.setText(step.title)
        self.content_label.setText(step.content)

        # Update tip
        if step.tip:
            self.tip_label.setText(step.tip)
            self.tip_frame.setVisible(True)
        else:
            self.tip_frame.setVisible(False)

        # Update progress
        progress = int((current_step / total_steps) * 100)
        self.progress_bar.setValue(progress)

        # Update buttons
        self.previous_button.setEnabled(current_step > 1)

        if current_step == total_steps:
            self.next_button.setText("Finish")
        else:
            self.next_button.setText("Next")

        # Adjust size
        self.adjustSize()

    def show_with_animation(self, position: QPoint):
        """Show tooltip with fade-in animation."""
        self.move(position)
        self.setWindowOpacity(0.0)
        self.show()

        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

    def hide_with_animation(self):
        """Hide tooltip with fade-out animation."""
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.hide)
        self.fade_animation.start()

    def move_to_position(self, position: QPoint):
        """Move tooltip to new position with animation."""
        self.move_animation.setStartValue(self.pos())
        self.move_animation.setEndValue(position)
        self.move_animation.start()


class TutorialManager:
    """Manages tutorial execution and state."""

    def __init__(self, parent_widget: QWidget):
        self.parent_widget = parent_widget
        self.current_tutorial: Optional[Dict[str, Any]] = None
        self.current_step_index = 0
        self.steps: List[TutorialStep] = []

        # UI components
        self.overlay = TutorialOverlay(parent_widget)
        self.tooltip = TutorialTooltip()

        # Auto-advance timer
        self.auto_advance_timer = QTimer()
        self.auto_advance_timer.setSingleShot(True)
        self.auto_advance_timer.timeout.connect(self.next_step)

        # Connect signals
        self.tooltip.next_clicked.connect(self.next_step)
        self.tooltip.previous_clicked.connect(self.previous_step)
        self.tooltip.skip_clicked.connect(self.skip_tutorial)
        self.tooltip.close_clicked.connect(self.end_tutorial)

        # Tutorial completion tracking
        self.completed_tutorials = set()
        self.skipped_tutorials = set()

    def start_tutorial(self, tutorial_data: Dict[str, Any]):
        """Start a tutorial."""
        try:
            self.current_tutorial = tutorial_data
            self.current_step_index = 0

            # Convert steps data to TutorialStep objects
            self.steps = []
            for step_data in tutorial_data.get('steps', []):
                step = TutorialStep(
                    number=step_data.get('number', len(self.steps) + 1),
                    title=step_data.get('title', ''),
                    content=step_data.get('content', ''),
                    tip=step_data.get('tip', ''),
                    highlight_element=step_data.get('highlight_element'),
                    action_required=step_data.get('action_required', False),
                    auto_advance=step_data.get('auto_advance', True),
                    duration=step_data.get('duration', 0)
                )
                self.steps.append(step)

            if not self.steps:
                logger.warning("No steps found in tutorial")
                return

            # Setup overlay
            self.overlay.resize(self.parent_widget.size())
            self.overlay.show()

            # Show first step
            self.show_current_step()

            logger.info(f"Started tutorial: {tutorial_data.get('title', 'Unknown')}")

        except Exception as e:
            logger.error(f"Error starting tutorial: {e}")
            self.end_tutorial()

    def show_current_step(self):
        """Show the current tutorial step."""
        if not self.steps or self.current_step_index >= len(self.steps):
            self.end_tutorial()
            return

        step = self.steps[self.current_step_index]

        # Update tooltip
        self.tooltip.update_step(step, self.current_step_index + 1, len(self.steps))

        # Handle highlighting
        if step.highlight_element:
            self._highlight_element(step.highlight_element)
        else:
            self.overlay.set_highlight_rect(QRect())

        # Position tooltip
        tooltip_position = self._calculate_tooltip_position(step)

        if self.current_step_index == 0:
            # First step - show with animation
            self.tooltip.show_with_animation(tooltip_position)
        else:
            # Move to new position
            self.tooltip.move_to_position(tooltip_position)

        # Setup auto-advance if enabled
        if step.auto_advance and step.duration > 0:
            self.auto_advance_timer.start(step.duration * 1000)
        else:
            self.auto_advance_timer.stop()

    def _highlight_element(self, element_identifier: str):
        """Highlight a specific UI element."""
        try:
            # Try to find widget by object name
            widget = self.parent_widget.findChild(QWidget, element_identifier)

            if widget and widget.isVisible():
                # Get global position and size
                global_pos = widget.mapToGlobal(QPoint(0, 0))
                parent_pos = self.parent_widget.mapFromGlobal(global_pos)

                highlight_rect = QRect(
                    parent_pos.x() - 5,
                    parent_pos.y() - 5,
                    widget.width() + 10,
                    widget.height() + 10
                )

                self.overlay.set_highlight_rect(highlight_rect)
            else:
                logger.warning(f"Could not find or highlight element: {element_identifier}")
                self.overlay.set_highlight_rect(QRect())

        except Exception as e:
            logger.error(f"Error highlighting element {element_identifier}: {e}")
            self.overlay.set_highlight_rect(QRect())

    def _calculate_tooltip_position(self, step: TutorialStep) -> QPoint:
        """Calculate optimal position for tooltip."""
        parent_rect = self.parent_widget.rect()
        tooltip_size = self.tooltip.sizeHint()

        # Default position (center-right)
        default_x = parent_rect.width() - tooltip_size.width() - 50
        default_y = parent_rect.height() // 2 - tooltip_size.height() // 2

        # If highlighting an element, position relative to it
        if step.highlight_element and not self.overlay.highlight_rect.isEmpty():
            highlight_rect = self.overlay.highlight_rect

            # Try to position tooltip to the right of highlighted element
            x = highlight_rect.right() + 20
            y = highlight_rect.top()

            # Adjust if tooltip would go off-screen
            if x + tooltip_size.width() > parent_rect.width():
                x = highlight_rect.left() - tooltip_size.width() - 20

            if y + tooltip_size.height() > parent_rect.height():
                y = parent_rect.height() - tooltip_size.height() - 20

            if x < 0:
                x = 20
            if y < 0:
                y = 20

            return QPoint(max(20, x), max(20, y))

        return QPoint(default_x, default_y)

    def next_step(self):
        """Move to the next tutorial step."""
        self.auto_advance_timer.stop()

        if self.current_step_index < len(self.steps) - 1:
            self.current_step_index += 1
            self.show_current_step()
        else:
            self.complete_tutorial()

    def previous_step(self):
        """Move to the previous tutorial step."""
        self.auto_advance_timer.stop()

        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.show_current_step()

    def skip_tutorial(self):
        """Skip the current tutorial."""
        if self.current_tutorial:
            tutorial_id = self.current_tutorial.get('id')
            if tutorial_id:
                self.skipped_tutorials.add(tutorial_id)

            logger.info(f"Skipped tutorial: {self.current_tutorial.get('title', 'Unknown')}")

        self.end_tutorial()

    def complete_tutorial(self):
        """Mark tutorial as completed and end it."""
        if self.current_tutorial:
            tutorial_id = self.current_tutorial.get('id')
            if tutorial_id:
                self.completed_tutorials.add(tutorial_id)

            logger.info(f"Completed tutorial: {self.current_tutorial.get('title', 'Unknown')}")

        self.end_tutorial()

    def end_tutorial(self):
        """End the current tutorial and cleanup."""
        self.auto_advance_timer.stop()

        # Hide UI components
        self.tooltip.hide_with_animation()
        self.overlay.hide()

        # Reset state
        self.current_tutorial = None
        self.current_step_index = 0
        self.steps.clear()

    def is_tutorial_completed(self, tutorial_id: str) -> bool:
        """Check if a tutorial has been completed."""
        return tutorial_id in self.completed_tutorials

    def is_tutorial_skipped(self, tutorial_id: str) -> bool:
        """Check if a tutorial has been skipped."""
        return tutorial_id in self.skipped_tutorials


class TutorialDialog(QDialog):
    """Static dialog for showing tutorial management interface."""

    @staticmethod
    def show_tutorial(parent: QWidget, tutorial_id: str, tutorial_data: Dict[str, Any]):
        """Show a tutorial using the tutorial manager."""
        if not hasattr(parent, '_tutorial_manager'):
            parent._tutorial_manager = TutorialManager(parent)

        # Check if tutorial was already completed or skipped
        if parent._tutorial_manager.is_tutorial_completed(tutorial_id):
            logger.debug(f"Tutorial {tutorial_id} already completed, skipping")
            return

        if parent._tutorial_manager.is_tutorial_skipped(tutorial_id):
            logger.debug(f"Tutorial {tutorial_id} was skipped, not showing")
            return

        parent._tutorial_manager.start_tutorial(tutorial_data)

    @staticmethod
    def create_welcome_tutorial() -> Dict[str, Any]:
        """Create the welcome tutorial data."""
        return {
            'id': 'welcome',
            'title': 'Welcome to Tutorial Agent',
            'steps': [
                {
                    'number': 1,
                    'title': 'Welcome! 🎉',
                    'content': 'Welcome to Tutorial Agent! This interactive tutorial will guide you through the main features of the application.',
                    'tip': 'You can skip this tutorial at any time or navigate using the Previous/Next buttons.',
                    'duration': 5
                },
                {
                    'number': 2,
                    'title': 'Language Selection',
                    'content': 'The sidebar on the left shows available programming languages. Click on any language card to start learning.',
                    'tip': 'Each language card shows your progress and estimated completion time.',
                    'highlight_element': 'language_cards_container'
                },
                {
                    'number': 3,
                    'title': 'Content Area',
                    'content': 'The main content area displays tutorials, examples, and exercises for the selected language.',
                    'tip': 'You can resize the content area by dragging the splitter between sections.',
                    'highlight_element': 'content_viewer'
                },
                {
                    'number': 4,
                    'title': 'Code Editor',
                    'content': 'The bottom section contains a powerful code editor where you can write and test code instantly.',
                    'tip': 'Use Ctrl+Enter to run code and Ctrl+K to clear the editor.',
                    'highlight_element': 'code_editor'
                },
                {
                    'number': 5,
                    'title': 'Progress Tracking',
                    'content': 'Your learning progress is automatically tracked and displayed in the sidebar below the language cards.',
                    'tip': 'Complete exercises and examples to earn progress points!',
                    'highlight_element': 'progress_viewer'
                },
                {
                    'number': 6,
                    'title': 'Search & Navigation',
                    'content': 'Use the search bar in the toolbar to quickly find specific topics, examples, or exercises.',
                    'tip': 'You can also use keyboard shortcuts for faster navigation.',
                    'highlight_element': 'search_bar'
                },
                {
                    'number': 7,
                    'title': 'Ready to Learn! ✨',
                    'content': 'You\'re all set! Choose a programming language from the sidebar to begin your learning journey.',
                    'tip': 'Remember: practice makes perfect. Don\'t hesitate to experiment with the code examples!',
                    'duration': 3
                }
            ]
        }

    @staticmethod
    def create_language_tutorial(language_name: str) -> Dict[str, Any]:
        """Create a language-specific tutorial."""
        return {
            'id': f'{language_name.lower()}_intro',
            'title': f'Getting Started with {language_name}',
            'steps': [
                {
                    'number': 1,
                    'title': f'Welcome to {language_name}! 🚀',
                    'content': f'You\'ve selected {language_name}. This tutorial will show you how to make the most of your {language_name} learning experience.',
                    'tip': f'{language_name} is a powerful programming language with many practical applications.'
                },
                {
                    'number': 2,
                    'title': 'Topic Structure',
                    'content': 'Each topic contains explanations, interactive examples, and hands-on exercises to reinforce your learning.',
                    'tip': 'Start with the basics and work your way up to more advanced topics.',
                    'highlight_element': 'content_viewer'
                },
                {
                    'number': 3,
                    'title': 'Interactive Examples',
                    'content': 'Click "Run Example" buttons to load code into the editor and see it in action.',
                    'tip': 'Try modifying the examples to experiment and learn!',
                    'highlight_element': 'code_editor'
                },
                {
                    'number': 4,
                    'title': 'Practice Exercises',
                    'content': 'Complete exercises to test your understanding and earn progress points.',
                    'tip': 'Don\'t worry if you don\'t get it right the first time - learning is a process!',
                    'highlight_element': 'progress_viewer'
                },
                {
                    'number': 5,
                    'title': 'Start Coding! 💻',
                    'content': f'You\'re ready to start your {language_name} journey. Begin with the first topic and have fun learning!',
                    'tip': 'Take breaks, practice regularly, and don\'t hesitate to revisit topics as needed.'
                }
            ]
        }

    @staticmethod
    def create_feature_tutorial(feature_name: str, steps_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a tutorial for a specific feature."""
        return {
            'id': f'{feature_name.lower()}_tutorial',
            'title': f'{feature_name} Tutorial',
            'steps': steps_data
        }


# Convenience functions for common tutorials
def show_welcome_tutorial(parent: QWidget):
    """Show the welcome tutorial."""
    tutorial_data = TutorialDialog.create_welcome_tutorial()
    TutorialDialog.show_tutorial(parent, 'welcome', tutorial_data)


def show_language_tutorial(parent: QWidget, language_name: str):
    """Show a language-specific tutorial."""
    tutorial_data = TutorialDialog.create_language_tutorial(language_name)
    TutorialDialog.show_tutorial(parent, f'{language_name.lower()}_intro', tutorial_data)


def show_feature_tutorial(parent: QWidget, feature_name: str, steps: List[Dict[str, Any]]):
    """Show a feature-specific tutorial."""
    tutorial_data = TutorialDialog.create_feature_tutorial(feature_name, steps)
    TutorialDialog.show_tutorial(parent, f'{feature_name.lower()}_tutorial', tutorial_data)