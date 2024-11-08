"""
Constants for Tutorial Agent
"""

import os
from pathlib import Path

# Application Information
APP_NAME = "Tutorial Agent"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Tutorial Agent Team"
APP_DESCRIPTION = "An interactive programming learning platform"

# Directory Paths
ROOT_DIR = Path(__file__).parent.parent
CONTENT_DIR = ROOT_DIR / 'content'
DATABASE_DIR = ROOT_DIR / 'database'
LOGS_DIR = ROOT_DIR / 'logs'
TEMP_DIR = ROOT_DIR / 'temp'
USER_DATA_DIR = ROOT_DIR / 'user_data'
ASSETS_DIR = ROOT_DIR / 'assets'

# File Paths
DATABASE_PATH = DATABASE_DIR / 'tutorial_agent.db'
LOG_FILE = LOGS_DIR / 'tutorial_agent.log'
SETTINGS_FILE = USER_DATA_DIR / 'settings.json'

# Content Structure
DIFFICULTY_LEVELS = {
    'BEGINNER': 'beginner',
    'INTERMEDIATE': 'intermediate',
    'ADVANCED': 'advanced'
}

# Supported Programming Languages
LANGUAGES = {
    'python': {
        'name': 'Python',
        'extension': '.py',
        'icon': 'python.png',
        'version': '3.8+',
        'compiler_command': 'python'
    },
    'cpp': {
        'name': 'C++',
        'extension': '.cpp',
        'icon': 'cpp.png',
        'version': 'C++17',
        'compiler_command': 'g++'
    },
    'csharp': {
        'name': 'C#',
        'extension': '.cs',
        'icon': 'csharp.png',
        'version': '8.0',
        'compiler_command': 'dotnet'
    },
    'java': {
        'name': 'Java',
        'extension': '.java',
        'icon': 'java.png',
        'version': '11',
        'compiler_command': 'javac'
    }
}

# GUI Constants
GUI = {
    'WINDOW_SIZE': (1200, 800),
    'WINDOW_MIN_SIZE': (800, 600),
    'SIDEBAR_WIDTH': 300,
    'CODE_EDITOR_FONT_SIZE': 12,
    'DEFAULT_FONT_FAMILY': 'Consolas',
    'ICON_SIZE': 24
}

# Editor Settings
EDITOR = {
    'TAB_SIZE': 4,
    'AUTO_INDENT': True,
    'LINE_NUMBERS': True,
    'HIGHLIGHT_CURRENT_LINE': True,
    'WORD_WRAP': True,
    'AUTO_COMPLETE': True,
    'BRACKET_MATCHING': True
}

# Theme Colors
COLORS = {
    'light': {
        'primary': '#3498db',
        'secondary': '#2ecc71',
        'background': '#ffffff',
        'text': '#2c3e50',
        'border': '#bdc3c7',
        'error': '#e74c3c',
        'warning': '#f1c40f',
        'success': '#2ecc71'
    },
    'dark': {
        'primary': '#2980b9',
        'secondary': '#27ae60',
        'background': '#2c3e50',
        'text': '#ecf0f1',
        'border': '#34495e',
        'error': '#c0392b',
        'warning': '#f39c12',
        'success': '#27ae60'
    }
}

# Quiz Settings
QUIZ = {
    'TIME_LIMIT': 300,  # seconds
    'PASSING_SCORE': 70,  # percentage
    'MAX_ATTEMPTS': 3,
    'SHOW_CORRECT_ANSWERS': False,
    'RANDOMIZE_QUESTIONS': True
}

# Learning Settings
LEARNING = {
    'DAILY_GOAL': 60,  # minutes
    'REMINDER_INTERVAL': 24,  # hours
    'STREAK_THRESHOLD': 5,  # days
    'POINTS_PER_LESSON': 10,
    'POINTS_PER_QUIZ': 20,
    'POINTS_PER_EXERCISE': 15
}

# Authentication Settings
AUTH = {
    'TOKEN_EXPIRY': 24 * 60 * 60,  # 24 hours in seconds
    'MIN_PASSWORD_LENGTH': 8,
    'REQUIRE_SPECIAL_CHAR': True,
    'REQUIRE_NUMBER': True,
    'MAX_LOGIN_ATTEMPTS': 5,
    'LOCKOUT_DURATION': 15 * 60  # 15 minutes in seconds
}

# Cache Settings
CACHE = {
    'MAX_SIZE': 100 * 1024 * 1024,  # 100MB
    'EXPIRATION': 60 * 60,  # 1 hour in seconds
    'CLEAN_INTERVAL': 24 * 60 * 60  # 24 hours in seconds
}

# API Settings
API = {
    'BASE_URL': 'http://api.tutorialagent.com',
    'VERSION': 'v1',
    'TIMEOUT': 30,  # seconds
    'MAX_RETRIES': 3,
    'RETRY_DELAY': 1  # second
}

# Logging Settings
LOGGING = {
    'LEVEL': 'INFO',
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'DATE_FORMAT': '%Y-%m-%d %H:%M:%S',
    'MAX_SIZE': 10 * 1024 * 1024,  # 10MB
    'BACKUP_COUNT': 5
}

# Performance Settings
PERFORMANCE = {
    'MAX_THREADS': 4,
    'CHUNK_SIZE': 8192,
    'MAX_MEMORY': 512 * 1024 * 1024,  # 512MB
    'CLEANUP_INTERVAL': 60 * 60  # 1 hour in seconds
}

# Error Messages
ERROR_MESSAGES = {
    'AUTH_FAILED': 'Authentication failed. Please check your credentials.',
    'INVALID_INPUT': 'Invalid input provided. Please check your input and try again.',
    'NOT_FOUND': 'The requested resource was not found.',
    'SERVER_ERROR': 'An unexpected error occurred. Please try again later.',
    'PERMISSION_DENIED': 'You do not have permission to perform this action.',
    'INVALID_FILE': 'Invalid file format or corrupted file.',
    'DATABASE_ERROR': 'Database operation failed. Please try again.',
    'NETWORK_ERROR': 'Network connection error. Please check your connection.'
}

# Success Messages
SUCCESS_MESSAGES = {
    'LOGIN_SUCCESS': 'Successfully logged in.',
    'LOGOUT_SUCCESS': 'Successfully logged out.',
    'SAVE_SUCCESS': 'Changes saved successfully.',
    'DELETE_SUCCESS': 'Successfully deleted.',
    'UPDATE_SUCCESS': 'Successfully updated.',
    'QUIZ_COMPLETE': 'Quiz completed successfully.',
    'EXERCISE_COMPLETE': 'Exercise completed successfully.'
}

# Create required directories
for directory in [CONTENT_DIR, DATABASE_DIR, LOGS_DIR, TEMP_DIR, USER_DATA_DIR, ASSETS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)