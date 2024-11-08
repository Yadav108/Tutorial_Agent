"""Set up project directory structure."""
import os
import shutil
from pathlib import Path


def create_directory_structure():
    """Create the project directory structure."""
    # Get the current directory where setup_structure.py is located
    base_dir = Path.cwd()
    print(f"Creating project structure in: {base_dir}")

    # Define the directory structure with files
    structure = {
        'gui': {
            '__init__.py': '''"""GUI package initialization."""
from .main_window import MainWindow
__all__ = ['MainWindow']''',

            'main_window.py': '''"""Main window implementation."""
from PyQt6.QtWidgets import QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tutorial Agent")
        self.setMinimumSize(1200, 800)''',

            'widgets': {
                '__init__.py': '''"""GUI widgets package."""''',
                'sidebar.py': '''"""Sidebar widget implementation."""
from PyQt6.QtWidgets import QWidget
class Sidebar(QWidget):
    def __init__(self):
        super().__init__()''',

                'content_viewer.py': '''"""Content viewer widget."""
from PyQt6.QtWidgets import QWidget
class ContentViewer(QWidget):
    def __init__(self):
        super().__init__()''',

                'code_editor.py': '''"""Code editor widget."""
from PyQt6.QtWidgets import QWidget
class CodeEditor(QWidget):
    def __init__(self):
        super().__init__()''',

                'quiz_widget.py': '''"""Quiz widget implementation."""
from PyQt6.QtWidgets import QWidget
class QuizWidget(QWidget):
    def __init__(self):
        super().__init__()'''
            },
            'dialogs': {
                '__init__.py': '''"""GUI dialogs package."""''',
                'settings_dialog.py': '''"""Settings dialog."""
from PyQt6.QtWidgets import QDialog
class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()''',

                'about_dialog.py': '''"""About dialog."""
from PyQt6.QtWidgets import QDialog
class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()''',

                'notification_dialog.py': '''"""Notification dialog."""
from PyQt6.QtWidgets import QDialog
class NotificationDialog(QDialog):
    def __init__(self):
        super().__init__()'''
            }
        },
        'database': {
            '__init__.py': '''"""Database package."""''',
            'models': {
                '__init__.py': '''"""Database models package."""''',
            }
        },
        'services': {
            '__init__.py': '''"""Services package."""''',
        },
        'config': {
            '__init__.py': '''"""Configuration package."""''',
        },
        'assets': {
            'images': {},
            'styles': {}
        }
    }

    def create_directories(parent_path, struct):
        """Recursively create directories and files."""
        for name, content in struct.items():
            path = parent_path / name

            if isinstance(content, dict):
                # Create directory
                path.mkdir(exist_ok=True)
                print(f"Created directory: {path}")
                create_directories(path, content)
            else:
                # Create file with content
                path.write_text(content)
                print(f"Created file: {path}")

    try:
        # Create the directory structure
        create_directories(base_dir, structure)

        # Create run.py in the root directory
        run_py_content = '''"""Application entry point."""
import sys
from PyQt6.QtWidgets import QApplication
from gui import MainWindow

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
'''
        run_py_path = base_dir / 'run.py'
        run_py_path.write_text(run_py_content)
        print(f"Created file: {run_py_path}")

        print("\nProject structure created successfully!")

    except Exception as e:
        print(f"Error creating project structure: {str(e)}")


if __name__ == "__main__":
    create_directory_structure()