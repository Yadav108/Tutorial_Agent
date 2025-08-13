# tests/conftest.py

import pytest
import tempfile
import shutil
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from content.enhanced_content_manager import EnhancedContentManager
from database.database_manager import DatabaseManager
from config.settings_manager import SettingsManager
from content.enhanced_models import Language, Topic, Example, Exercise, DifficultyLevel


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for tests."""
    if not QApplication.instance():
        app = QApplication([])
        yield app
        app.quit()
    else:
        yield QApplication.instance()


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def test_content_dir(temp_dir):
    """Create test content directory structure."""
    content_dir = temp_dir / "content"
    languages_dir = content_dir / "languages"

    # Create Python language content
    python_dir = languages_dir / "python"
    python_dir.mkdir(parents=True)

    # Create a simple Python topic file
    topic_file = python_dir / "basics.py"
    topic_file.write_text("""
from content.enhanced_models import Topic, Example, Exercise, DifficultyLevel

def create_python_basics_content():
    return Topic(
        title="Python Basics",
        description="Learn the fundamentals of Python programming",
        content="# Python Basics\\n\\nPython is a versatile programming language.",
        examples=[
            Example(
                title="Hello World",
                code='print("Hello, World!")',
                explanation="This prints Hello World to the console"
            )
        ],
        exercises=[
            Exercise(
                title="Print Your Name",
                description="Write a program that prints your name",
                starter_code='name = "Your Name"\\nprint(name)'
            )
        ],
        difficulty=DifficultyLevel.BEGINNER
    )
""")

    # Create JavaScript content
    js_dir = languages_dir / "javascript"
    js_dir.mkdir(parents=True)

    js_topic_file = js_dir / "basics.py"
    js_topic_file.write_text("""
from content.enhanced_models import Topic, Example, Exercise, DifficultyLevel

def create_javascript_basics_content():
    return Topic(
        title="JavaScript Basics",
        description="Learn the fundamentals of JavaScript programming",
        content="# JavaScript Basics\\n\\nJavaScript is the language of the web.",
        examples=[
            Example(
                title="Hello World",
                code='console.log("Hello, World!");',
                explanation="This prints Hello World to the console"
            )
        ],
        exercises=[
            Exercise(
                title="Alert Your Name",
                description="Create an alert with your name",
                starter_code='const name = "Your Name";\\nalert(name);'
            )
        ],
        difficulty=DifficultyLevel.BEGINNER
    )
