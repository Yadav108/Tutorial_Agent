"""Database handler module for Tutorial Agent."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import logging
from typing import Optional
from pathlib import Path

from .models import Base
from config.settings import Settings


class DatabaseHandler:
    """Handles database connections and operations."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseHandler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.settings = Settings()
        self.engine = None
        self.session_factory = None
        self._initialized = True
        self.logger = logging.getLogger(__name__)

    def initialize(self, db_url: Optional[str] = None) -> bool:
        """
        Initialize the database connection and create tables.

        Args:
            db_url: Optional database URL. If not provided, uses default from settings.

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Get database URL from settings if not provided
            if db_url is None:
                db_path = Path(self.settings.DATA_DIR) / 'tutorial_agent.db'
                db_url = f'sqlite:///{db_path}'

            # Create engine
            self.engine = create_engine(
                db_url,
                echo=self.settings.get('database', 'echo', False),
                pool_size=self.settings.get('database', 'pool_size', 5),
                max_overflow=self.settings.get('database', 'max_overflow', 10)
            )

            # Create session factory
            self.session_factory = sessionmaker(bind=self.engine)

            # Create all tables
            Base.metadata.create_all(self.engine)

            self.logger.info(f"Database initialized successfully at {db_url}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize database: {str(e)}")
            return False

    @contextmanager
    def get_session(self):
        """
        Get a database session within a context manager.

        Yields:
            Session: Database session
        """
        session = scoped_session(self.session_factory)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.remove()

    def create_tables(self) -> bool:
        """
        Create all database tables.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            Base.metadata.create_all(self.engine)
            self.logger.info("Database tables created successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create tables: {str(e)}")
            return False

    def drop_tables(self) -> bool:
        """
        Drop all database tables.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            Base.metadata.drop_all(self.engine)
            self.logger.info("Database tables dropped successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to drop tables: {str(e)}")
            return False

    def check_connection(self) -> bool:
        """
        Check if database connection is working.

        Returns:
            bool: True if connection is working, False otherwise
        """
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
            return True
        except Exception as e:
            self.logger.error(f"Database connection check failed: {str(e)}")
            return False

    def vacuum(self) -> bool:
        """
        Perform database vacuum (SQLite only).

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.get_session() as session:
                session.execute("VACUUM")
            self.logger.info("Database vacuum completed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to vacuum database: {str(e)}")
            return False


# Global database handler instance
db = DatabaseHandler()