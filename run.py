# run.py

import sys
import os
import logging
import traceback
from pathlib import Path

from PyQt6.QtWidgets import QApplication

# Setup logging first
from gui import MainWindow

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tutorial_agent.log', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('TutorialAgent')


def setup_environment():
    """Setup necessary environment variables and paths."""
    try:
        # Add the project root to Python path
        project_root = os.path.dirname(os.path.abspath(__file__))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        # Create assets directory if it doesn't exist
        assets_dir = os.path.join(project_root, 'assets', 'icons')
        os.makedirs(assets_dir, exist_ok=True)

        logger.info(f"Project root: {project_root}")
        logger.info(f"Assets directory: {assets_dir}")

    except Exception as e:
        logger.error(f"Error setting up environment: {str(e)}", exc_info=True)
        raise


def exception_hook(exctype, value, tb):
    """Global exception handler to log unhandled exceptions."""
    logger.critical(''.join(traceback.format_exception(exctype, value, tb)))
    sys.__excepthook__(exctype, value, tb)  # Call the default handler


# In your run.py, add:

def setup_assets():
    """Setup assets directory and icons."""
    try:
        # Create assets directory
        icons_dir = Path(__file__).parent / 'assets' / 'icons'
        icons_dir.mkdir(parents=True, exist_ok=True)

        # Check for required icons
        required_icons = ['python.svg', 'javascript.svg', 'csharp.svg']
        missing_icons = [icon for icon in required_icons
                         if not (icons_dir / icon).exists()]

        if missing_icons:
            logger.warning(f"Missing icons: {missing_icons}")

    except Exception as e:
        logger.error(f"Error setting up assets: {str(e)}", exc_info=True)


def main():
    try:
        logger.info("Starting Tutorial Agent application")

        # Setup environment
        setup_environment()
        setup_assets()

        # Create application
        app = QApplication(sys.argv)
        window = MainWindow()
        app.setStyle('Fusion')
        window.show()

        logger.info("Application started successfully")
        return app.exec()

    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())