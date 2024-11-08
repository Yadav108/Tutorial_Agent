"""
Utility test suite for Tutorial Agent
"""

import pytest
from pathlib import Path
import tempfile
import shutil


class UtilsTestCase:
    """Base class for utility tests"""

    def setup_method(self):
        """Set up test method"""
        # Create temporary test directory
        self.test_dir = Path(tempfile.mkdtemp())
        self.addCleanup(self.cleanup_test_dir)

    def cleanup_test_dir(self):
        """Clean up temporary test directory"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def create_test_file(self, content, name="test.txt"):
        """Create a test file with content"""
        file_path = self.test_dir / name
        file_path.write_text(content)
        return file_path

    def create_test_directory(self, name="test_dir"):
        """Create a test directory"""
        dir_path = self.test_dir / name
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    def addCleanup(self, func, *args, **kwargs):
        """Add cleanup function to be called after test"""
        if not hasattr(self, '_cleanups'):
            self._cleanups = []
        self._cleanups.append((func, args, kwargs))

    def teardown_method(self):
        """Tear down test method"""
        if hasattr(self, '_cleanups'):
            for func, args, kwargs in reversed(self._cleanups):
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"Cleanup error: {str(e)}")


# Test utilities
def create_temp_file(content="", suffix=".txt"):
    """Create a temporary file with content"""
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    temp_file.write(content.encode())
    temp_file.close()
    return Path(temp_file.name)


def create_temp_directory():
    """Create a temporary directory"""
    return Path(tempfile.mkdtemp())


def requires_temp_dir(func):
    """Decorator to provide temporary directory to test"""

    def wrapper(*args, **kwargs):
        temp_dir = create_temp_directory()
        try:
            return func(*args, temp_dir=temp_dir, **kwargs)
        finally:
            shutil.rmtree(temp_dir)

    return wrapper


def requires_temp_file(content="", suffix=".txt"):
    """Decorator to provide temporary file to test"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            temp_file = create_temp_file(content, suffix)
            try:
                return func(*args, temp_file=temp_file, **kwargs)
            finally:
                temp_file.unlink()

        return wrapper

    return decorator


# Test data generators
def generate_random_string(length=10):
    """Generate random string"""
    import string
    import random
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_random_file(size_bytes=1024):
    """Generate random binary file"""
    import os
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, 'wb') as f:
        f.write(os.urandom(size_bytes))
    return Path(temp_file.name)


# Export test components
__all__ = [
    'UtilsTestCase',
    'create_temp_file',
    'create_temp_directory',
    'requires_temp_dir',
    'requires_temp_file',
    'generate_random_string',
    'generate_random_file'
]