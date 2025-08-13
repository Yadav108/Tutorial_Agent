# gui/widgets/enhanced_code_editor.py

import logging
import subprocess
import tempfile
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QTabWidget,
    QPushButton, QLabel, QComboBox, QSplitter, QProgressBar,
    QToolBar, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread, pyqtSlot
from PyQt6.QtGui import (
    QFont, QSyntaxHighlighter, QTextCharFormat, QColor,
    QTextCursor, QTextDocument, QPainter
)

logger = logging.getLogger('TutorialAgent.CodeEditor')


class SimpleSyntaxHighlighter(QSyntaxHighlighter):
    """Simple syntax highlighter for multiple languages."""

    def __init__(self, document: QTextDocument, language: str = 'python'):
        super().__init__(document)
        self.language = language.lower()
        self.setup_highlighting_rules()

    def setup_highlighting_rules(self):
        """Setup syntax highlighting rules."""
        self.highlighting_rules = []

        # Define colors for dark theme
        keyword_color = QColor("#569cd6")  # Blue
        string_color = QColor("#ce9178")  # Orange
        comment_color = QColor("#6a9955")  # Green
        number_color = QColor("#b5cea8")  # Light green

        # Keywords format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(keyword_color)
        keyword_format.setFontWeight(QFont.Weight.Bold)

        # Define keywords for different languages
        if self.language == 'python':
            keywords = [
                'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
                'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
                'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
                'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
                'True', 'try', 'while', 'with', 'yield', 'print', 'len',
                'range', 'str', 'int', 'float', 'list', 'dict', 'tuple'
            ]
        elif self.language == 'javascript':
            keywords = [
                'async', 'await', 'break', 'case', 'catch', 'class', 'const',
                'continue', 'default', 'do', 'else', 'export', 'extends',
                'false', 'finally', 'for', 'function', 'if', 'import', 'in',
                'instanceof', 'let', 'new', 'null', 'return', 'super',
                'switch', 'this', 'throw', 'true', 'try', 'typeof', 'var',
                'void', 'while', 'with', 'yield'
            ]
        elif self.language in ['csharp', 'c#']:
            keywords = [
                'abstract', 'as', 'base', 'bool', 'break', 'byte', 'case',
                'catch', 'char', 'checked', 'class', 'const', 'continue',
                'decimal', 'default', 'delegate', 'do', 'double', 'else',
                'enum', 'event', 'explicit', 'extern', 'false', 'finally',
                'fixed', 'float', 'for', 'foreach', 'goto', 'if', 'implicit',
                'in', 'int', 'interface', 'internal', 'is', 'lock', 'long',
                'namespace', 'new', 'null', 'object', 'operator', 'out',
                'override', 'params', 'private', 'protected', 'public',
                'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short',
                'sizeof', 'stackalloc', 'static', 'string', 'struct',
                'switch', 'this', 'throw', 'true', 'try', 'typeof', 'uint',
                'ulong', 'unchecked', 'unsafe', 'ushort', 'using', 'virtual',
                'void', 'volatile', 'while'
            ]
        else:
            keywords = []

        # Add keyword patterns
        for keyword in keywords:
            pattern = f'\\b{keyword}\\b'
            self.highlighting_rules.append((pattern, keyword_format))

        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(string_color)

        # Add string patterns based on language
        if self.language == 'python':
            self.highlighting_rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', string_format))
            self.highlighting_rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", string_format))
        else:
            self.highlighting_rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', string_format))
            self.highlighting_rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", string_format))

        # Number format
        number_format = QTextCharFormat()
        number_format.setForeground(number_color)
        self.highlighting_rules.append((r'\b\d+\.?\d*\b', number_format))

        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(comment_color)
        comment_format.setFontItalic(True)

        if self.language == 'python':
            self.highlighting_rules.append((r'#[^\r\n]*', comment_format))
        elif self.language in ['javascript', 'csharp', 'c#', 'java']:
            self.highlighting_rules.append((r'//[^\r\n]*', comment_format))

    def highlightBlock(self, text):
        """Apply syntax highlighting to a text block."""
        for pattern, format_obj in self.highlighting_rules:
            regex = re.compile(pattern)
            for match in regex.finditer(text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, format_obj)


