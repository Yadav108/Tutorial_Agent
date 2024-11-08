"""Base model and database utilities."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime

class DatabaseError(Exception):
    """Base exception for database errors."""
    pass

# Create the declarative base
Base = declarative_base()

class TimestampMixin:
    """Mixin for adding created_at and updated_at timestamps to models."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

__all__ = ['Base', 'TimestampMixin', 'DatabaseError']