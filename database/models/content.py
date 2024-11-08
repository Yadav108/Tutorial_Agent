"""Content model definition."""
from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Content(Base, TimestampMixin):
    """Content model for tutorials, exercises, and quizzes."""

    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # tutorial, exercise, quiz
    language = Column(String(50), nullable=False)
    content_text = Column(Text)  # Renamed from 'content' to avoid confusion
    content_metadata = Column(JSON)  # Renamed from 'metadata' as it's a reserved word
    topic_id = Column(String(100))  # Added to identify topics
    difficulty = Column(Integer)
    order = Column(Integer)  # For ordering topics within a language
    prerequisites = Column(JSON)  # List of prerequisite topic IDs

    # Relationships
    progress = relationship("Progress", back_populates="content")
    submissions = relationship("CodeSubmission", back_populates="content")

    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title}', type='{self.type}')>"

    @property
    def is_complete(self):
        """Check if content has all required fields."""
        return all([
            self.title,
            self.type,
            self.language,
            self.content_text
        ])

    def to_dict(self):
        """Convert content to dictionary representation."""
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'language': self.language,
            'content_text': self.content_text,
            'content_metadata': self.content_metadata,
            'topic_id': self.topic_id,
            'difficulty': self.difficulty,
            'order': self.order,
            'prerequisites': self.prerequisites
        }