"""
Tutorial Agent - Interactive Programming Learning Platform

A comprehensive learning platform for multiple programming languages including
Python, C++, C#, Java, and JavaScript with interactive tutorials, code execution,
quizzes, and progress tracking.

Author: Aryan Yadav
Email: yadavaryan2073@gmail.com
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Aryan Yadav"
__email__ = "yadavaryan2073@gmail.com"
__description__ = "Interactive Programming Learning Platform"

# Core imports
from .core import (
    TutorialAgent,
    ContentManager,
    ProgressManager,
    SettingsManager
)

# Service imports
from .services import (
    AuthService,
    ContentService,
    QuizService,
    ProgressService
)

# Export main components
__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__description__",
    "TutorialAgent",
    "ContentManager",
    "ProgressManager",
    "SettingsManager",
    "AuthService",
    "ContentService", 
    "QuizService",
    "ProgressService"
]