# gui/widgets/code_editor.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit,
    QPushButton, QLabel, QComboBox, QFrame, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter


class CodeEditor(QWidget):
    """Code editor widget with syntax highlighting and execution."""

    code_executed = pyqtSignal(str)  # Signal emitted when code is executed

    def __init__(self):
        super().__init__()
        self.current_language = None
        self.highlighter = None
        self.init_widgets()
        self.setup_ui()
        self.set_theme("Dark")  # Set default theme after widgets are created

    def init_widgets(self):
        """Initialize widgets before setup."""
        # Language selector
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Python", "JavaScript", "C#", "Java", "C++"])
        self.language_selector.currentTextChanged.connect(self.set_language)

        # Theme selector
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark", "Light"])
        self.theme_selector.currentTextChanged.connect(self.set_theme)

        # Run button
        self.run_button = QPushButton("Run")
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.run_button.clicked.connect(self.run_code)

        # Code editor
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Courier New", 12))

        # Output area
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier New", 12))
        self.output.setMaximumHeight(150)

    def setup_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create toolbar
        toolbar = QFrame()
        toolbar.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
            }
        """)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)

        # Add widgets to toolbar
        toolbar_layout.addWidget(QLabel("Language:"))
        toolbar_layout.addWidget(self.language_selector)
        toolbar_layout.addWidget(QLabel("Theme:"))
        toolbar_layout.addWidget(self.theme_selector)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.run_button)

        layout.addWidget(toolbar)

        # Create editor and output areas
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.output)

        layout.addWidget(splitter)

    def set_language(self, language: str):
        """Set the programming language and update syntax highlighting."""
        self.current_language = language

        # Clear existing highlighter
        if self.highlighter:
            self.highlighter.setDocument(None)
            self.highlighter = None

        # Set template code
        self.set_template_code(language)

        # Update status
        self.output.clear()
        self.output.appendPlainText(f"Switched to {language}")

    def set_theme(self, theme: str):
        """Set the editor theme."""
        if theme == "Dark":
            editor_style = """
                QPlainTextEdit {
                    background-color: #282c34;
                    color: #abb2bf;
                    border: none;
                }
            """
            output_style = """
                QPlainTextEdit {
                    background-color: #21252b;
                    color: #98c379;
                    border: none;
                    border-top: 1px solid #181a1f;
                }
            """
        else:
            editor_style = """
                QPlainTextEdit {
                    background-color: white;
                    color: #2c3e50;
                    border: none;
                }
            """
            output_style = """
                QPlainTextEdit {
                    background-color: #f8f9fa;
                    color: #2c3e50;
                    border: none;
                    border-top: 1px solid #dee2e6;
                }
            """

        self.editor.setStyleSheet(editor_style)
        self.output.setStyleSheet(output_style)

    def set_template_code(self, language: str):
        """Set template code for the selected language."""
        templates = {
            "Python": "# Write your Python code here\n\n",
            "JavaScript": "// Write your JavaScript code here\n\n",
            "C#": """using System;

class Program
{
    static void Main()
    {
        // Write your C# code here
    }
}""",
            "Java": """public class Main {
    public static void main(String[] args) {
        // Write your Java code here
    }
}""",
            "C++": """#include <iostream>

int main() {
    // Write your C++ code here
    return 0;
}"""
        }

        self.editor.setPlainText(templates.get(language, ""))

    def run_code(self):
        """Execute the current code."""
        if not self.current_language:
            self.output.setPlainText("Error: Please select a language first.")
            return

        code = self.editor.toPlainText()
        if not code.strip():
            self.output.setPlainText("Error: No code to execute!")
            return

        self.output.clear()
        self.output.appendPlainText(f"Executing {self.current_language} code...\n")
        self.code_executed.emit(code)

    def set_output(self, text: str):
        """Set the output text."""
        self.output.setPlainText(text)

    def append_output(self, text: str):
        """Append text to the output."""
        self.output.appendPlainText(text)

    def get_code(self) -> str:
        """Get the current code from the editor."""
        return self.editor.toPlainText()

    def set_code(self, code: str):
        """Set code in the editor."""
        self.editor.setPlainText(code)

    def clear(self):
        """Clear both editor and output."""
        self.editor.clear()
        self.output.clear()