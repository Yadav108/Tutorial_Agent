"""User model definition."""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin, DatabaseError


class User(Base, TimestampMixin):
    """User model for storing user account information."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    progress = relationship("Progress", back_populates="user")
    submissions = relationship("CodeSubmission", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"