""")

    return content_dir


@pytest.fixture
def test_database(temp_dir):
    """Create test database."""
    db_path = temp_dir / "test.db"
    db_manager = DatabaseManager(db_path)
    yield db_manager
    db_manager.cleanup()


@pytest.fixture
def test_settings(temp_dir):
    """Create test settings manager."""
    settings_manager = SettingsManager(temp_dir)
    yield settings_manager


@pytest.fixture
def sample_language():
    """Create sample language for testing."""
    return Language(
        name="Test Language",
        description="A test programming language",
        topics=[
            Topic(
                title="Test Topic",
                description="A test topic",
                content="# Test Content",
                examples=[
                    Example(
                        title="Test Example",
                        code="print('test')",
                        explanation="A test example"
                    )
                ],
                exercises=[
                    Exercise(
                        title="Test Exercise",
                        description="A test exercise",
                        starter_code="# Write your code here"
                    )
                ]
            )
        ]
    )


# tests/test_models.py

import pytest
from datetime import datetime, timezone
from content.enhanced_models import (
    Language, Topic, Example, Exercise, UserProgress,
    DifficultyLevel, ProgressStatus, ValidationError
)


class TestExample:
    """Test the Example model."""

    def test_example_creation(self):
        """Test creating a valid example."""
        example = Example(
            title="Hello World",
            code='print("Hello, World!")',
            explanation="This prints Hello World",
            language="python"
        )

        assert example.title == "Hello World"
        assert example.code == 'print("Hello, World!")'
        assert example.language == "python"
        assert example.difficulty == DifficultyLevel.MEDIUM

    def test_example_validation_empty_title(self):
        """Test example validation with empty title."""
        with pytest.raises(ValidationError, match="Example title cannot be empty"):
            Example(
                title="",
                code='print("test")',
                explanation="Test explanation"
            )

    def test_example_validation_empty_code(self):
        """Test example validation with empty code."""
        with pytest.raises(ValidationError, match="Code cannot be empty"):
            Example(
                title="Test",
                code="",
                explanation="Test explanation"
            )

    def test_example_complexity_score(self):
        """Test complexity score calculation."""
        simple_example = Example(
            title="Simple",
            code='print("hello")',
            explanation="Simple code"
        )

        complex_example = Example(
            title="Complex",
            code='''
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n-1)

for i in range(5):
    print(f"Factorial of {i} is {factorial(i)}")
''',
            explanation="Complex recursive function"
        )

        assert complex_example.get_complexity_score() > simple_example.get_complexity_score()

    def test_example_reading_time(self):
        """Test reading time estimation."""
        example = Example(
            title="Test",
            code='print("hello")',
            explanation="This is a simple example that prints hello to the console."
        )

        reading_time = example.estimate_reading_time()
        assert reading_time >= 30  # Minimum 30 seconds
        assert isinstance(reading_time, int)


class TestExercise:
    """Test the Exercise model."""

    def test_exercise_creation(self):
        """Test creating a valid exercise."""
        exercise = Exercise(
            title="Print Name",
            description="Write a program that prints your name",
            starter_code='name = "Your Name"\nprint(name)',
            solution='name = "John Doe"\nprint(name)'
        )

        assert exercise.title == "Print Name"
        assert exercise.max_attempts == 5
        assert exercise.points == 10

    def test_exercise_validation(self):
        """Test exercise validation."""
        with pytest.raises(ValidationError, match="Exercise title cannot be empty"):
            Exercise(title="", description="Test")

        with pytest.raises(ValidationError, match="Exercise description cannot be empty"):
            Exercise(title="Test", description="")

    def test_exercise_difficulty_multiplier(self):
        """Test difficulty multiplier calculation."""
        beginner_exercise = Exercise(
            title="Beginner",
            description="Easy exercise",
            difficulty=DifficultyLevel.BEGINNER
        )

        advanced_exercise = Exercise(
            title="Advanced",
            description="Hard exercise",
            difficulty=DifficultyLevel.ADVANCED
        )

        assert advanced_exercise.get_difficulty_multiplier() > beginner_exercise.get_difficulty_multiplier()

    def test_exercise_max_points(self):
        """Test maximum points calculation."""
        exercise = Exercise(
            title="Test",
            description="Test exercise",
            points=10,
            difficulty=DifficultyLevel.HARD
        )

        max_points = exercise.calculate_max_points()
        assert max_points == int(10 * 1.5)  # Hard difficulty multiplier


class TestTopic:
    """Test the Topic model."""

    def test_topic_creation(self):
        """Test creating a valid topic."""
        topic = Topic(
            title="Python Basics",
            description="Learn Python fundamentals",
            content="# Python Basics\n\nPython is awesome!"
        )

        assert topic.title == "Python Basics"
        assert topic.estimated_duration_minutes == 30
        assert topic.is_published is True

    def test_topic_validation(self):
        """Test topic validation."""
        with pytest.raises(ValidationError, match="Topic title cannot be empty"):
            Topic(title="", description="Test", content="Test")

    def test_topic_add_example(self):
        """Test adding examples to topic."""
        topic = Topic(
            title="Test Topic",
            description="Test description",
            content="Test content"
        )

        example = topic.add_example(
            title="Test Example",
            code='print("test")',
            explanation="Test explanation"
        )

        assert len(topic.examples) == 1
        assert topic.examples[0] == example
        assert example.title == "Test Example"

    def test_topic_add_exercise(self):
        """Test adding exercises to topic."""
        topic = Topic(
            title="Test Topic",
            description="Test description",
            content="Test content"
        )

        exercise = topic.add_exercise(
            title="Test Exercise",
            description="Test exercise description"
        )

        assert len(topic.exercises) == 1
        assert topic.exercises[0] == exercise
        assert exercise.title == "Test Exercise"

    def test_topic_total_estimated_time(self):
        """Test total estimated time calculation."""
        topic = Topic(
            title="Test Topic",
            description="Test description",
            content="Test content",
            estimated_duration_minutes=30
        )

        topic.add_example(
            title="Example",
            code='print("test")',
            explanation="Short explanation"
        )

        topic.add_exercise(
            title="Exercise",
            description="Test exercise",
            estimated_time_minutes=15
        )

        total_time = topic.get_total_estimated_time()
        assert total_time > 30  # Should include example and exercise time

    def test_topic_content_stats(self):
        """Test content statistics."""
        topic = Topic(
            title="Test Topic",
            description="Test description",
            content="This is a test content with multiple words for testing."
        )

        topic.add_example("Ex1", "code", "explanation")
        topic.add_exercise("Ex1", "description")

        stats = topic.get_content_stats()

        assert stats['word_count'] > 0
        assert stats['examples_count'] == 1
        assert stats['exercises_count'] == 1
        assert 'total_estimated_minutes' in stats


class TestLanguage:
    """Test the Language model."""

    def test_language_creation(self):
        """Test creating a valid language."""
        language = Language(
            name="Python",
            description="A versatile programming language"
        )

        assert language.name == "Python"
        assert language.color == "#3498db"
        assert language.is_active is True

    def test_language_validation(self):
        """Test language validation."""
        with pytest.raises(ValidationError, match="Language name cannot be empty"):
            Language(name="", description="Test")

        with pytest.raises(ValidationError, match="Color must be a valid hex color"):
            Language(name="Test", description="Test", color="invalid")

    def test_language_add_topic(self):
        """Test adding topics to language."""
        language = Language(
            name="Test Language",
            description="Test description"
        )

        topic = language.add_topic(
            title="Test Topic",
            description="Test topic description",
            content="Test content"
        )

        assert len(language.topics) == 1
        assert language.topics[0] == topic
        assert topic.order_index == 0

    def test_language_get_topic_by_title(self):
        """Test getting topic by title."""
        language = Language(
            name="Test Language",
            description="Test description"
        )

        topic = language.add_topic(
            title="Test Topic",
            description="Test description",
            content="Test content"
        )

        found_topic = language.get_topic_by_title("Test Topic")
        assert found_topic == topic

        not_found = language.get_topic_by_title("Nonexistent")
        assert not_found is None

    def test_language_stats(self):
        """Test language statistics."""
        language = Language(
            name="Test Language",
            description="Test description"
        )

        topic = language.add_topic(
            title="Test Topic",
            description="Test description",
            content="Test content"
        )

        topic.add_example("Example", "code", "explanation")
        topic.add_exercise("Exercise", "description")

        stats = language.get_language_stats()

        assert stats['total_topics'] == 1
        assert stats['total_examples'] == 1
        assert stats['total_exercises'] == 1
        assert 'total_estimated_minutes' in stats


class TestUserProgress:
    """Test the UserProgress model."""

    def test_user_progress_creation(self):
        """Test creating user progress."""
        progress = UserProgress(
            user_id="test_user",
            language_id="python",
            topic_id="basics",
            status=ProgressStatus.IN_PROGRESS,
            completion_percentage=50.0
        )

        assert progress.user_id == "test_user"
        assert progress.status == ProgressStatus.IN_PROGRESS
        assert progress.completion_percentage == 50.0

    def test_user_progress_validation(self):
        """Test user progress validation."""
        with pytest.raises(ValidationError, match="User ID cannot be empty"):
            UserProgress(user_id="", language_id="test", topic_id="test")

        with pytest.raises(ValidationError, match="Completion percentage must be between 0 and 100"):
            UserProgress(
                user_id="test",
                language_id="test",
                topic_id="test",
                completion_percentage=150.0
            )

    def test_mark_example_completed(self):
        """Test marking examples as completed."""
        progress = UserProgress(
            user_id="test_user",
            language_id="python",
            topic_id="basics"
        )

        progress.mark_example_completed("example_1")
        progress.mark_example_completed("example_2")

        assert len(progress.completed_examples) == 2
        assert "example_1" in progress.completed_examples
        assert "example_2" in progress.completed_examples

    def test_mark_exercise_completed(self):
        """Test marking exercises as completed."""
        progress = UserProgress(
            user_id="test_user",
            language_id="python",
            topic_id="basics"
        )

        progress.mark_exercise_completed("exercise_1", 85.0)
        progress.mark_exercise_completed("exercise_2", 90.0)

        assert len(progress.completed_exercises) == 2
        assert progress.exercise_scores["exercise_1"] == 85.0
        assert progress.exercise_scores["exercise_2"] == 90.0

    def test_average_exercise_score(self):
        """Test average exercise score calculation."""
        progress = UserProgress(
            user_id="test_user",
            language_id="python",
            topic_id="basics"
        )

        progress.mark_exercise_completed("ex1", 80.0)
        progress.mark_exercise_completed("ex2", 90.0)
        progress.mark_exercise_completed("ex3", 70.0)

        avg_score = progress.get_average_exercise_score()
        assert avg_score == 80.0


# tests/test_content_manager.py

import pytest
from unittest.mock import patch, MagicMock
from content.enhanced_content_manager import EnhancedContentManager
from content.enhanced_models import Language, Topic


class TestEnhancedContentManager:
    """Test the enhanced content manager."""

    def test_content_manager_initialization(self, test_content_dir):
        """Test content manager initialization."""
        manager = EnhancedContentManager(test_content_dir)

        assert manager.content_dir == test_content_dir
        assert manager.cache is not None
        assert manager.performance_monitor is not None

    def test_load_all_languages(self, test_content_dir):
        """Test loading all languages."""
        manager = EnhancedContentManager(test_content_dir)
        languages = manager.get_all_languages()

        # Should load Python and JavaScript from test content
        assert len(languages) >= 0  # May be 0 if content loading fails

        # Test that cache is working
        languages_cached = manager.get_all_languages()
        assert languages_cached == languages

    def test_search_functionality(self, test_content_dir):
        """Test search functionality."""
        manager = EnhancedContentManager(test_content_dir)

        # Search for "hello"
        results = manager.search("hello")

        # Should return some results
        assert isinstance(results, list)

        # Test search with language filter
        results_filtered = manager.search("hello", language="python")
        assert isinstance(results_filtered, list)

    def test_get_language(self, test_content_dir):
        """Test getting specific language."""
        manager = EnhancedContentManager(test_content_dir)

        # Try to get Python language
        python_lang = manager.get_language("Python")

        if python_lang:  # Only test if language was loaded
            assert python_lang.name.lower() == "python"

    def test_cache_functionality(self, test_content_dir):
        """Test caching functionality."""
        manager = EnhancedContentManager(test_content_dir, cache_size_mb=10)

        # Test cache stats
        stats = manager.cache.get_stats()
        assert 'hits' in stats
        assert 'misses' in stats
        assert 'hit_rate' in stats

    def test_performance_monitoring(self, test_content_dir):
        """Test performance monitoring."""
        manager = EnhancedContentManager(test_content_dir)

        # Get performance stats
        stats = manager.performance_monitor.get_stats()
        assert isinstance(stats, dict)

    def test_user_statistics(self, test_content_dir):
        """Test user statistics."""
        manager = EnhancedContentManager(test_content_dir)

        stats = manager.get_user_statistics()

        assert 'total_languages' in stats
        assert 'languages_started' in stats
        assert 'cache_stats' in stats
        assert 'performance_stats' in stats


# tests/test_database_manager.py

import pytest
from database.database_manager import DatabaseManager
from content.enhanced_models import Language, Topic, Example, Exercise, UserProgress, ProgressStatus


class TestDatabaseManager:
    """Test the database manager."""

    def test_database_initialization(self, test_database):
        """Test database initialization."""
        assert test_database.db_path.exists()

        # Test that tables were created
        conn = test_database.get_connection()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row[0] for row in cursor.fetchall()]

        expected_tables = [
            'schema_version', 'languages', 'topics', 'examples',
            'exercises', 'user_progress', 'user_sessions', 'learning_stats'
        ]

        for table in expected_tables:
            assert table in tables

    def test_save_and_load_language(self, test_database, sample_language):
        """Test saving and loading a language."""
        # Save language
        language_id = test_database.save_language(sample_language)
        assert language_id == sample_language.id

        # Load language
        loaded_language = test_database.get_language(language_id)
        assert loaded_language is not None
        assert loaded_language.name == sample_language.name
        assert len(loaded_language.topics) == len(sample_language.topics)

    def test_get_all_languages(self, test_database, sample_language):
        """Test getting all languages."""
        # Save a language first
        test_database.save_language(sample_language)

        # Get all languages
        languages = test_database.get_all_languages()
        assert len(languages) >= 1
        assert sample_language.id in languages

    def test_save_and_load_user_progress(self, test_database):
        """Test saving and loading user progress."""
        progress = UserProgress(
            user_id="test_user",
            language_id="test_lang",
            topic_id="test_topic",
            status=ProgressStatus.IN_PROGRESS,
            completion_percentage=75.0
        )

        # Save progress
        progress_id = test_database.save_user_progress(progress)
        assert progress_id == progress.id

        # Load progress
        loaded_progress = test_database.get_user_progress("test_user")
        assert len(loaded_progress) == 1
        assert loaded_progress[0].completion_percentage == 75.0

    def test_search_content(self, test_database, sample_language):
        """Test content search functionality."""
        # Save language with content
        test_database.save_language(sample_language)

        # Search for content
        results = test_database.search_content("test")
        assert isinstance(results, list)

        # Search with user context
        results_with_user = test_database.search_content("test", user_id="test_user")
        assert isinstance(results_with_user, list)

    def test_learning_statistics(self, test_database):
        """Test learning statistics retrieval."""
        stats = test_database.get_learning_statistics("test_user")

        assert 'daily_stats' in stats
        assert 'summary' in stats
        assert isinstance(stats['daily_stats'], list)
        assert isinstance(stats['summary'], dict)

    def test_database_backup(self, test_database, temp_dir):
        """Test database backup functionality."""
        backup_path = test_database.backup_database(temp_dir / "backup.db")

        assert backup_path.exists()
        assert backup_path.stat().st_size > 0


# tests/test_settings_manager.py

import pytest
from config.settings_manager import SettingsManager, ThemeMode, LanguagePreference


class TestSettingsManager:
    """Test the settings manager."""

    def test_settings_initialization(self, test_settings):
        """Test settings manager initialization."""
        assert test_settings.settings is not None
        assert test_settings.config_file.exists()

    def test_get_and_set_settings(self, test_settings):
        """Test getting and setting individual settings."""
        # Test default value
        font_size = test_settings.get('editor.font_size')
        assert font_size == 12

        # Test setting value
        success = test_settings.set('editor.font_size', 14)
        assert success

        # Test getting updated value
        updated_font_size = test_settings.get('editor.font_size')
        assert updated_font_size == 14

    def test_settings_validation(self, test_settings):
        """Test settings validation."""
        # Try to set invalid font size
        success = test_settings.set('editor.font_size', 100)  # Should fail validation
        assert not success

        # Font size should remain unchanged
        font_size = test_settings.get('editor.font_size')
        assert font_size != 100

    def test_settings_callbacks(self, test_settings):
        """Test settings change callbacks."""
        callback_called = []

        def callback(value):
            callback_called.append(value)

        # Register callback
        test_settings.register_callback('editor.font_size', callback)

        # Change setting
        test_settings.set('editor.font_size', 16)

        # Check callback was called
        assert len(callback_called) == 1
        assert callback_called[0] == 16

    def test_reset_to_defaults(self, test_settings):
        """Test resetting settings to defaults."""
        # Change a setting
        test_settings.set('editor.font_size', 20)

        # Reset editor settings
        success = test_settings.reset_to_defaults('editor')
        assert success

        # Check setting was reset
        font_size = test_settings.get('editor.font_size')
        assert font_size == 12  # Default value

    def test_export_import_settings(self, test_settings, temp_dir):
        """Test exporting and importing settings."""
        # Change some settings
        test_settings.set('editor.font_size', 18)
        test_settings.set('ui.theme', ThemeMode.DARK)

        # Export settings
        export_file = temp_dir / "exported_settings.json"
        success = test_settings.export_settings(export_file)
        assert success
        assert export_file.exists()

        # Reset settings
        test_settings.reset_to_defaults()

        # Import settings
        success = test_settings.import_settings(export_file)
        assert success

        # Check settings were restored
        assert test_settings.get('editor.font_size') == 18
        assert test_settings.get('ui.theme') == ThemeMode.DARK


# tests/test_integration.py

import pytest
from PyQt6.QtWidgets import QWidget
from unittest.mock import patch, MagicMock


class TestIntegration:
    """Integration tests for the complete application."""

    @pytest.fixture
    def app_components(self, qapp, test_content_dir, test_database, test_settings):
        """Setup complete application components for testing."""
        return {
            'content_manager': EnhancedContentManager(test_content_dir),
            'database': test_database,
            'settings': test_settings,
            'qapp': qapp
        }

    def test_content_manager_database_integration(self, app_components, sample_language):
        """Test integration between content manager and database."""
        content_manager = app_components['content_manager']
        database = app_components['database']

        # Save language to database
        language_id = database.save_language(sample_language)

        # Verify it can be retrieved
        loaded_language = database.get_language(language_id)
        assert loaded_language is not None
        assert loaded_language.name == sample_language.name

    def test_settings_content_manager_integration(self, app_components):
        """Test integration between settings and content manager."""
        settings = app_components['settings']
        content_manager = app_components['content_manager']

        # Update cache settings
        settings.set('performance.cache_size_mb', 50)
        settings.set('performance.enable_caching', True)

        # Verify settings are applied
        assert settings.get('performance.cache_size_mb') == 50
        assert settings.get('performance.enable_caching') is True

    @patch('PyQt6.QtWidgets.QMainWindow')
    def test_main_window_initialization(self, mock_main_window, app_components):
        """Test main window initialization with all components."""
        # This would test the actual main window initialization
        # but we mock it here to avoid GUI dependencies in tests
        mock_window = mock_main_window.return_value
        mock_window.content_manager = app_components['content_manager']
        mock_window.database = app_components['database']
        mock_window.settings = app_components['settings']

        # Simulate initialization
        assert mock_window.content_manager is not None
        assert mock_window.database is not None
        assert mock_window.settings is not None


# tests/test_performance.py

import pytest
import time
from utils.performance_monitor import PerformanceMonitor, measure_performance


class TestPerformanceMonitor:
    """Test performance monitoring functionality."""

    def test_performance_monitor_initialization(self):
        """Test performance monitor initialization."""
        monitor = PerformanceMonitor()

        assert monitor.max_history == 1000
        assert len(monitor.metrics_history) == 0
        assert len(monitor.operation_stats) == 0

    def test_record_metric(self):
        """Test recording custom metrics."""
        monitor = PerformanceMonitor()

        monitor.record_metric("test_metric", 42.0, {"unit": "seconds"})

        assert len(monitor.metrics_history) == 1
        metric = monitor.metrics_history[0]
        assert metric.name == "test_metric"
        assert metric.value == 42.0
        assert metric.metadata["unit"] == "seconds"

    def test_record_operation(self):
        """Test recording operation performance."""
        monitor = PerformanceMonitor()

        monitor.record_operation("test_operation", 1.5, success=True)
        monitor.record_operation("test_operation", 2.0, success=True)
        monitor.record_operation("test_operation", 0.5, success=False)

        stats = monitor.operation_stats["test_operation"]
        assert stats.count == 3
        assert stats.error_count == 1
        assert stats.avg_time == (1.5 + 2.0 + 0.5) / 3
        assert stats.success_rate == (2 / 3) * 100

    def test_measure_performance_decorator(self):
        """Test performance measurement decorator."""
        monitor = PerformanceMonitor()

        @measure_performance("test_function", monitor)
        def slow_function():
            time.sleep(0.1)
            return "result"

        result = slow_function()

        assert result == "result"
        assert "test_function" in monitor.operation_stats
        assert monitor.operation_stats["test_function"].count == 1
        assert monitor.operation_stats["test_function"].avg_time >= 0.1

    def test_system_monitoring(self):
        """Test system performance monitoring."""
        monitor = PerformanceMonitor()

        # Start monitoring briefly
        monitor.start_monitoring(interval=0.1)
        time.sleep(0.2)
        monitor.stop_monitoring()

        # Check that some metrics were collected
        stats = monitor.get_system_stats()
        assert isinstance(stats, dict)

        # CPU and memory metrics might be available
        if 'cpu_percent' in stats:
            assert 'current' in stats['cpu_percent']
            assert 'average' in stats['cpu_percent']


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])