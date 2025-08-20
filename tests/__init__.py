"""
Test suite for Tutorial Agent
"""

import os
import sys
import pytest
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test constants
TEST_DATA_DIR = Path(__file__).parent / 'data'
TEST_TEMP_DIR = Path(__file__).parent / 'temp'
TEST_DB_PATH = TEST_TEMP_DIR / 'test.db'

# Ensure test directories exist
TEST_DATA_DIR.mkdir(exist_ok=True)
TEST_TEMP_DIR.mkdir(exist_ok=True)


def run_tests():
    """Run all tests"""
    pytest.main(['tests'])


def setup_test_environment():
    """Setup test environment"""
    # Set test environment variable
    os.environ['TUTORIAL_AGENT_ENV'] = 'test'

    # Create test directories if they don't exist
    TEST_DATA_DIR.mkdir(exist_ok=True)
    TEST_TEMP_DIR.mkdir(exist_ok=True)

    # Initialize test database
    from tutorial_agent.database import init_database
    init_database(TEST_DB_PATH)


def teardown_test_environment():
    """Cleanup test environment"""
    # Remove test database
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()

    # Remove test temp directory
    if TEST_TEMP_DIR.exists():
        import shutil
        shutil.rmtree(TEST_TEMP_DIR)


# Test fixtures
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers",
        "gui: mark test as requiring GUI (PyQt6)",
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running",
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test",
    )


def pytest_addoption(parser):
    """Add custom pytest options"""
    parser.addoption(
        "--run-gui",
        action="store_true",
        default=False,
        help="run GUI tests"
    )
    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="run slow tests"
    )
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on options"""
    skip_gui = pytest.mark.skip(reason="need --run-gui option to run")
    skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
    skip_integration = pytest.mark.skip(reason="need --run-integration option to run")

    for item in items:
        if "gui" in item.keywords and not config.getoption("--run-gui"):
            item.add_marker(skip_gui)
        if "slow" in item.keywords and not config.getoption("--run-slow"):
            item.add_marker(skip_slow)
        if "integration" in item.keywords and not config.getoption("--run-integration"):
            item.add_marker(skip_integration)


# Test utilities
class TestCase:
    """Base test case class"""

    @classmethod
    def setup_class(cls):
        """Set up test class"""
        setup_test_environment()

    @classmethod
    def teardown_class(cls):
        """Tear down test class"""
        teardown_test_environment()

    def setup_method(self):
        """Set up test method"""
        pass

    def teardown_method(self):
        """Tear down test method"""
        pass


# Export test components
__all__ = [
    'TestCase',
    'run_tests',
    'setup_test_environment',
    'teardown_test_environment',
    'TEST_DATA_DIR',
    'TEST_TEMP_DIR',
    'TEST_DB_PATH'
]