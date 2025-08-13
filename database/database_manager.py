# database/database_manager.py

import logging
import sqlite3
import json
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timezone
from contextlib import contextmanager
from dataclasses import asdict
import uuid

from content.enhanced_models import (
    Language, Topic, Example, Exercise, UserProgress,
    DifficultyLevel, ProgressStatus, ContentType
)

logger = logging.getLogger('TutorialAgent.Database')


class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass


class DatabaseManager:
    """SQLite database manager for persistent data storage."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Path.home() / ".tutorial_agent" / "data.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Connection pool (thread-local storage)
        self._local = threading.local()

        # Database version for migrations
        self.current_version = 3

        # Initialize database
        self.initialize_database()

        logger.info(f"Database manager initialized: {self.db_path}")

    def get_connection(self) -> sqlite3.Connection:
        """Get thread-local database connection."""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False,
                timeout=30.0
            )
            self._local.connection.row_factory = sqlite3.Row

            # Enable foreign keys
            self._local.connection.execute("PRAGMA foreign_keys = ON")

            # Performance optimizations
            self._local.connection.execute("PRAGMA journal_mode = WAL")
            self._local.connection.execute("PRAGMA synchronous = NORMAL")
            self._local.connection.execute("PRAGMA cache_size = 10000")
            self._local.connection.execute("PRAGMA temp_store = MEMORY")

        return self._local.connection

    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database transaction failed: {e}")
            raise DatabaseError(f"Transaction failed: {e}")

    def initialize_database(self):
        """Initialize database schema and perform migrations."""
        try:
            with self.transaction() as conn:
                # Check if database exists and get version
                current_version = self._get_schema_version(conn)

                if current_version == 0:
                    # Fresh installation
                    self._create_initial_schema(conn)
                    self._set_schema_version(conn, self.current_version)
                    logger.info("Created fresh database schema")
                elif current_version < self.current_version:
                    # Migration needed
                    self._perform_migrations(conn, current_version)
                    logger.info(f"Migrated database from version {current_version} to {self.current_version}")

                # Create indexes for performance
                self._create_indexes(conn)

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise DatabaseError(f"Failed to initialize database: {e}")

    def _get_schema_version(self, conn: sqlite3.Connection) -> int:
        """Get current schema version."""
        try:
            cursor = conn.execute("SELECT version FROM schema_version ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            return row[0] if row else 0
        except sqlite3.OperationalError:
            return 0

    def _set_schema_version(self, conn: sqlite3.Connection, version: int):
        """Set schema version."""
        conn.execute(
            "INSERT INTO schema_version (version, applied_at) VALUES (?, ?)",
            (version, datetime.now(timezone.utc).isoformat())
        )

    def _create_initial_schema(self, conn: sqlite3.Connection):
        """Create initial database schema."""

        # Schema version tracking
        conn.execute("""
            CREATE TABLE schema_version (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version INTEGER NOT NULL,
                applied_at TEXT NOT NULL
            )
        """)

        # Languages table
        conn.execute("""
            CREATE TABLE languages (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                icon TEXT,
                color TEXT,
                version TEXT,
                difficulty TEXT,
                estimated_hours INTEGER,
                popularity_score REAL,
                is_active BOOLEAN DEFAULT 1,
                official_docs_url TEXT,
                community_links TEXT, -- JSON
                learning_path TEXT,   -- JSON
                metadata TEXT,        -- JSON
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Topics table
        conn.execute("""
            CREATE TABLE topics (
                id TEXT PRIMARY KEY,
                language_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                content TEXT NOT NULL,
                learning_objectives TEXT, -- JSON
                prerequisites TEXT,       -- JSON
                difficulty TEXT,
                estimated_duration_minutes INTEGER,
                order_index INTEGER DEFAULT 0,
                is_published BOOLEAN DEFAULT 1,
                best_practices TEXT,      -- JSON
                common_mistakes TEXT,     -- JSON
                additional_resources TEXT, -- JSON
                tags TEXT,                -- JSON
                metadata TEXT,            -- JSON
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE CASCADE
            )
        """)

        # Examples table
        conn.execute("""
            CREATE TABLE examples (
                id TEXT PRIMARY KEY,
                topic_id TEXT NOT NULL,
                title TEXT NOT NULL,
                code TEXT NOT NULL,
                explanation TEXT NOT NULL,
                language TEXT NOT NULL,
                difficulty TEXT,
                tags TEXT,               -- JSON
                expected_output TEXT,
                execution_time_ms INTEGER,
                memory_usage_kb INTEGER,
                metadata TEXT,           -- JSON
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
            )
        """)

        # Exercises table
        conn.execute("""
            CREATE TABLE exercises (
                id TEXT PRIMARY KEY,
                topic_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                instructions TEXT,
                starter_code TEXT,
                solution TEXT,
                difficulty TEXT,
                estimated_time_minutes INTEGER,
                tags TEXT,              -- JSON
                hints TEXT,             -- JSON
                test_cases TEXT,        -- JSON
                max_attempts INTEGER DEFAULT 5,
                points INTEGER DEFAULT 10,
                language TEXT NOT NULL,
                metadata TEXT,          -- JSON
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
            )
        """)

        # User progress table
        conn.execute("""
            CREATE TABLE user_progress (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                language_id TEXT,
                topic_id TEXT,
                exercise_id TEXT,
                status TEXT NOT NULL,
                completion_percentage REAL DEFAULT 0,
                time_spent_minutes INTEGER DEFAULT 0,
                attempts INTEGER DEFAULT 0,
                last_accessed TEXT NOT NULL,
                completed_examples TEXT, -- JSON
                completed_exercises TEXT, -- JSON
                exercise_scores TEXT,     -- JSON
                notes TEXT,
                bookmarked BOOLEAN DEFAULT 0,
                metadata TEXT,            -- JSON
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (language_id) REFERENCES languages(id) ON DELETE SET NULL,
                FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE SET NULL,
                FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE SET NULL
            )
        """)

        # User sessions table for analytics
        conn.execute("""
            CREATE TABLE user_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration_minutes INTEGER,
                languages_accessed TEXT, -- JSON
                topics_completed INTEGER DEFAULT 0,
                exercises_completed INTEGER DEFAULT 0,
                session_type TEXT,
                metadata TEXT,           -- JSON
                created_at TEXT NOT NULL
            )
        """)

        # Learning statistics
        conn.execute("""
            CREATE TABLE learning_stats (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                date TEXT NOT NULL,
                total_time_minutes INTEGER DEFAULT 0,
                topics_completed INTEGER DEFAULT 0,
                exercises_completed INTEGER DEFAULT 0,
                exercises_attempted INTEGER DEFAULT 0,
                average_score REAL DEFAULT 0,
                languages_practiced TEXT, -- JSON
                streak_days INTEGER DEFAULT 0,
                achievements TEXT,         -- JSON
                metadata TEXT,             -- JSON
                created_at TEXT NOT NULL,
                UNIQUE(user_id, date)
            )
        """)

        # Application settings (backup for settings manager)
        conn.execute("""
            CREATE TABLE app_settings (
                id TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                value_type TEXT NOT NULL,
                description TEXT,
                updated_at TEXT NOT NULL,
                UNIQUE(category, key)
            )
        """)

    def _create_indexes(self, conn: sqlite3.Connection):
        """Create database indexes for performance."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_topics_language_id ON topics(language_id)",
            "CREATE INDEX IF NOT EXISTS idx_topics_order_index ON topics(order_index)",
            "CREATE INDEX IF NOT EXISTS idx_examples_topic_id ON examples(topic_id)",
            "CREATE INDEX IF NOT EXISTS idx_exercises_topic_id ON exercises(topic_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_progress_language_id ON user_progress(language_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_progress_topic_id ON user_progress(topic_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_progress_status ON user_progress(status)",
            "CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_learning_stats_user_date ON learning_stats(user_id, date)",
            "CREATE INDEX IF NOT EXISTS idx_app_settings_category ON app_settings(category)"
        ]

        for index_sql in indexes:
            conn.execute(index_sql)

    def _perform_migrations(self, conn: sqlite3.Connection, from_version: int):
        """Perform database migrations."""
        for version in range(from_version + 1, self.current_version + 1):
            migration_method = getattr(self, f'_migrate_to_v{version}', None)
            if migration_method:
                logger.info(f"Applying migration to version {version}")
                migration_method(conn)
                self._set_schema_version(conn, version)

    def _migrate_to_v2(self, conn: sqlite3.Connection):
        """Migration to version 2 - Add user sessions table."""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration_minutes INTEGER,
                languages_accessed TEXT,
                topics_completed INTEGER DEFAULT 0,
                exercises_completed INTEGER DEFAULT 0,
                session_type TEXT,
                metadata TEXT,
                created_at TEXT NOT NULL
            )
        """)

    def _migrate_to_v3(self, conn: sqlite3.Connection):
        """Migration to version 3 - Add learning statistics."""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_stats (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                date TEXT NOT NULL,
                total_time_minutes INTEGER DEFAULT 0,
                topics_completed INTEGER DEFAULT 0,
                exercises_completed INTEGER DEFAULT 0,
                exercises_attempted INTEGER DEFAULT 0,
                average_score REAL DEFAULT 0,
                languages_practiced TEXT,
                streak_days INTEGER DEFAULT 0,
                achievements TEXT,
                metadata TEXT,
                created_at TEXT NOT NULL,
                UNIQUE(user_id, date)
            )
        """)

    # Language operations
    def save_language(self, language: Language) -> str:
        """Save or update a language."""
        try:
            with self.transaction() as conn:
                data = {
                    'id': language.id,
                    'name': language.name,
                    'description': language.description,
                    'icon': language.icon,
                    'color': language.color,
                    'version': language.version,
                    'difficulty': language.difficulty.value if isinstance(language.difficulty,
                                                                          DifficultyLevel) else language.difficulty,
                    'estimated_hours': language.estimated_hours,
                    'popularity_score': language.popularity_score,
                    'is_active': language.is_active,
                    'official_docs_url': language.official_docs_url,
                    'community_links': json.dumps(language.community_links),
                    'learning_path': json.dumps(language.learning_path),
                    'metadata': json.dumps(language.metadata),
                    'created_at': language.created_at.isoformat(),
                    'updated_at': language.updated_at.isoformat()
                }

                conn.execute("""
                    INSERT OR REPLACE INTO languages 
                    (id, name, description, icon, color, version, difficulty, estimated_hours,
                     popularity_score, is_active, official_docs_url, community_links, 
                     learning_path, metadata, created_at, updated_at)
                    VALUES (:id, :name, :description, :icon, :color, :version, :difficulty,
                            :estimated_hours, :popularity_score, :is_active, :official_docs_url,
                            :community_links, :learning_path, :metadata, :created_at, :updated_at)
                """, data)

                # Save topics
                for topic in language.topics:
                    self._save_topic(conn, topic, language.id)

                logger.debug(f"Saved language: {language.name}")
                return language.id

        except Exception as e:
            logger.error(f"Error saving language {language.name}: {e}")
            raise DatabaseError(f"Failed to save language: {e}")

    def _save_topic(self, conn: sqlite3.Connection, topic: Topic, language_id: str):
        """Save a topic (internal method)."""
        data = {
            'id': topic.id,
            'language_id': language_id,
            'title': topic.title,
            'description': topic.description,
            'content': topic.content,
            'learning_objectives': json.dumps(topic.learning_objectives),
            'prerequisites': json.dumps(topic.prerequisites),
            'difficulty': topic.difficulty.value if isinstance(topic.difficulty, DifficultyLevel) else topic.difficulty,
            'estimated_duration_minutes': topic.estimated_duration_minutes,
            'order_index': topic.order_index,
            'is_published': topic.is_published,
            'best_practices': json.dumps(topic.best_practices),
            'common_mistakes': json.dumps(topic.common_mistakes),
            'additional_resources': json.dumps(topic.additional_resources),
            'tags': json.dumps(topic.tags),
            'metadata': json.dumps(topic.metadata),
            'created_at': topic.created_at.isoformat(),
            'updated_at': topic.updated_at.isoformat()
        }

        conn.execute("""
            INSERT OR REPLACE INTO topics 
            (id, language_id, title, description, content, learning_objectives, prerequisites,
             difficulty, estimated_duration_minutes, order_index, is_published, best_practices,
             common_mistakes, additional_resources, tags, metadata, created_at, updated_at)
            VALUES (:id, :language_id, :title, :description, :content, :learning_objectives,
                    :prerequisites, :difficulty, :estimated_duration_minutes, :order_index,
                    :is_published, :best_practices, :common_mistakes, :additional_resources,
                    :tags, :metadata, :created_at, :updated_at)
        """, data)

        # Save examples
        for example in topic.examples:
            self._save_example(conn, example, topic.id)

        # Save exercises
        for exercise in topic.exercises:
            self._save_exercise(conn, exercise, topic.id)

    def _save_example(self, conn: sqlite3.Connection, example: Example, topic_id: str):
        """Save an example (internal method)."""
        data = {
            'id': example.id,
            'topic_id': topic_id,
            'title': example.title,
            'code': example.code,
            'explanation': example.explanation,
            'language': example.language,
            'difficulty': example.difficulty.value if isinstance(example.difficulty,
                                                                 DifficultyLevel) else example.difficulty,
            'tags': json.dumps(example.tags),
            'expected_output': example.expected_output,
            'execution_time_ms': example.execution_time_ms,
            'memory_usage_kb': example.memory_usage_kb,
            'metadata': json.dumps(example.metadata),
            'created_at': example.created_at.isoformat(),
            'updated_at': example.updated_at.isoformat()
        }

        conn.execute("""
            INSERT OR REPLACE INTO examples 
            (id, topic_id, title, code, explanation, language, difficulty, tags,
             expected_output, execution_time_ms, memory_usage_kb, metadata, created_at, updated_at)
            VALUES (:id, :topic_id, :title, :code, :explanation, :language, :difficulty,
                    :tags, :expected_output, :execution_time_ms, :memory_usage_kb,
                    :metadata, :created_at, :updated_at)
        """, data)

    def _save_exercise(self, conn: sqlite3.Connection, exercise: Exercise, topic_id: str):
        """Save an exercise (internal method)."""
        data = {
            'id': exercise.id,
            'topic_id': topic_id,
            'title': exercise.title,
            'description': exercise.description,
            'instructions': exercise.instructions,
            'starter_code': exercise.starter_code,
            'solution': exercise.solution,
            'difficulty': exercise.difficulty.value if isinstance(exercise.difficulty,
                                                                  DifficultyLevel) else exercise.difficulty,
            'estimated_time_minutes': exercise.estimated_time_minutes,
            'tags': json.dumps(exercise.tags),
            'hints': json.dumps(exercise.hints),
            'test_cases': json.dumps(exercise.test_cases),
            'max_attempts': exercise.max_attempts,
            'points': exercise.points,
            'language': exercise.language,
            'metadata': json.dumps(exercise.metadata),
            'created_at': exercise.created_at.isoformat(),
            'updated_at': exercise.updated_at.isoformat()
        }

        conn.execute("""
            INSERT OR REPLACE INTO exercises 
            (id, topic_id, title, description, instructions, starter_code, solution,
             difficulty, estimated_time_minutes, tags, hints, test_cases, max_attempts,
             points, language, metadata, created_at, updated_at)
            VALUES (:id, :topic_id, :title, :description, :instructions, :starter_code,
                    :solution, :difficulty, :estimated_time_minutes, :tags, :hints,
                    :test_cases, :max_attempts, :points, :language, :metadata,
                    :created_at, :updated_at)
        """, data)

    def get_language(self, language_id: str) -> Optional[Language]:
        """Get a language by ID."""
        try:
            conn = self.get_connection()
            cursor = conn.execute(
                "SELECT * FROM languages WHERE id = ?", (language_id,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            # Convert row to language object
            language_data = dict(row)

            # Parse JSON fields
            language_data['community_links'] = json.loads(language_data.get('community_links') or '[]')
            language_data['learning_path'] = json.loads(language_data.get('learning_path') or '[]')
            language_data['metadata'] = json.loads(language_data.get('metadata') or '{}')

            # Convert timestamps
            language_data['created_at'] = datetime.fromisoformat(language_data['created_at'])
            language_data['updated_at'] = datetime.fromisoformat(language_data['updated_at'])

            # Convert difficulty
            if language_data['difficulty']:
                language_data['difficulty'] = DifficultyLevel(language_data['difficulty'])

            # Load topics
            topics = self._get_topics_for_language(language_id)
            language_data['topics'] = topics

            return Language(**language_data)

        except Exception as e:
            logger.error(f"Error getting language {language_id}: {e}")
            return None

    def _get_topics_for_language(self, language_id: str) -> List[Topic]:
        """Get all topics for a language."""
        try:
            conn = self.get_connection()
            cursor = conn.execute(
                "SELECT * FROM topics WHERE language_id = ? ORDER BY order_index",
                (language_id,)
            )

            topics = []
            for row in cursor.fetchall():
                topic_data = dict(row)

                # Parse JSON fields
                for field in ['learning_objectives', 'prerequisites', 'best_practices',
                              'common_mistakes', 'additional_resources', 'tags', 'metadata']:
                    topic_data[field] = json.loads(topic_data.get(field) or '[]' if field != 'metadata' else '{}')

                # Convert timestamps
                topic_data['created_at'] = datetime.fromisoformat(topic_data['created_at'])
                topic_data['updated_at'] = datetime.fromisoformat(topic_data['updated_at'])

                # Convert difficulty
                if topic_data['difficulty']:
                    topic_data['difficulty'] = DifficultyLevel(topic_data['difficulty'])

                # Load examples and exercises
                topic_data['examples'] = self._get_examples_for_topic(topic_data['id'])
                topic_data['exercises'] = self._get_exercises_for_topic(topic_data['id'])

                # Remove language_id as it's not part of Topic model
                del topic_data['language_id']

                topics.append(Topic(**topic_data))

            return topics

        except Exception as e:
            logger.error(f"Error getting topics for language {language_id}: {e}")
            return []

    def _get_examples_for_topic(self, topic_id: str) -> List[Example]:
        """Get all examples for a topic."""
        try:
            conn = self.get_connection()
            cursor = conn.execute(
                "SELECT * FROM examples WHERE topic_id = ?", (topic_id,)
            )

            examples = []
            for row in cursor.fetchall():
                example_data = dict(row)

                # Parse JSON fields
                example_data['tags'] = json.loads(example_data.get('tags') or '[]')
                example_data['metadata'] = json.loads(example_data.get('metadata') or '{}')

                # Convert timestamps
                example_data['created_at'] = datetime.fromisoformat(example_data['created_at'])
                example_data['updated_at'] = datetime.fromisoformat(example_data['updated_at'])

                # Convert difficulty
                if example_data['difficulty']:
                    example_data['difficulty'] = DifficultyLevel(example_data['difficulty'])

                # Remove topic_id
                del example_data['topic_id']

                examples.append(Example(**example_data))

            return examples

        except Exception as e:
            logger.error(f"Error getting examples for topic {topic_id}: {e}")
            return []

    def _get_exercises_for_topic(self, topic_id: str) -> List[Exercise]:
        """Get all exercises for a topic."""
        try:
            conn = self.get_connection()
            cursor = conn.execute(
                "SELECT * FROM exercises WHERE topic_id = ?", (topic_id,)
            )

            exercises = []
            for row in cursor.fetchall():
                exercise_data = dict(row)

                # Parse JSON fields
                for field in ['tags', 'hints', 'test_cases', 'metadata']:
                    exercise_data[field] = json.loads(exercise_data.get(field) or '[]' if field != 'metadata' else '{}')

                # Convert timestamps
                exercise_data['created_at'] = datetime.fromisoformat(exercise_data['created_at'])
                exercise_data['updated_at'] = datetime.fromisoformat(exercise_data['updated_at'])

                # Convert difficulty
                if exercise_data['difficulty']:
                    exercise_data['difficulty'] = DifficultyLevel(exercise_data['difficulty'])

                # Remove topic_id
                del exercise_data['topic_id']

                exercises.append(Exercise(**exercise_data))

            return exercises

        except Exception as e:
            logger.error(f"Error getting exercises for topic {topic_id}: {e}")
            return []

    def get_all_languages(self) -> Dict[str, Language]:
        """Get all languages."""
        try:
            conn = self.get_connection()
            cursor = conn.execute(
                "SELECT id FROM languages WHERE is_active = 1 ORDER BY name"
            )

            languages = {}
            for row in cursor.fetchall():
                language_id = row[0]
                language = self.get_language(language_id)
                if language:
                    languages[language_id] = language

            return languages

        except Exception as e:
            logger.error(f"Error getting all languages: {e}")
            return {}

    # User progress operations
    def save_user_progress(self, progress: UserProgress) -> str:
        """Save or update user progress."""
        try:
            with self.transaction() as conn:
                data = {
                    'id': progress.id,
                    'user_id': progress.user_id,
                    'language_id': progress.language_id,
                    'topic_id': progress.topic_id,
                    'exercise_id': getattr(progress, 'exercise_id', None),
                    'status': progress.status.value if isinstance(progress.status, ProgressStatus) else progress.status,
                    'completion_percentage': progress.completion_percentage,
                    'time_spent_minutes': progress.time_spent_minutes,
                    'attempts': progress.attempts,
                    'last_accessed': progress.last_accessed.isoformat(),
                    'completed_examples': json.dumps(progress.completed_examples),
                    'completed_exercises': json.dumps(progress.completed_exercises),
                    'exercise_scores': json.dumps(progress.exercise_scores),
                    'notes': progress.notes,
                    'bookmarked': progress.bookmarked,
                    'metadata': json.dumps(progress.metadata),
                    'created_at': progress.created_at.isoformat(),
                    'updated_at': progress.updated_at.isoformat()
                }

                conn.execute("""
                    INSERT OR REPLACE INTO user_progress 
                    (id, user_id, language_id, topic_id, exercise_id, status, completion_percentage,
                     time_spent_minutes, attempts, last_accessed, completed_examples,
                     completed_exercises, exercise_scores, notes, bookmarked, metadata,
                     created_at, updated_at)
                    VALUES (:id, :user_id, :language_id, :topic_id, :exercise_id, :status,
                            :completion_percentage, :time_spent_minutes, :attempts, :last_accessed,
                            :completed_examples, :completed_exercises, :exercise_scores, :notes,
                            :bookmarked, :metadata, :created_at, :updated_at)
                """, data)

                return progress.id

        except Exception as e:
            logger.error(f"Error saving user progress: {e}")
            raise DatabaseError(f"Failed to save user progress: {e}")

    def get_user_progress(self, user_id: str, language_id: str = None,
                          topic_id: str = None) -> List[UserProgress]:
        """Get user progress with optional filtering."""
        try:
            conn = self.get_connection()

            query = "SELECT * FROM user_progress WHERE user_id = ?"
            params = [user_id]

            if language_id:
                query += " AND language_id = ?"
                params.append(language_id)

            if topic_id:
                query += " AND topic_id = ?"
                params.append(topic_id)

            query += " ORDER BY last_accessed DESC"

            cursor = conn.execute(query, params)

            progress_list = []
            for row in cursor.fetchall():
                progress_data = dict(row)

                # Parse JSON fields
                for field in ['completed_examples', 'completed_exercises', 'exercise_scores', 'metadata']:
                    progress_data[field] = json.loads(progress_data.get(field) or '[]' if field != 'metadata' else '{}')

                # Convert timestamps
                progress_data['created_at'] = datetime.fromisoformat(progress_data['created_at'])
                progress_data['updated_at'] = datetime.fromisoformat(progress_data['updated_at'])
                progress_data['last_accessed'] = datetime.fromisoformat(progress_data['last_accessed'])

                # Convert status
                if progress_data['status']:
                    progress_data['status'] = ProgressStatus(progress_data['status'])

                # Remove exercise_id if None
                if not progress_data.get('exercise_id'):
                    del progress_data['exercise_id']

                progress_list.append(UserProgress(**progress_data))

            return progress_list

        except Exception as e:
            logger.error(f"Error getting user progress: {e}")
            return []

    def get_learning_statistics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get learning statistics for a user."""
        try:
            conn = self.get_connection()

            # Get daily stats for the specified period
            cursor = conn.execute("""
                SELECT date, total_time_minutes, topics_completed, exercises_completed,
                       exercises_attempted, average_score, languages_practiced, streak_days
                FROM learning_stats 
                WHERE user_id = ? AND date >= date('now', '-{} days')
                ORDER BY date DESC
            """.format(days), (user_id,))

            daily_stats = []
            for row in cursor.fetchall():
                stat_data = dict(row)
                stat_data['languages_practiced'] = json.loads(stat_data.get('languages_practiced') or '[]')
                daily_stats.append(stat_data)

            # Calculate summary statistics
            total_time = sum(stat['total_time_minutes'] for stat in daily_stats)
            total_topics = sum(stat['topics_completed'] for stat in daily_stats)
            total_exercises = sum(stat['exercises_completed'] for stat in daily_stats)

            # Get current streak
            current_streak = daily_stats[0]['streak_days'] if daily_stats else 0

            # Get overall progress
            progress_cursor = conn.execute("""
                SELECT COUNT(*) as total_progress, 
                       AVG(completion_percentage) as avg_completion,
                       COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_items
                FROM user_progress WHERE user_id = ?
            """, (user_id,))

            progress_data = dict(progress_cursor.fetchone())

            return {
                'daily_stats': daily_stats,
                'summary': {
                    'total_time_minutes': total_time,
                    'total_topics_completed': total_topics,
                    'total_exercises_completed': total_exercises,
                    'current_streak_days': current_streak,
                    'avg_completion_percentage': progress_data['avg_completion'] or 0,
                    'total_progress_items': progress_data['total_progress'] or 0,
                    'completed_items': progress_data['completed_items'] or 0
                }
            }

        except Exception as e:
            logger.error(f"Error getting learning statistics: {e}")
            return {'daily_stats': [], 'summary': {}}

    def search_content(self, query: str, user_id: str = None) -> List[Dict[str, Any]]:
        """Search across all content with optional user context."""
        try:
            conn = self.get_connection()

            # Search in languages, topics, examples, and exercises
            results = []

            # Search languages
            cursor = conn.execute("""
                SELECT 'language' as type, id, name as title, description, NULL as language_name
                FROM languages 
                WHERE name LIKE ? OR description LIKE ?
                AND is_active = 1
            """, (f'%{query}%', f'%{query}%'))

            for row in cursor.fetchall():
                results.append(dict(row))

            # Search topics
            cursor = conn.execute("""
                SELECT 'topic' as type, t.id, t.title, t.description, l.name as language_name
                FROM topics t
                JOIN languages l ON t.language_id = l.id
                WHERE (t.title LIKE ? OR t.description LIKE ? OR t.content LIKE ?)
                AND t.is_published = 1 AND l.is_active = 1
            """, (f'%{query}%', f'%{query}%', f'%{query}%'))

            for row in cursor.fetchall():
                results.append(dict(row))

            # Search examples
            cursor = conn.execute("""
                SELECT 'example' as type, e.id, e.title, e.explanation as description, l.name as language_name
                FROM examples e
                JOIN topics t ON e.topic_id = t.id
                JOIN languages l ON t.language_id = l.id
                WHERE (e.title LIKE ? OR e.explanation LIKE ? OR e.code LIKE ?)
                AND t.is_published = 1 AND l.is_active = 1
            """, (f'%{query}%', f'%{query}%', f'%{query}%'))

            for row in cursor.fetchall():
                results.append(dict(row))

            # Search exercises
            cursor = conn.execute("""
                SELECT 'exercise' as type, ex.id, ex.title, ex.description, l.name as language_name
                FROM exercises ex
                JOIN topics t ON ex.topic_id = t.id
                JOIN languages l ON t.language_id = l.id
                WHERE (ex.title LIKE ? OR ex.description LIKE ?)
                AND t.is_published = 1 AND l.is_active = 1
            """, (f'%{query}%', f'%{query}%'))

            for row in cursor.fetchall():
                results.append(dict(row))

            # If user_id provided, add progress information
            if user_id:
                for result in results:
                    if result['type'] in ['topic', 'exercise']:
                        progress_cursor = conn.execute("""
                            SELECT completion_percentage, status 
                            FROM user_progress 
                            WHERE user_id = ? AND (topic_id = ? OR exercise_id = ?)
                        """, (user_id, result['id'], result['id']))

                        progress_row = progress_cursor.fetchone()
                        if progress_row:
                            result['completion_percentage'] = progress_row[0]
                            result['status'] = progress_row[1]

            return results

        except Exception as e:
            logger.error(f"Error searching content: {e}")
            return []

    def backup_database(self, backup_path: Optional[Path] = None) -> Path:
        """Create a backup of the database."""
        try:
            if backup_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = self.db_path.parent / f"backup_{timestamp}.db"

            # Close connections to allow backup
            if hasattr(self._local, 'connection'):
                self._local.connection.close()
                delattr(self._local, 'connection')

            # Copy database file
            import shutil
            shutil.copy2(self.db_path, backup_path)

            logger.info(f"Database backed up to: {backup_path}")
            return backup_path

        except Exception as e:
            logger.error(f"Error creating database backup: {e}")
            raise DatabaseError(f"Failed to backup database: {e}")

    def cleanup(self):
        """Cleanup database connections."""
        try:
            if hasattr(self._local, 'connection'):
                self._local.connection.close()
                delattr(self._local, 'connection')
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error during database cleanup: {e}")


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_database_manager() -> DatabaseManager:
    """Get the global database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def initialize_database(db_path: Optional[Path] = None) -> DatabaseManager:
    """Initialize the global database manager."""
    global _db_manager
    _db_manager = DatabaseManager(db_path)
    return _db_manager


def cleanup_database():
    """Cleanup global database manager."""
    global _db_manager
    if _db_manager:
        _db_manager.cleanup()
        _db_manager = None