# gui/dialogs/tutorial_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QScrollArea, QSizePolicy,
    QProgressBar, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont


class StepWidget(QFrame):
    """Widget for displaying a single tutorial step."""

    def __init__(self, step_data: dict):
        super().__init__()
        self.step_data = step_data
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            StepWidget {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
            QLabel#titleLabel {
                color: #2d3436;
                font-size: 18px;
                font-weight: bold;
            }
            QLabel#contentLabel {
                color: #636e72;
                font-size: 14px;
                line-height: 1.6;
            }
            QLabel#tipLabel {
                color: #00b894;
                font-size: 13px;
                font-style: italic;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Step number and title
        header_layout = QHBoxLayout()

        step_number = QLabel(f"Step {self.step_data['number']}")
        step_number.setStyleSheet("""
            QLabel {
                background-color: #0984e3;
                color: white;
                border-radius: 12px;
                padding: 4px 12px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(step_number)

        title = QLabel(self.step_data['title'])
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Content
        content = QLabel(self.step_data['content'])
        content.setObjectName("contentLabel")
        content.setWordWrap(True)
        layout.addWidget(content)

        # Image if provided
        if 'image' in self.step_data:
            image_label = QLabel()
            pixmap = QPixmap(self.step_data['image'])
            image_label.setPixmap(pixmap.scaled(
                400, 200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(image_label)

        # Tip if provided
        if 'tip' in self.step_data:
            tip_layout = QHBoxLayout()

            tip_icon = QLabel("💡")
            tip_icon.setStyleSheet("font-size: 16px;")
            tip_layout.addWidget(tip_icon)

            tip = QLabel(f"Tip: {self.step_data['tip']}")
            tip.setObjectName("tipLabel")
            tip.setWordWrap(True)
            tip_layout.addWidget(tip)

            layout.addLayout(tip_layout)


class TutorialDialog(QDialog):
    """Dialog for displaying interactive tutorials."""

    tutorial_completed = pyqtSignal(str)  # Signal emitted when tutorial is completed

    def __init__(self, parent=None, tutorial_data: dict = None):
        super().__init__(parent)
        self.tutorial_data = tutorial_data or {}
        self.current_step = 0
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.tutorial_data.get('title', 'Tutorial'))
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            TutorialDialog {
                background-color: #f5f6fa;
            }
            QPushButton {
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton#nextButton {
                background-color: #0984e3;
                color: white;
            }
            QPushButton#nextButton:hover {
                background-color: #0878d4;
            }
            QPushButton#backButton {
                background-color: #dfe6e9;
                color: #2d3436;
            }
            QPushButton#backButton:hover {
                background-color: #b2bec3;
            }
            QPushButton#skipButton {
                background-color: transparent;
                color: #636e72;
            }
            QPushButton#skipButton:hover {
                color: #2d3436;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Header with title and progress
        header_layout = QHBoxLayout()

        title = QLabel(self.tutorial_data.get('title', 'Tutorial'))
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2d3436;
        """)
        header_layout.addWidget(title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(len(self.tutorial_data.get('steps', [])))
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #dfe6e9;
                border-radius: 7px;
                text-align: center;
                max-width: 200px;
            }
            QProgressBar::chunk {
                background-color: #0984e3;
                border-radius: 7px;
            }
        """)
        header_layout.addWidget(self.progress_bar)

        layout.addLayout(header_layout)

        # Stacked widget for steps
        self.step_stack = QStackedWidget()

        # Add steps to stack
        for step_data in self.tutorial_data.get('steps', []):
            step_widget = StepWidget(step_data)
            self.step_stack.addWidget(step_widget)

        layout.addWidget(self.step_stack)

        # Navigation buttons
        button_layout = QHBoxLayout()

        self.skip_button = QPushButton("Skip Tutorial")
        self.skip_button.setObjectName("skipButton")
        self.skip_button.clicked.connect(self.skip_tutorial)
        button_layout.addWidget(self.skip_button)

        button_layout.addStretch()

        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self.previous_step)
        self.back_button.setEnabled(False)
        button_layout.addWidget(self.back_button)

        self.next_button = QPushButton("Next")
        self.next_button.setObjectName("nextButton")
        self.next_button.clicked.connect(self.next_step)
        button_layout.addWidget(self.next_button)

        layout.addLayout(button_layout)

        # Update progress
        self.update_progress()

    def update_progress(self):
        """Update progress bar and navigation buttons."""
        total_steps = self.step_stack.count()
        self.progress_bar.setValue(self.current_step + 1)

        # Update button states
        self.back_button.setEnabled(self.current_step > 0)

        if self.current_step == total_steps - 1:
            self.next_button.setText("Finish")
        else:
            self.next_button.setText("Next")

        # Update skip button visibility
        self.skip_button.setVisible(self.current_step < total_steps - 1)

    def next_step(self):
        """Move to next step or complete tutorial."""
        if self.current_step < self.step_stack.count() - 1:
            self.current_step += 1
            self.step_stack.setCurrentIndex(self.current_step)
            self.update_progress()
        else:
            self.complete_tutorial()

    def previous_step(self):
        """Move to previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.step_stack.setCurrentIndex(self.current_step)
            self.update_progress()

    def skip_tutorial(self):
        """Skip the tutorial."""
        # You might want to show a confirmation dialog here
        self.reject()

    def complete_tutorial(self):
        """Complete the tutorial and emit signal."""
        tutorial_id = self.tutorial_data.get('id', '')
        self.tutorial_completed.emit(tutorial_id)
        self.accept()

    @classmethod
    def show_tutorial(cls, parent, tutorial_id: str, tutorial_data: dict):
        """Show a tutorial dialog."""
        dialog = cls(parent, tutorial_data)
        return dialog.exec()