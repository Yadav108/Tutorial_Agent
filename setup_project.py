#!/usr/bin/env python3
"""
Tutorial Agent Project Setup Script

This script sets up the Tutorial Agent project structure, creates necessary
directories, downloads assets, and initializes the database.
"""

import os
import sys
import shutil
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Any
import json
import urllib.request
import urllib.error


def setup_logging():
    """Setup basic logging for setup script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('TutorialAgent.Setup')


logger = setup_logging()


class ProjectSetup:
    """Main project setup class."""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.absolute()
        self.errors = []
        
    def run_setup(self):
        """Run the complete project setup."""
        logger.info("Starting Tutorial Agent project setup...")
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Creating directory structure", self.create_directories),
            ("Installing dependencies", self.install_dependencies),
            ("Setting up assets", self.setup_assets),
            ("Creating configuration files", self.create_config_files),
            ("Initializing database", self.setup_database),
            ("Setting up development tools", self.setup_dev_tools),
            ("Running tests", self.run_basic_tests)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"Running: {step_name}")
            try:
                step_func()
                logger.info(f"✓ {step_name} completed successfully")
            except Exception as e:
                error_msg = f"✗ {step_name} failed: {e}"
                logger.error(error_msg)
                self.errors.append(error_msg)
        
        # Summary
        if self.errors:
            logger.error(f"Setup completed with {len(self.errors)} errors:")
            for error in self.errors:
                logger.error(f"  - {error}")
            return False
        else:
            logger.info("🎉 Project setup completed successfully!")
            return True
    
    def check_python_version(self):
        """Check if Python version meets requirements."""
        min_version = (3, 8)
        current_version = sys.version_info[:2]
        
        if current_version < min_version:
            raise RuntimeError(
                f"Python {min_version[0]}.{min_version[1]}+ required. "
                f"Current version: {current_version[0]}.{current_version[1]}"
            )
        
        logger.info(f"Python version check passed: {sys.version}")
    
    def create_directories(self):
        """Create necessary project directories."""
        directories = [
            'assets/icons',
            'assets/images', 
            'assets/styles',
            'logs',
            'cache',
            'data',
            'config',
            'content/languages/python',
            'content/languages/javascript',
            'content/languages/csharp', 
            'content/languages/java',
            'content/languages/cpp',
            'content/exercises/python',
            'content/exercises/javascript',
            'content/exercises/csharp',
            'content/exercises/java',
            'content/exercises/cpp',
            'database/migrations',
            'tests/test_data',
            'docs/user_guide',
            'docs/developer_guide',
            'docs/api'
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {directory}")
    
    def install_dependencies(self):
        """Install Python dependencies."""
        requirements_file = self.project_root / 'requirements.txt'
        
        if not requirements_file.exists():
            logger.warning("requirements.txt not found, skipping dependency installation")
            return
        
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ], check=True, capture_output=True, text=True)
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install dependencies: {e.stderr}")
    
    def setup_assets(self):
        """Setup application assets."""
        self.create_placeholder_icons()
        self.create_default_styles()
    
    def create_placeholder_icons(self):
        """Create placeholder SVG icons."""
        icons = {
            'python.svg': self.create_python_icon(),
            'javascript.svg': self.create_javascript_icon(),
            'csharp.svg': self.create_csharp_icon(),
            'java.svg': self.create_java_icon(),
            'cpp.svg': self.create_cpp_icon(),
            'search.svg': self.create_search_icon()
        }
        
        icons_dir = self.project_root / 'assets' / 'icons'
        
        for filename, content in icons.items():
            icon_path = icons_dir / filename
            with open(icon_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.debug(f"Created icon: {filename}")
    
    def create_python_icon(self) -> str:
        return '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L2 7v10l10 5 10-5V7l-10-5z" fill="#3776ab" stroke="#3776ab" stroke-width="1"/>
            <path d="M12 7v10" stroke="white" stroke-width="2"/>
            <path d="M8 9h8" stroke="white" stroke-width="1"/>
        </svg>'''
    
    def create_javascript_icon(self) -> str:
        return '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <rect x="2" y="2" width="20" height="20" rx="2" fill="#f7df1e"/>
            <path d="M8 16v-3c0-1 .5-1.5 1.5-1.5s1.5.5 1.5 1.5v3" stroke="#000" stroke-width="2" fill="none"/>
            <path d="M13 12h2.5c1 0 1.5.5 1.5 1.5s-.5 1.5-1.5 1.5H15" stroke="#000" stroke-width="2" fill="none"/>
        </svg>'''
    
    def create_csharp_icon(self) -> str:
        return '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <rect x="2" y="2" width="20" height="20" rx="2" fill="#512bd4"/>
            <text x="12" y="16" text-anchor="middle" fill="white" font-family="monospace" font-size="12">C#</text>
        </svg>'''
    
    def create_java_icon(self) -> str:
        return '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <rect x="2" y="2" width="20" height="20" rx="2" fill="#ed8b00"/>
            <text x="12" y="16" text-anchor="middle" fill="white" font-family="monospace" font-size="10" font-weight="bold">JAVA</text>
        </svg>'''
    
    def create_cpp_icon(self) -> str:
        return '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <rect x="2" y="2" width="20" height="20" rx="2" fill="#00599c"/>
            <text x="12" y="16" text-anchor="middle" fill="white" font-family="monospace" font-size="9" font-weight="bold">C++</text>
        </svg>'''
    
    def create_search_icon(self) -> str:
        return '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
            <path d="21 21l-4.35-4.35" stroke="currentColor" stroke-width="2"/>
        </svg>'''
    
    def create_default_styles(self):
        """Create default application styles."""
        styles_dir = self.project_root / 'assets' / 'styles'
        
        # Light theme
        light_style = '''
        /* Tutorial Agent Light Theme */
        QMainWindow {
            background-color: #ffffff;
            color: #333333;
        }
        
        QWidget {
            background-color: #ffffff;
            color: #333333;
            font-family: "Segoe UI", Arial, sans-serif;
        }
        
        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #0056b3;
        }
        
        QPushButton:pressed {
            background-color: #004085;
        }
        '''
        
        # Dark theme
        dark_style = '''
        /* Tutorial Agent Dark Theme */
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            font-family: "Segoe UI", Arial, sans-serif;
        }
        
        QPushButton {
            background-color: #0d6efd;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #0b5ed7;
        }
        
        QPushButton:pressed {
            background-color: #0a58ca;
        }
        '''
        
        with open(styles_dir / 'light_theme.qss', 'w', encoding='utf-8') as f:
            f.write(light_style)
            
        with open(styles_dir / 'dark_theme.qss', 'w', encoding='utf-8') as f:
            f.write(dark_style)
    
    def create_config_files(self):
        """Create default configuration files."""
        config_dir = self.project_root / 'config'
        
        # Default settings
        default_settings = {
            "editor": {
                "font_family": "Consolas",
                "font_size": 12,
                "theme": "vscode_dark",
                "show_line_numbers": True,
                "word_wrap": False,
                "tab_size": 4,
                "auto_indent": True
            },
            "ui": {
                "theme": "light",
                "language": "en",
                "window_maximized": False,
                "window_width": 1400,
                "window_height": 900
            },
            "learning": {
                "auto_save_progress": True,
                "show_progress_notifications": True,
                "enable_achievements": True,
                "preferred_languages": ["python"]
            }
        }
        
        settings_file = config_dir / 'default_settings.json'
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, indent=2)
    
    def setup_database(self):
        """Initialize the database."""
        # Create database directory
        db_dir = self.project_root / 'database'
        db_dir.mkdir(exist_ok=True)
        
        # The actual database initialization will be handled by the application
        logger.info("Database directory created - initialization will occur on first run")
    
    def setup_dev_tools(self):
        """Setup development tools configuration."""
        # Create .gitignore if it doesn't exist
        gitignore_content = '''
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Application
tutorial_agent.log*
*.db
*.sqlite
*.sqlite3
cache/
logs/
user_progress.json

# OS
.DS_Store
Thumbs.db
'''
        
        gitignore_path = self.project_root / '.gitignore'
        if not gitignore_path.exists():
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
    
    def run_basic_tests(self):
        """Run basic tests to verify setup."""
        # Test imports
        test_imports = [
            'PyQt6.QtWidgets',
            'SQLAlchemy', 
            'yaml',
            'pygments'
        ]
        
        for module_name in test_imports:
            try:
                __import__(module_name)
                logger.debug(f"Import test passed: {module_name}")
            except ImportError as e:
                raise RuntimeError(f"Import test failed for {module_name}: {e}")


def main():
    """Main setup function."""
    project_root = Path(__file__).parent.absolute()
    setup = ProjectSetup(project_root)
    
    success = setup.run_setup()
    
    if success:
        print("\n" + "="*50)
        print("🎉 Tutorial Agent setup completed successfully!")
        print("="*50)
        print()
        print("Next steps:")
        print("1. Run the application: python run.py")
        print("2. Or run with debug mode: python run.py --debug")
        print("3. For help: python run.py --help")
        print()
        return 0
    else:
        print("\n" + "="*50)
        print("❌ Setup completed with errors")
        print("="*50)
        print()
        print("Please check the error messages above and fix any issues.")
        return 1


if __name__ == '__main__':
    sys.exit(main())