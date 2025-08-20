"""
Service layer components for Tutorial Agent

This package provides service layer components that handle business logic
and data operations for the Tutorial Agent application.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import services from original location
try:
    from services.auth_service import AuthService
    from services.content_service import ContentService  
    from services.quiz_service import QuizService
    from services.progress_service import ProgressService
except ImportError:
    # Fallback for development
    class AuthService:
        def __init__(self):
            pass
    
    class ContentService:
        def __init__(self):
            pass
            
    class QuizService:
        def __init__(self):
            pass
            
    class ProgressService:
        def __init__(self):
            pass

# Service registry
_service_registry = {}

def register_service(name: str, service_instance):
    """Register a service instance."""
    _service_registry[name] = service_instance

def get_service(name: str):
    """Get a registered service instance."""
    return _service_registry.get(name)

def init_services():
    """Initialize all services."""
    # Register default services
    register_service('auth', AuthService())
    register_service('content', ContentService())
    register_service('quiz', QuizService())
    register_service('progress', ProgressService())
    
    # Initialize each service
    for service in _service_registry.values():
        if hasattr(service, 'initialize'):
            service.initialize()

def cleanup_services():
    """Cleanup all services."""
    for service in _service_registry.values():
        if hasattr(service, 'cleanup'):
            service.cleanup()
    _service_registry.clear()

# Export all components
__all__ = [
    "AuthService",
    "ContentService",
    "QuizService", 
    "ProgressService",
    "register_service",
    "get_service",
    "init_services",
    "cleanup_services"
]