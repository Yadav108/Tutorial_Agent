"""
Service layer components for Tutorial Agent
"""

from .auth_service import AuthService
from .content_service import ContentService
from .quiz_service import QuizService
from .progress_service import ProgressService

# Create global service instances
auth_service = AuthService()
content_service = ContentService()
quiz_service = QuizService()
progress_service = ProgressService()

# Service status constants
SERVICE_STATUS = {
    'READY': 'ready',
    'INITIALIZING': 'initializing',
    'ERROR': 'error',
    'MAINTENANCE': 'maintenance'
}


def init_services():
    """Initialize all services"""
    services = [
        auth_service,
        content_service,
        quiz_service,
        progress_service
    ]

    for service in services:
        if hasattr(service, 'init'):
            service.init()


def cleanup_services():
    """Cleanup and close all services"""
    services = [
        auth_service,
        content_service,
        quiz_service,
        progress_service
    ]

    for service in services:
        if hasattr(service, 'cleanup'):
            service.cleanup()


# Export service components
__all__ = [
    'AuthService',
    'ContentService',
    'QuizService',
    'ProgressService',
    'auth_service',
    'content_service',
    'quiz_service',
    'progress_service',
    'init_services',
    'cleanup_services',
    'SERVICE_STATUS'
]