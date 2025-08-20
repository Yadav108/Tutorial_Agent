#!/usr/bin/env python3
"""
Tutorial Agent Application Runner

Enhanced application launcher with proper error handling, logging setup,
and dependency management.
"""

import sys
import os
import logging
import traceback
import argparse
from pathlib import Path
from typing import Optional

# Early path setup
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

# Import after path setup
from utils.logging_setup import setup_logging
from utils.error_handler import setup_global_exception_handler
from config.settings_manager import get_settings_manager

logger = logging.getLogger('TutorialAgent')


def check_dependencies() -> bool:
    """Check if all required dependencies are available."""
    # Use correct package import names (case-sensitive)
    required_packages = {
        'PyQt6': 'PyQt6',
        'sqlalchemy': 'SQLAlchemy', 
        'yaml': 'PyYAML',
        'pygments': 'Pygments'
    }
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        logger.error(f"Missing required packages: {missing_packages}")
        return False
    
    return True


def setup_environment() -> bool:
    """Setup necessary environment variables and paths."""
    try:
        # Create required directories
        required_dirs = [
            project_root / 'assets' / 'icons',
            project_root / 'logs',
            project_root / 'cache',
            project_root / 'data'
        ]
        
        for directory in required_dirs:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")

        logger.info(f"Project root: {project_root}")
        logger.info("Environment setup completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error setting up environment: {str(e)}", exc_info=True)
        return False


def setup_assets() -> bool:
    """Setup assets directory and icons."""
    try:
        icons_dir = project_root / 'assets' / 'icons'
        icons_dir.mkdir(parents=True, exist_ok=True)

        # Check for required icons
        required_icons = ['python.svg', 'javascript.svg', 'csharp.svg', 'java.svg', 'cpp.svg', 'search.svg']
        missing_icons = [icon for icon in required_icons
                         if not (icons_dir / icon).exists()]

        if missing_icons:
            logger.warning(f"Missing icons: {missing_icons}")
            # Create placeholder SVG files if they don't exist
            create_placeholder_icons(icons_dir, missing_icons)

        logger.info("Assets setup completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error setting up assets: {str(e)}", exc_info=True)
        return False


def create_placeholder_icons(icons_dir: Path, missing_icons: list):
    """Create placeholder SVG icons for missing icons."""
    placeholder_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <path d="m9 9 6 6"/>
        <path d="m15 9-6 6"/>
    </svg>'''
    
    for icon in missing_icons:
        icon_path = icons_dir / icon
        try:
            with open(icon_path, 'w', encoding='utf-8') as f:
                f.write(placeholder_svg)
            logger.debug(f"Created placeholder icon: {icon}")
        except Exception as e:
            logger.warning(f"Could not create placeholder icon {icon}: {e}")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Tutorial Agent - Interactive Programming Learning Platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python run.py                    # Run with default settings
  python run.py --debug            # Run with debug logging
  python run.py --config custom    # Use custom config file
  python run.py --reset-settings   # Reset all settings to defaults
        '''
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true', 
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--config', 
        type=str, 
        help='Path to custom config file'
    )
    
    parser.add_argument(
        '--reset-settings', 
        action='store_true', 
        help='Reset all settings to defaults'
    )
    
    parser.add_argument(
        '--no-gui', 
        action='store_true', 
        help='Run in CLI mode (future feature)'
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='Tutorial Agent 1.0.0'
    )
    
    return parser.parse_args()


def initialize_application(args: argparse.Namespace) -> bool:
    """Initialize the application with given arguments."""
    try:
        # Setup logging
        log_level = logging.DEBUG if args.debug else logging.INFO
        setup_logging(
            log_file=project_root / 'logs' / 'tutorial_agent.log',
            level=log_level
        )
        
        # Setup global exception handling
        setup_global_exception_handler()
        
        # Check dependencies
        if not check_dependencies():
            show_error_dialog("Missing Dependencies", 
                            "Some required packages are missing. Please run:\npip install -r requirements.txt")
            return False
        
        # Setup environment
        if not setup_environment():
            show_error_dialog("Environment Error", 
                            "Failed to setup application environment. Check logs for details.")
            return False
        
        # Setup assets
        if not setup_assets():
            logger.warning("Assets setup failed, but continuing anyway")
        
        # Initialize settings
        settings_manager = get_settings_manager()
        if args.reset_settings:
            settings_manager.reset_to_defaults()
            logger.info("Settings reset to defaults")
        
        logger.info("Application initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}", exc_info=True)
        return False


def show_error_dialog(title: str, message: str):
    """Show error dialog without requiring full app initialization."""
    try:
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        
    except Exception as e:
        # Fallback to console output
        print(f"ERROR: {title}")
        print(f"MESSAGE: {message}")
        print(f"DISPLAY ERROR: {e}")


def main():
    """Main application entry point."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Initialize application
        if not initialize_application(args):
            return 1
        
        # Handle no-gui mode (future feature)
        if args.no_gui:
            print("CLI mode is not yet implemented")
            return 0
        
        logger.info("Starting Tutorial Agent GUI application")
        
        # Create and configure Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("Tutorial Agent")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Aryan Yadav")
        app.setOrganizationDomain("tutorial-agent.dev")
        app.setStyle('Fusion')
        
        # Import GUI after Qt app is created
        from gui.main_window import MainWindow
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("GUI application started successfully")
        
        # Run the application event loop
        result = app.exec()
        
        logger.info("Application shutting down")
        return result

    except ImportError as e:
        logger.error(f"Import error: {e}")
        show_error_dialog("Import Error", f"Failed to import required modules:\n{e}")
        return 1
    
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        show_error_dialog("Startup Error", f"Application failed to start:\n{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
