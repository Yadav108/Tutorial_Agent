"""
Services test suite for Tutorial Agent
"""

import pytest
from pathlib import Path
import tempfile
import json
from typing import Dict, Any
from unittest.mock import Mock, MagicMock, patch


class ServicesTestCase:
    """Base class for service tests"""

    def setup_method(self):
        """Set up test method"""
        self.setup_test_database()
        self.setup_test_content()
        self.setup_mocks()

    def teardown_method(self):
        """Tear down test method"""
        self.cleanup_test_database()
        self.cleanup_test_content()
        self.cleanup_mocks()

    def setup_test_database(self):
        """Setup test database"""
        from tutorial_agent.database import init_database
        self.test_db_path = Path(tempfile.mkdtemp()) / 'test.db'
        init_database(self.test_db_path)

    def cleanup_test_database(self):
        """Cleanup test database"""
        if hasattr(self, 'test_db_path') and self.test_db_path.exists():
            self.test_db_path.unlink()
            self.test_db_path.parent.rmdir()

    def setup_test_content(self):
        """Setup test content"""
        self.test_content_dir = Path(tempfile.mkdtemp())
        self.create_test_content()

    def cleanup_test_content(self):
        """Cleanup test content"""
        if hasattr(self, 'test_content_dir') and self.test_content_dir.exists():
            import shutil
            shutil.rmtree(self.test_content_dir)

    def setup_mocks(self):
        """Setup service mocks"""
        self.mocks = {}
        # Store original services to restore later
        self.original_services = {}

        # Setup mock services
        self.setup_mock_auth_service()
        self.setup_mock_content_service()
        self.setup_mock_quiz_service()
        self.setup_mock_progress_service()

    def cleanup_mocks(self):
        """Cleanup and restore original services"""
        # Restore original services
        for service_name, original_service in self.original_services.items():
            setattr(self, service_name, original_service)

    def create_test_content(self):
        """Create test content files"""
        # Create Python content
        python_dir = self.test_content_dir / 'python'
        python_dir.mkdir(parents=True)
        self.create_test_topic(python_dir, 'basics')
        self.create_test_topic(python_dir, 'intermediate')
        self.create_test_topic(python_dir, 'advanced')

    def create_test_topic(self, lang_dir: Path, level: str):
        """Create test topic content"""
        topic_data = {
            "id": f"{level}_topic",
            "title": f"{level.title()} Topic",
            "description": f"Test {level} topic content",
            "content": f"# {level.title()} Topic Content\nTest content for {level} topic.",
            "examples": [
                {
                    "title": "Example 1",
                    "code": "print('Hello, World!')",
                    "explanation": "Basic example"
                }
            ],
            "exercises": [
                {
                    "id": "ex1",
                    "title": "Exercise 1",
                    "description": "Test exercise",
                    "solution": "# Solution\npass"
                }
            ],
            "quiz": {
                "questions": [
                    {
                        "id": "q1",
                        "question": "Test question?",
                        "options": ["A", "B", "C", "D"],
                        "correct": 0
                    }
                ]
            }
        }

        topic_file = lang_dir / f"{level}.json"
        topic_file.write_text(json.dumps(topic_data, indent=2))

    def setup_mock_auth_service(self):
        """Setup mock authentication service"""
        auth_service_mock = Mock()
        auth_service_mock.validate_user.return_value = True
        auth_service_mock.get_user_settings.return_value = {}

        self.mocks['auth_service'] = auth_service_mock
        self.original_services['auth_service'] = getattr(self, 'auth_service', None)
        self.auth_service = auth_service_mock

    def setup_mock_content_service(self):
        """Setup mock content service"""
        content_service_mock = Mock()
        content_service_mock.get_content.return_value = {}
        content_service_mock.get_topics.return_value = []

        self.mocks['content_service'] = content_service_mock
        self.original_services['content_service'] = getattr(self, 'content_service', None)
        self.content_service = content_service_mock

    def setup_mock_quiz_service(self):
        """Setup mock quiz service"""
        quiz_service_mock = Mock()
        quiz_service_mock.get_quiz.return_value = {}
        quiz_service_mock.submit_quiz.return_value = {'score': 0, 'total': 0}

        self.mocks['quiz_service'] = quiz_service_mock
        self.original_services['quiz_service'] = getattr(self, 'quiz_service', None)
        self.quiz_service = quiz_service_mock

    def setup_mock_progress_service(self):
        """Setup mock progress service"""
        progress_service_mock = Mock()
        progress_service_mock.get_user_progress.return_value = {}

        self.mocks['progress_service'] = progress_service_mock
        self.original_services['progress_service'] = getattr(self, 'progress_service', None)
        self.progress_service = progress_service_mock

    def create_test_user(self) -> Dict[str, Any]:
        """Create test user"""
        user_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test_password'
        }
        return user_data

    def create_test_quiz_data(self) -> Dict[str, Any]:
        """Create test quiz data"""
        quiz_data = {
            'questions': [
                {
                    'id': 'q1',
                    'question': 'Test question?',
                    'options': ['A', 'B', 'C', 'D'],
                    'correct': 0
                }
            ],
            'passing_score': 70,
            'time_limit': 300
        }
        return quiz_data


# Test decorators
def requires_database(func):
    """Decorator for tests requiring database"""
    return pytest.mark.database(func)


def requires_content(func):
    """Decorator for tests requiring content"""
    return pytest.mark.content(func)


def requires_authentication(func):
    """Decorator for tests requiring authentication"""
    return pytest.mark.auth(func)


# Mock response builder
class MockResponseBuilder:
    """Builder for mock service responses"""

    @staticmethod
    def success_response(**kwargs):
        """Build success response"""
        return {'status': 'success', **kwargs}

    @staticmethod
    def error_response(message, code=None):
        """Build error response"""
        return {
            'status': 'error',
            'message': message,
            'code': code
        }

    @staticmethod
    def progress_response(completed=0, total=0):
        """Build progress response"""
        return {
            'completed': completed,
            'total': total,
            'percentage': (completed / total * 100) if total > 0 else 0
        }


# Export test components
__all__ = [
    'ServicesTestCase',
    'requires_database',
    'requires_content',
    'requires_authentication',
    'MockResponseBuilder'
]