"""Learning Path model definition."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from typing import Dict, List, Optional
from datetime import datetime
from .base import Base, TimestampMixin


class LearningPath(Base, TimestampMixin):
    """Model for storing learning paths."""

    __tablename__ = 'learning_paths'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    language = Column(String(50), nullable=False)
    level = Column(String(50), nullable=False)
    topics = Column(JSON, nullable=False)
    estimated_duration = Column(Integer)  # in days
    prerequisites = Column(JSON)
    is_custom = Column(Boolean, nullable=False, default=False)
    status = Column(String(50), nullable=False, default='not_started')
    completion_percentage = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="learning_paths")

    # Status choices
    STATUS_CHOICES = {
        'NOT_STARTED': 'not_started',
        'IN_PROGRESS': 'in_progress',
        'COMPLETED': 'completed',
        'PAUSED': 'paused'
    }

    # Level choices
    LEVEL_CHOICES = {
        'BEGINNER': 'beginner',
        'INTERMEDIATE': 'intermediate',
        'ADVANCED': 'advanced'
    }

    def __repr__(self):
        return f"<LearningPath(id={self.id}, title='{self.title}', user_id={self.user_id})>"

    @classmethod
    def get_for_user(cls, db_session, user_id: int) -> List['LearningPath']:
        """Get all learning paths for a user."""
        return db_session.query(cls).filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_recommended_paths(cls, db_session, user_id: int, language: str = None) -> List['LearningPath']:
        """Get recommended learning paths based on user's progress."""
        from .progress import Progress

        # Calculate user's progress statistics
        progress_stats = db_session.query(Progress).filter_by(user_id=user_id)
        total_topics = progress_stats.count()
        completed_topics = progress_stats.filter_by(status='completed').count()

        # Determine appropriate level
        completion_rate = (completed_topics / total_topics * 100) if total_topics > 0 else 0
        if completion_rate < 30:
            recommended_level = cls.LEVEL_CHOICES['BEGINNER']
        elif completion_rate < 70:
            recommended_level = cls.LEVEL_CHOICES['INTERMEDIATE']
        else:
            recommended_level = cls.LEVEL_CHOICES['ADVANCED']

        # Query for recommended paths
        query = db_session.query(cls).filter_by(
            is_custom=False,
            level=recommended_level
        )

        if language:
            query = query.filter_by(language=language)

        return query.order_by(cls.created_at.desc()).limit(5).all()

    def update_progress(self, db_session):
        """Update path completion percentage."""
        from .progress import Progress

        if not self.topics:
            return

        completed_topics = 0
        total_topics = len(self.topics)

        for topic_id in self.topics:
            progress = db_session.query(Progress).filter_by(
                user_id=self.user_id,
                topic_id=topic_id,
                status='completed'
            ).first()

            if progress:
                completed_topics += 1

        self.completion_percentage = int((completed_topics / total_topics) * 100)

        # Update status based on completion
        if self.completion_percentage == 100:
            self.status = self.STATUS_CHOICES['COMPLETED']
        elif self.completion_percentage > 0:
            self.status = self.STATUS_CHOICES['IN_PROGRESS']

        db_session.add(self)
        db_session.commit()

    def check_prerequisites(self, db_session) -> bool:
        """Check if prerequisites are met."""
        if not self.prerequisites:
            return True

        from .progress import Progress

        for prereq in self.prerequisites:
            progress = db_session.query(Progress).filter_by(
                user_id=self.user_id,
                topic_id=prereq['topic_id'],
                language=prereq.get('language', self.language),
                status='completed'
            ).first()

            if not progress:
                return False

        return True

    def get_next_topic(self, db_session) -> Optional[str]:
        """Get next incomplete topic in path."""
        if not self.topics:
            return None

        from .progress import Progress

        for topic_id in self.topics:
            progress = db_session.query(Progress).filter_by(
                user_id=self.user_id,
                topic_id=topic_id,
                status='completed'
            ).first()

            if not progress:
                return topic_id

        return None

    def clone_for_user(self, db_session, user_id: int) -> 'LearningPath':
        """Create a copy of this path for another user."""
        new_path = LearningPath(
            user_id=user_id,
            title=self.title,
            description=self.description,
            language=self.language,
            level=self.level,
            topics=self.topics,
            estimated_duration=self.estimated_duration,
            prerequisites=self.prerequisites,
            is_custom=True,
            status=self.STATUS_CHOICES['NOT_STARTED'],
            completion_percentage=0
        )

        db_session.add(new_path)
        db_session.commit()
        return new_path

    @classmethod
    def create_default_paths(cls, db_session):
        """Create default learning paths."""
        default_paths = [
            {
                'title': 'Python Basics',
                'description': 'A beginner-friendly path to learn Python fundamentals',
                'language': 'python',
                'level': cls.LEVEL_CHOICES['BEGINNER'],
                'topics': [
                    'python_intro',
                    'python_variables',
                    'python_controlflow',
                    'python_functions'
                ],
                'estimated_duration': 14,
                'prerequisites': []
            },
            {
                'title': 'Advanced Python Development',
                'description': 'Deep dive into advanced Python concepts',
                'language': 'python',
                'level': cls.LEVEL_CHOICES['ADVANCED'],
                'topics': [
                    'python_oop',
                    'python_decorators',
                    'python_async',
                    'python_testing'
                ],
                'estimated_duration': 30,
                'prerequisites': [
                    {'topic_id': 'python_intro'},
                    {'topic_id': 'python_functions'}
                ]
            }
        ]

        for path_data in default_paths:
            path = cls(
                user_id=0,  # System user
                is_custom=False,
                status=cls.STATUS_CHOICES['NOT_STARTED'],
                completion_percentage=0,
                **path_data
            )
            db_session.add(path)

        db_session.commit()

    def to_dict(self) -> Dict:
        """Convert learning path to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'language': self.language,
            'level': self.level,
            'topics': self.topics,
            'estimated_duration': self.estimated_duration,
            'prerequisites': self.prerequisites,
            'is_custom': self.is_custom,
            'status': self.status,
            'completion_percentage': self.completion_percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }