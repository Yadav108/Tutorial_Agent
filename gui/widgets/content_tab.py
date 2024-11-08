# gui/widgets/content_tab.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QScrollArea,
    QSplitter, QFrame, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QTextCursor
from gui.widgets.code_editor import CodeEditor
import re


class ContentTab(QWidget):
    """Widget for displaying tutorial content in a tab."""

    code_executed = pyqtSignal(str)  # Signal when code is executed

    def __init__(self, title: str, content: str, language: str = None, parent=None):
        """
        Initialize content tab.

        Args:
            title (str): Tab title
            content (str): HTML content to display
            language (str): Programming language for code editor
            parent: Parent widget
        """
        super().__init__(parent)
        self.title = title
        self.language = language
        self.code_editor = None
        self.init_ui(content)

    def init_ui(self, content: str):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create toolbar if needed
        if self._needs_toolbar(content):
            toolbar = self._create_toolbar()
            layout.addWidget(toolbar)

        # Create splitter for content and code editor
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Create content display with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        self.content_display = QTextEdit()
        self.content_display.setReadOnly(True)
        self.content_display.setHtml(content)
        self.content_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                line-height: 1.6;
            }
            QTextEdit:focus {
                outline: none;
            }
        """)
        self.content_display.setAcceptRichText(True)

        content_layout.addWidget(self.content_display)
        scroll_area.setWidget(content_widget)
        splitter.addWidget(scroll_area)

        # Add code editor if needed
        if self._needs_code_editor(content):
            self.code_editor = CodeEditor()
            if self.language:
                self.code_editor.set_language(self.language)

            # Connect code editor signals
            self.code_editor.code_executed.connect(self.code_executed)

            splitter.addWidget(self.code_editor)

            # Set initial sizes (60% content, 40% editor)
            splitter.setSizes([600, 400])

            # Set starter code if present
            starter_code = self._extract_starter_code(content)
            if starter_code:
                self.code_editor.editor.setPlainText(starter_code)

        layout.addWidget(splitter)

    def _needs_toolbar(self, content: str) -> bool:
        """Check if content needs a toolbar."""
        return any(keyword in content for keyword in
                   ['Exercise', 'Example', 'Practice', 'Quiz'])

    def _create_toolbar(self) -> QFrame:
        """Create toolbar with relevant buttons."""
        toolbar = QFrame()
        toolbar.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                padding: 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)

        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(10, 5, 10, 5)

        # Add buttons based on content type
        if hasattr(self, 'title'):
            if 'Exercise' in self.title:
                check_btn = QPushButton("Check Solution")
                check_btn.clicked.connect(self._check_solution)
                layout.addWidget(check_btn)
            elif 'Example' in self.title:
                run_btn = QPushButton("Run Example")
                run_btn.clicked.connect(self._run_example)
                layout.addWidget(run_btn)

        layout.addStretch()
        return toolbar

    def _needs_code_editor(self, content: str) -> bool:
        """Check if content needs a code editor."""
        return any(keyword in content for keyword in
                   ['Exercise', 'Example', 'Practice', 'Try it yourself', '<code>'])

    def _extract_starter_code(self, content: str) -> str:
        """Extract starter code from content."""
        # Try different code block patterns
        patterns = [
            r'<pre><code>(.*?)</code></pre>',
            r'```[\w]*\n(.*?)```',
            r'<div class="starter-code">(.*?)</div>'
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                code = match.group(1)
                return self._clean_code(code)

        return ""

    def _clean_code(self, code: str) -> str:
        """Clean extracted code."""
        # Remove HTML entities
        code = code.replace('&lt;', '<').replace('&gt;', '>')
        code = code.replace('&amp;', '&').replace('&quot;', '"')

        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in code.splitlines()]

        # Remove empty lines from start and end
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()

        return '\n'.join(lines)

    def update_content(self, content: str):
        """Update the displayed content."""
        self.content_display.setHtml(content)

        # Update code editor if needed
        if self.code_editor:
            starter_code = self._extract_starter_code(content)
            if starter_code:
                self.code_editor.editor.setPlainText(starter_code)

    def get_editor(self):
        """Get the code editor if it exists."""
        return self.code_editor

    def _run_example(self):
        """Run the example code."""
        if self.code_editor:
            self.code_editor.run_code()

    def _check_solution(self):
        """Check the exercise solution."""
        if self.code_editor:
            # Here you would implement solution checking logic
            code = self.code_editor.editor.toPlainText()
            self.code_executed.emit(code)

    def set_language(self, language: str):
        """Set the programming language for the code editor."""
        self.language = language
        if self.code_editor:
            self.code_editor.set_language(language)

    def get_code(self) -> str:
        """Get the current code from the editor."""
        if self.code_editor:
            return self.code_editor.editor.toPlainText()
        return ""

    def set_code(self, code: str):
        """Set code in the editor."""
        if self.code_editor:
            self.code_editor.editor.setPlainText(code)

    def clear_output(self):
        """Clear the code editor output."""
        if self.code_editor:
            self.code_editor.set_output("")