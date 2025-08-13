# gui/widgets/code_editor.py

import logging
import subprocess
import tempfile
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QTabWidget,
    QPushButton, QLabel, QComboBox, QSplitter, QProgressBar,
    QToolBar, QMessageBox, QFrame, QToolBar, QMessageBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread, pyqtSlot, QProcess
from PyQt6.QtGui import (
    QFont, QSyntaxHighlighter, QTextCharFormat, QColor,
    QTextCursor, QTextDocument, QPainter, QFontMetrics, QPalette
)

from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.formatters import get_formatter_by_name
from pygments.styles import get_all_styles

logger = logging.getLogger('TutorialAgent.CodeEditor')


class LineNumberArea(QWidget):
    """Line number area for the code editor."""

    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return self.code_editor.lineNumberAreaWidth()

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)


class PygmentsSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter using Pygments."""

    def __init__(self, document: QTextDocument, language: str = 'python'):
        super().__init__(document)
        self.language = language.lower()
        self.lexer = None
        self.formatter = None
        self.setup_highlighter()

    def setup_highlighter(self):
        """Setup Pygments lexer and formatter."""
        try:
            # Language mapping
            language_map = {
                'python': 'python',
                'javascript': 'javascript',
                'java': 'java',
                'csharp': 'csharp',
                'c#': 'csharp',
                'cpp': 'cpp',
                'c++': 'cpp'
            }

            lexer_name = language_map.get(self.language, 'text')
            self.lexer = get_lexer_by_name(lexer_name)

        except Exception as e:
            logger.warning(f"Could not setup syntax highlighting for {self.language}: {e}")
            self.lexer = get_lexer_by_name('text')

    def highlightBlock(self, text):
        """Highlight a block of text."""
        if not self.lexer or not text.strip():
            return

        try:
            # Define color schemes
            colors = {
                'Keyword': QColor('#569cd6'),  # Blue
                'String': QColor('#ce9178'),  # Orange
                'Comment': QColor('#6a9955'),  # Green
                'Number': QColor('#b5cea8'),  # Light green
                'Operator': QColor('#d4d4d4'),  # Light gray
                'Name.Function': QColor('#dcdcaa'),  # Yellow
                'Name.Class': QColor('#4ec9b0'),  # Cyan
                'Error': QColor('#f44747'),  # Red
            }

            # Tokenize the text
            tokens = list(self.lexer.get_tokens(text))

            index = 0
            for token_type, value in tokens:
                if not value.strip():
                    index += len(value)
                    continue

                # Create format
                format = QTextCharFormat()

                # Apply colors based on token type
                token_name = str(token_type)
                if token_name in colors:
                    format.setForeground(colors[token_name])
                elif 'Keyword' in token_name:
                    format.setForeground(colors['Keyword'])
                    format.setFontWeight(QFont.Weight.Bold)
                elif 'String' in token_name:
                    format.setForeground(colors['String'])
                elif 'Comment' in token_name:
                    format.setForeground(colors['Comment'])
                    format.setFontItalic(True)
                elif 'Number' in token_name:
                    format.setForeground(colors['Number'])
                elif 'Function' in token_name:
                    format.setForeground(colors['Name.Function'])
                elif 'Class' in token_name:
                    format.setForeground(colors['Name.Class'])
                elif 'Error' in token_name:
                    format.setForeground(colors['Error'])
                    format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)

                # Apply the format
                self.setFormat(index, len(value), format)
                index += len(value)

        except Exception as e:
            logger.debug(f"Error highlighting block: {e}")


class CodeExecutionThread(QThread):
    """Thread for executing code safely."""

    output_ready = pyqtSignal(str)
    error_ready = pyqtSignal(str)
    execution_finished = pyqtSignal(bool)  # success/failure

    def __init__(self, code: str, language: str):
        super().__init__()
        self.code = code
        self.language = language.lower()
        self.process = None

    def run(self):
        """Execute the code."""
        try:
            if self.language == 'python':
                self._execute_python()
            elif self.language == 'javascript':
                self._execute_javascript()
            elif self.language == 'java':
                self._execute_java()
            elif self.language in ['csharp', 'c#']:
                self._execute_csharp()
            elif self.language in ['cpp', 'c++']:
                self._execute_cpp()
            else:
                self.error_ready.emit(f"Execution not supported for {self.language}")
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
                timeout=10,
                cwd=os.path.dirname(temp_file)
            )

            if result.returncode == 0:
                self.output_ready.emit(result.stdout)
                self.execution_finished.emit(True)
            else:
                self.error_ready.emit(result.stderr)
                self.execution_finished.emit(False)

        finally:
            try:
                os.unlink(temp_file)
            except:
                pass

    def _execute_javascript(self):
        """Execute JavaScript code using Node.js."""
        # Check if Node.js is available
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
                self.output_ready.emit(result.stdout)
                self.execution_finished.emit(True)
            else:
                self.error_ready.emit(result.stderr)
                self.execution_finished.emit(False)

        finally:
            try:
                os.unlink(temp_file)
            except:
                pass

    def _execute_java(self):
        """Execute Java code."""
        # Create a temporary directory for Java files
        temp_dir = tempfile.mkdtemp()
        java_file = os.path.join(temp_dir, 'Main.java')

        try:
            # Write Java code
            with open(java_file, 'w') as f:
                f.write(self.code)

            # Compile
            compile_result = subprocess.run(
                ['javac', java_file],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=temp_dir
            )

            if compile_result.returncode != 0:
                self.error_ready.emit(f"Compilation error:\n{compile_result.stderr}")
                self.execution_finished.emit(False)
                return

            # Run
            run_result = subprocess.run(
                ['java', 'Main'],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=temp_dir
            )

            if run_result.returncode == 0:
                self.output_ready.emit(run_result.stdout)
                self.execution_finished.emit(True)
            else:
                self.error_ready.emit(run_result.stderr)
                self.execution_finished.emit(False)

        finally:
            # Cleanup
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

    def _execute_csharp(self):
        """Execute C# code using dotnet."""
        self.error_ready.emit("C# execution requires .NET SDK (not implemented yet)")
        self.execution_finished.emit(False)

    def _execute_cpp(self):
        """Execute C++ code using g++."""
        self.error_ready.emit("C++ execution requires g++ compiler (not implemented yet)")
        self.execution_finished.emit(False)


