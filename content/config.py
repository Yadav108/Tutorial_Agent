# content/config.py

from pathlib import Path

# Base directory configuration
CONTENT_DIR = Path(__file__).parent
LANGUAGES_DIR = CONTENT_DIR / 'languages'
RESOURCES_DIR = CONTENT_DIR / 'resources'
USER_DATA_DIR = CONTENT_DIR / 'user_data'

# Content settings
MAX_ATTEMPTS_PER_EXERCISE = 3
CODE_EXECUTION_TIMEOUT = 5  # seconds
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Language-specific settings
LANGUAGE_CONFIGS = {
    'python': {
        'version': '3.8+',
        'file_extension': '.py',
        'comment_symbol': '#',
        'execution_command': 'python'
    },
    'javascript': {
        'version': 'ES6+',
        'file_extension': '.js',
        'comment_symbol': '//',
        'execution_command': 'node'
    },
    'csharp': {
        'version': '9.0',
        'file_extension': '.cs',
        'comment_symbol': '//',
        'execution_command': 'dotnet run'
    }
}

# Exercise settings
EXERCISE_DIFFICULTY_WEIGHTS = {
    'BEGINNER': 1,
    'INTERMEDIATE': 2,
    'ADVANCED': 3
}

# Progress tracking settings
COMPLETION_THRESHOLD = 80  # percentage
MASTERY_THRESHOLD = 95  # percentage

# Resource types
RESOURCE_TYPES = [
    'documentation',
    'tutorial',
    'video',
    'article',
    'tool',
    'book',
    'practice'
]

# File type validations
ALLOWED_FILE_TYPES = {
    'code': ['.py', '.js', '.cs', '.java', '.cpp', '.html', '.css'],
    'images': ['.png', '.jpg', '.jpeg', '.gif', '.svg'],
    'documents': ['.pdf', '.md', '.txt']
}

# UI related settings
CODE_EDITOR_THEMES = {
    'light': {
        'background': '#ffffff',
        'foreground': '#2d3436',
        'selection': '#b2bec3',
        'comment': '#636e72',
        'keyword': '#0984e3',
        'string': '#00b894',
        'number': '#e17055',
        'operator': '#6c5ce7'
    },
    'dark': {
        'background': '#2d3436',
        'foreground': '#dfe6e9',
        'selection': '#636e72',
        'comment': '#b2bec3',
        'keyword': '#74b9ff',
        'string': '#55efc4',
        'number': '#fab1a0',
        'operator': '#a29bfe'
    }
}

# Tutorial content structure
TOPIC_STRUCTURE = [
    'description',
    'prerequisites',
    'learning_objectives',
    'content',
    'examples',
    'exercises',
    'quiz',
    'additional_resources'
]

# Define paths for various content types
def get_language_path(language: str) -> Path:
    """Get the path for a specific language's content."""
    return LANGUAGES_DIR / language.lower()

def get_resource_path(language: str, resource_type: str) -> Path:
    """Get the path for language-specific resources."""
    return RESOURCES_DIR / language.lower() / resource_type

def get_user_data_path(username: str) -> Path:
    """Get the path for user-specific data."""
    return USER_DATA_DIR / username

# Ensure required directories exist
def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        LANGUAGES_DIR,
        RESOURCES_DIR,
        USER_DATA_DIR
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize directories when module is imported
ensure_directories()