class CodeExecutionThread(QThread):
    """Thread for executing code safely."""

    output_ready = pyqtSignal(str)
    error_ready = pyqtSignal(str)
    execution_finished = pyqtSignal(bool)

    def __init__(self, code: str, language: str):
        super().__init__()
        self.code = code
        self.language = language.lower()

    def run(self):
        """Execute the code."""
        try:
            if self.language == 'python':
                self._execute_python()
            elif self.language == 'javascript':
                self._execute_javascript()
            else:
                self.error_ready.emit(f"Code execution not yet supported for {self.language}")
                self.execution_finished.emit(False)

        except Exception as e:
            self.error_ready.emit(f"Execution error: {str(e)}")
            self.execution_finished.emit(False)

    def _execute_python(self):
        """Execute Python code."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.code)
            temp_file = f.name

        try:
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                self.output_ready.emit(result.stdout or "Code executed successfully (no output)")
                self.execution_finished.emit(True)
            else:
                self.error_ready.emit(result.stderr or "Unknown error occurred")
                self.execution_finished.emit(False)

        finally:
            try:
                os.unlink(temp_file)
            except:
                pass

    def _execute_javascript(self):
        """Execute JavaScript code using Node.js."""
        try:
            subprocess.run(['node', '--version'], capture_output=True, timeout=5)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.error_ready.emit("Node.js not found. Please install Node.js to run JavaScript code.")
            self.execution_finished.emit(False)
            return

        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(self.code)
            temp_file = f.name

        try:
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                self.output_ready.emit(result.stdout or "Code executed successfully (no output)")
                self.execution_finished.emit(True)
            else:
                self.error_ready.emit(result.stderr or "Unknown error occurred")
                self.execution_finished.emit(False)

        finally:
            try:
                os.unlink(temp_file)
            except:
                pass


class EnhancedCodeEditor(QTextEdit):
    """Enhanced code editor with basic professional features."""

    content_changed = pyqtSignal()

    def __init__(self, language: str = 'python'):
        super().__init__()
        self.language = language.lower()
        self.setup_editor()
        self.setup_syntax_highlighting()

        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.setSingleShot(True)

        # Connect signals
        self.textChanged.connect(self.on_text_changed)

    def setup_editor(self):
        """Setup the editor appearance and behavior."""
        # Font
        font = QFont("Consolas", 12)
        if not font.exactMatch():
            font = QFont("Courier New", 12)
        font.setFixedPitch(True)
        self.setFont(font)

        # Tab settings
        self.setTabStopDistance(40)  # 4 spaces

        # Line wrap
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        # Styling
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                selection-background-color: #264f78;
                selection-color: #ffffff;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12pt;
                line-height: 1.4;
                padding: 8px;
            }
        """)

    def setup_syntax_highlighting(self):
        """Setup syntax highlighting based on language."""
        self.highlighter = SimpleSyntaxHighlighter(self.document(), self.language)

    def keyPressEvent(self, event):
        """Handle key press events for smart editing."""
        # Auto-indentation on Enter
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.textCursor()
            current_line = cursor.block().text()

            # Calculate current indentation
            indent = 0
            for char in current_line:
                if char == ' ':
                    indent += 1
                elif char == '\t':
                    indent += 4
                else:
                    break

            # Add extra indent for certain patterns
            if current_line.strip().endswith(':'):
                indent += 4
            elif current_line.strip().endswith('{'):
                indent += 4

            super().keyPressEvent(event)
            self.insertPlainText(' ' * indent)
            return

        super().keyPressEvent(event)

    def on_text_changed(self):
        """Handle text changes."""
        self.content_changed.emit()
        self.auto_save_timer.start(2000)  # Auto-save after 2 seconds

    def auto_save(self):
        """Auto-save functionality."""
        logger.debug("Auto-saving code editor content")

    def set_language(self, language: str):
        """Set the programming language."""
        self.language = language.lower()
        self.setup_syntax_highlighting()

    def set_code(self, code: str):
        """Set the code content."""
        self.setPlainText(code)

    def get_code(self) -> str:
        """Get the current code content."""
        return self.toPlainText()

    def clear_editor(self):
        """Clear the editor content."""
        self.clear()


