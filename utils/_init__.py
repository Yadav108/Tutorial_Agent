"""
Utility functions and helpers for Tutorial Agent
"""

from .content_loader import ContentLoader
from .quiz_handler import QuizHandler
from .code_runner import CodeRunner
from .helpers.file_helpers import FileHelper
from .helpers.string_helpers import StringHelper

# Create global utility instances
content_loader = ContentLoader()
quiz_handler = QuizHandler()
code_runner = CodeRunner()
file_helper = FileHelper()
string_helper = StringHelper()


# Utility functions
def setup_logging():
    """Setup application logging"""
    import logging
    from pathlib import Path

    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'tutorial_agent.log'),
            logging.StreamHandler()
        ]
    )


def cleanup_temp_files():
    """Clean up temporary files"""
    file_helper.cleanup_temp_files()


def get_version():
    """Get application version"""
    from .. import VERSION_INFO
    version = '{major}.{minor}.{patch}'.format(**VERSION_INFO)
    if VERSION_INFO['release'] != 'final':
        version = f"{version}-{VERSION_INFO['release']}"
    return version


# Export utility components
__all__ = [
    'ContentLoader',
    'QuizHandler',
    'CodeRunner',
    'FileHelper',
    'StringHelper',
    'content_loader',
    'quiz_handler',
    'code_runner',
    'file_helper',
    'string_helper',
    'setup_logging',
    'cleanup_temp_files',
    'get_version'
]

# Initialize logging
setup_logging()