class EnhancedCodeEditor(QTextEdit):
    """Enhanced code editor with advanced features."""

    code_executed = pyqtSignal(bool, str)  # success, output
    content_changed = pyqtSignal()

    def __init__(self, language: str = 'python'):
        super().__init__()
        self.language = language.lower()
        self.setup_editor()
        self.setup_line_numbers()
        self.setup_auto_completion()

        # Syntax highlighter
        self.highlighter = PygmentsSyntaxHighlighter(self.document(), self.language)

        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.setSingleShot(True)

        # Connect signals
        self.textChanged.connect(self.on_text_changed)

    def setup_editor(self):
        """Setup the editor appearance and behavior."""
        # Font
        font = QFont("Consolas", 11)
        if not font.exactMatch():
            font = QFont("Courier New", 11)
        font.setFixedPitch(True)
        self.setFont(font)

        # Tab settings
        self.setTabStopDistance(40)  # 4 spaces

        # Line wrap
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        # Colors and styling
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                selection-background-color: #264f78;
                selection-color: #ffffff;
            }
        """)

    def setup_line_numbers(self):
        """Setup line number area."""
        self.line_number_area = LineNumberArea(self)

        # Connect signals for line number updates
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def setup_auto_completion(self):
        """Setup auto-completion keywords."""
        self.keywords = {
            'python': [
                'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except',
                'finally', 'import', 'from', 'return', 'yield', 'with', 'as', 'pass',
                'break', 'continue', 'lambda', 'global', 'nonlocal', 'assert', 'del',
                'print', 'len', 'range', 'enumerate', 'zip', 'map', 'filter', 'sum',
                'max', 'min', 'sorted', 'reversed', 'any', 'all', 'isinstance', 'type'
            ],
            'javascript': [
                'function', 'var', 'let', 'const', 'if', 'else', 'for', 'while',
                'switch', 'case', 'break', 'continue', 'return', 'try', 'catch',
                'finally', 'throw', 'new', 'this', 'typeof', 'instanceof',
                'console.log', 'console.error', 'document', 'window', 'setTimeout'
            ],
            'java': [
                'public', 'private', 'protected', 'class', 'interface', 'extends',
                'implements', 'static', 'final', 'abstract', 'if', 'else', 'for',
                'while', 'switch', 'case', 'break', 'continue', 'return', 'try',
                'catch', 'finally', 'throw', 'throws', 'new', 'this', 'super',
                'System.out.println', 'String', 'int', 'double', 'boolean', 'void'
            ]
        }

    def lineNumberAreaWidth(self):
        """Calculate width needed for line numbers."""
        digits = 1
        max_val = max(1, self.blockCount())
        while max_val >= 10:
            max_val //= 10
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        """Update the viewport margins for line numbers."""
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        """Update the line number area."""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()
        )

    def lineNumberAreaPaintEvent(self, event):
        """Paint the line number area."""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor('#2d2d30'))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(block_number + 1)
                painter.setPen(QColor('#858585'))
                painter.drawText(
                    0, int(top), self.line_number_area.width(), height,
                    Qt.AlignmentFlag.AlignRight, number
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlightCurrentLine(self):
        """Highlight the current line."""
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor('#2a2a2a')
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def keyPressEvent(self, event):
        """Handle key press events."""
        # Auto-indentation
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            cursor = self.textCursor()
            current_line = cursor.block().text()

            # Calculate indentation
            indent = 0
            for char in current_line:
                if char == ' ':
                    indent += 1
                elif char == '\t':
                    indent += 4
                else:
                    break

            # Add extra indent for certain keywords
            if current_line.strip().endswith(':'):
                indent += 4

            super().keyPressEvent(event)
            self.insertPlainText(' ' * indent)
            return

        # Auto-completion trigger
        elif event.key() == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            word = cursor.selectedText()

            if word in self.keywords.get(self.language, []):
                # Simple auto-completion
                pass

        super().keyPressEvent(event)

    def on_text_changed(self):
        """Handle text changes."""
        self.content_changed.emit()

        # Start auto-save timer
        self.auto_save_timer.start(2000)  # 2 seconds

    def auto_save(self):
        """Auto-save current content."""
        # Implement auto-save logic here
        logger.debug("Auto-saving code editor content")

    def set_language(self, language: str):
        """Set the programming language."""
        self.language = language.lower()
        self.highlighter = PygmentsSyntaxHighlighter(self.document(), self.language)

    def set_code(self, code: str):
        """Set the code content."""
        self.setPlainText(code)

    def get_code(self) -> str:
        """Get the current code content."""
        return self.toPlainText()

    def insert_code(self, code: str):
        """Insert code at current cursor position."""
        cursor = self.textCursor()
        cursor.insertText(code)

    def clear_editor(self):
        """Clear the editor content."""
        self.clear()


class CodeEditor(QWidget):
    """Main code editor widget with tabs and execution."""

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

        # Add initial editor
        self.add_new_tab()

        splitter.addWidget(self.tab_widget)

        # Create output area
        self.output_area = self.create_output_area()
        splitter.addWidget(self.output_area)

        # Set splitter proportions
        splitter.setStretchFactor(0, 3)  # Editor
        splitter.setStretchFactor(1, 1)  # Output

        layout.addWidget(splitter)

    def create_toolbar(self):
        """Create the editor toolbar."""
        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet("""
            QToolBar {
                background: #2d2d30;
                border: none;
                spacing: 5px;
                padding: 5px;
            }
            QPushButton {
                background: #0e639c;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px 10px;
                font-weight: bold;
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
                border-radius: 3px;
                padding: 3px 8px;
                min-width: 80px;
            }
        """)

        # Run button
        self.run_button = QPushButton("▶ Run")
        self.run_button.clicked.connect(self.run_code)
        self.toolbar.addWidget(self.run_button)

        # Language selector
        self.language_combo = QComboBox()
        self.language_combo.addItems(['Python', 'JavaScript', 'Java', 'C#', 'C++'])
        self.language_combo.currentTextChanged.connect(self.change_language)
        self.toolbar.addWidget(self.language_combo)

        # Add spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer)

        # Clear button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_editor)
        self.toolbar.addWidget(clear_button)

        # New tab button
        new_tab_button = QPushButton("+ New")
        new_tab_button.clicked.connect(self.add_new_tab)
        self.toolbar.addWidget(new_tab_button)

    def create_output_area(self):
        """Create the output display area."""
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        output_layout.setContentsMargins(5, 5, 5, 5)

        # Output label
        output_label = QLabel("Output:")
        output_label.setStyleSheet("color: #d4d4d4; font-weight: bold; margin-bottom: 5px;")
        output_layout.addWidget(output_label)

        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(200)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #0c0c0c;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10pt;
            }
        """)
        output_layout.addWidget(self.output_text)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3e3e3e;
                border-radius: 3px;
                text-align: center;
                background: #2d2d30;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #0e639c;
                border-radius: 2px;
            }
        """)
        output_layout.addWidget(self.progress_bar)

        return output_widget

    def add_new_tab(self, title: str = None):
        """Add a new editor tab."""
        if title is None:
            title = f"untitled_{self.tab_widget.count() + 1}.py"

        editor = EnhancedCodeEditor(self.current_language)
        editor.content_changed.connect(self.on_content_changed)

        self.tab_widget.addTab(editor, title)
        self.tab_widget.setCurrentWidget(editor)

        return editor

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
            'csharp': 'C#',
            'c#': 'C#',
            'cpp': 'C++',
            'c++': 'C++'
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
            'C#': 'csharp',
            'C++': 'cpp'
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
        self.output_text.setPlainText("Executing...")

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
                font-size: 10pt;
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
                font-size: 10pt;
            }
        """)

    @pyqtSlot(bool)
    def execution_finished(self, success: bool):
        """Handle execution completion."""
        self.run_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.code_executed.emit(success, self.output_text.toPlainText())

    def on_content_changed(self):
        """Handle editor content changes."""
        # Update tab title to indicate unsaved changes
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            current_title = self.tab_widget.tabText(current_index)
            if not current_title.endswith('*'):
                self.tab_widget.setTabText(current_index, current_title + '*')