class ProfessionalCodeEditor(QWidget):
    """Professional code editor widget with tabs and execution."""

    code_executed = pyqtSignal(bool, str)  # success, output

    def __init__(self):
        super().__init__()
        self.current_language = 'python'
        self.execution_thread = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create toolbar
        self.create_toolbar()
        layout.addWidget(self.toolbar)

        # Create splitter for editor and output
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Create tab widget for multiple files
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3e3e3e;
                background: #1e1e1e;
            }
            QTabBar::tab {
                background: #2d2d30;
                color: #d4d4d4;
                padding: 8px 12px;
                margin-right: 2px;
                border: 1px solid #3e3e3e;
            }
            QTabBar::tab:selected {
                background: #1e1e1e;
                border-bottom: 1px solid #1e1e1e;
            }
            QTabBar::tab:hover {
                background: #3e3e3e;
            }
        """)

        # Add initial editor
        self.add_new_tab()

        splitter.addWidget(self.tab_widget)

        # Create output area
        self.output_area = self.create_output_area()
        splitter.addWidget(self.output_area)

        # Set splitter proportions
        splitter.setStretchFactor(0, 3)  # Editor
        splitter.setStretchFactor(1, 1)  # Output
        splitter.setSizes([600, 200])

        layout.addWidget(splitter)

    def create_toolbar(self):
        """Create the editor toolbar."""
        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet("""
            QToolBar {
                background: #2d2d30;
                border: none;
                spacing: 5px;
                padding: 8px;
            }
            QPushButton {
                background: #0e639c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
                min-height: 20px;
            }
            QPushButton:hover {
                background: #1177bb;
            }
            QPushButton:pressed {
                background: #0d5a94;
            }
            QPushButton:disabled {
                background: #404040;
                color: #808080;
            }
            QComboBox {
                background: #3e3e3e;
                color: white;
                border: 1px solid #5a5a5a;
                border-radius: 4px;
                padding: 6px 10px;
                min-width: 120px;
                font-size: 12px;
            }
        """)

        # Run button
        self.run_button = QPushButton("▶ Run Code")
        self.run_button.clicked.connect(self.run_code)
        self.toolbar.addWidget(self.run_button)

        # Language selector
        self.language_combo = QComboBox()
        self.language_combo.addItems(['Python', 'JavaScript', 'Java', 'C#'])
        self.language_combo.currentTextChanged.connect(self.change_language)
        self.toolbar.addWidget(self.language_combo)

        # Add separator
        self.toolbar.addSeparator()

        # Clear button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_editor)
        self.toolbar.addWidget(clear_button)

        # New tab button
        new_tab_button = QPushButton("+ New Tab")
        new_tab_button.clicked.connect(self.add_new_tab)
        self.toolbar.addWidget(new_tab_button)

    def create_output_area(self):
        """Create the output display area."""
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        output_layout.setContentsMargins(8, 8, 8, 8)

        # Output label
        output_label = QLabel("Output:")
        output_label.setStyleSheet("""
            QLabel {
                color: #d4d4d4; 
                font-weight: bold; 
                font-size: 13px;
                margin-bottom: 5px;
            }
        """)
        output_layout.addWidget(output_label)

        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(180)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #0c0c0c;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11pt;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        output_layout.addWidget(self.output_text)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                text-align: center;
                background: #2d2d30;
                color: white;
                font-size: 12px;
                height: 24px;
            }
            QProgressBar::chunk {
                background-color: #0e639c;
                border-radius: 3px;
            }
        """)
        output_layout.addWidget(self.progress_bar)

        return output_widget

    def add_new_tab(self, title: str = None):
        """Add a new editor tab."""
        if title is None:
            ext_map = {
                'python': '.py',
                'javascript': '.js',
                'java': '.java',
                'csharp': '.cs'
            }
            ext = ext_map.get(self.current_language, '.py')
            title = f"untitled_{self.tab_widget.count() + 1}{ext}"

        editor = EnhancedCodeEditor(self.current_language)
        editor.content_changed.connect(self.on_content_changed)

        # Add starter code
        starter_code = self.get_starter_code(self.current_language)
        editor.set_code(starter_code)

        self.tab_widget.addTab(editor, title)
        self.tab_widget.setCurrentWidget(editor)

        return editor

    def get_starter_code(self, language: str) -> str:
        """Get starter code for different languages."""
        starters = {
            'python': '# Write your Python code here\nprint("Hello, World!")\n',
            'javascript': '// Write your JavaScript code here\nconsole.log("Hello, World!");\n',
            'java': '''// Write your Java code here
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}''',
            'csharp': '''// Write your C# code here
using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello, World!");
    }
}'''
        }
        return starters.get(language, '// Write your code here\n')

    def close_tab(self, index: int):
        """Close a tab."""
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def get_current_editor(self) -> Optional[EnhancedCodeEditor]:
        """Get the currently active editor."""
        return self.tab_widget.currentWidget()

    def set_language(self, language: str):
        """Set the programming language."""
        self.current_language = language.lower()

        # Update all editors
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if isinstance(editor, EnhancedCodeEditor):
                editor.set_language(self.current_language)

        # Update language combo
        language_map = {
            'python': 'Python',
            'javascript': 'JavaScript',
            'java': 'Java',
            'csharp': 'C#'
        }
        display_name = language_map.get(self.current_language, 'Python')

        index = self.language_combo.findText(display_name)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)

    def change_language(self, language: str):
        """Handle language change from combo box."""
        language_map = {
            'Python': 'python',
            'JavaScript': 'javascript',
            'Java': 'java',
            'C#': 'csharp'
        }
        self.set_language(language_map.get(language, 'python'))

    def set_code(self, code: str):
        """Set code in the current editor."""
        editor = self.get_current_editor()
        if editor:
            editor.set_code(code)

    def get_code(self) -> str:
        """Get code from the current editor."""
        editor = self.get_current_editor()
        return editor.get_code() if editor else ""

    def clear_editor(self):
        """Clear the current editor."""
        editor = self.get_current_editor()
        if editor:
            editor.clear_editor()
        self.output_text.clear()

    def run_code(self):
        """Execute the current code."""
        editor = self.get_current_editor()
        if not editor:
            return

        code = editor.get_code().strip()
        if not code:
            self.output_text.setPlainText("No code to execute.")
            return

        # Disable run button and show progress
        self.run_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.output_text.setPlainText("Executing code...")

        # Execute in background thread
        self.execution_thread = CodeExecutionThread(code, self.current_language)
        self.execution_thread.output_ready.connect(self.show_output)
        self.execution_thread.error_ready.connect(self.show_error)
        self.execution_thread.execution_finished.connect(self.execution_finished)
        self.execution_thread.start()

    @pyqtSlot(str)
    def show_output(self, output: str):
        """Show execution output."""
        self.output_text.setPlainText(output)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #0c0c0c;
                color: #90ee90;
                border: 1px solid #3e3e3e;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11pt;
                border-radius: 4px;
                padding: 8px;
            }
        """)

    @pyqtSlot(str)
    def show_error(self, error: str):
        """Show execution error."""
        self.output_text.setPlainText(error)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #0c0c0c;
                color: #ff6b6b;
                border: 1px solid #3e3e3e;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11pt;
                border-radius: 4px;
                padding: 8px;
            }
        """)

    @pyqtSlot(bool)
    def execution_finished(self, success: bool):
        """Handle execution completion."""
        self.run_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.code_executed.emit(success, self.output_text.toPlainText())

        # Show notification
        try:
            from utils.simple_notifications import show_success, show_error
            if success:
                show_success("Code executed successfully!")
            else:
                show_error("Code execution failed!")
        except ImportError:
            pass

    def on_content_changed(self):
        """Handle editor content changes."""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            current_title = self.tab_widget.tabText(current_index)
            if not current_title.endswith('*'):
                self.tab_widget.setTabText(current_index, current_title + '*')