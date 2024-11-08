"""Code submission model definition."""
from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, Float, JSON, func,
    case, distinct
)
from sqlalchemy.orm import relationship
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .base import Base, TimestampMixin


class CodeSubmission(Base, TimestampMixin):
    """Model for storing code submissions."""

    __tablename__ = 'code_submissions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    language = Column(String(50), nullable=False)
    topic_id = Column(String(100), nullable=False)
    exercise_id = Column(String(100), nullable=False)
    code = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    results = Column(JSON)
    feedback = Column(Text)
    execution_time = Column(Float)
    memory_usage = Column(Integer)

    # Relationships
    user = relationship("User", back_populates="code_submissions")

    # Submission status options
    STATUS_CHOICES = {
        'PENDING': 'pending',
        'RUNNING': 'running',
        'COMPLETED': 'completed',
        'FAILED': 'failed',
        'ERROR': 'error'
    }

    def __repr__(self):
        return f"<CodeSubmission(id={self.id}, user_id={self.user_id}, status='{self.status}')>"

    @classmethod
    def get_user_submissions(cls, db_session, user_id: int,
                             language: Optional[str] = None,
                             topic_id: Optional[str] = None) -> List['CodeSubmission']:
        """Get submissions for a user."""
        query = db_session.query(cls).filter_by(user_id=user_id)

        if language:
            query = query.filter_by(language=language)

        if topic_id:
            query = query.filter_by(topic_id=topic_id)

        return query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_latest_submission(cls, db_session, user_id: int,
                              language: str, exercise_id: str) -> Optional['CodeSubmission']:
        """Get user's latest submission for an exercise."""
        return db_session.query(cls).filter_by(
            user_id=user_id,
            language=language,
            exercise_id=exercise_id
        ).order_by(cls.created_at.desc()).first()

    def update_status(self, db_session, status: str, results: Dict = None,
                      execution_time: float = None, memory_usage: int = None):
        """Update submission status and results."""
        if status not in self.STATUS_CHOICES.values():
            raise ValueError(f"Invalid status. Must be one of: {', '.join(self.STATUS_CHOICES.values())}")

        self.status = status
        if results:
            self.results = results
        if execution_time is not None:
            self.execution_time = execution_time
        if memory_usage is not None:
            self.memory_usage = memory_usage

        db_session.add(self)
        db_session.commit()

    def add_feedback(self, db_session, feedback: str):
        """Add feedback to submission."""
        self.feedback = feedback
        db_session.add(self)
        db_session.commit()

    @classmethod
    def get_submission_statistics(cls, db_session, user_id: int) -> Dict:
        """Get submission statistics for a user."""
        stats = db_session.query(
            cls.language,
            func.count().label('total_submissions'),
            func.sum(
                case(
                    [(cls.status == 'completed', 1)],
                    else_=0
                )
            ).label('successful_submissions'),
            func.avg(cls.execution_time).label('avg_execution_time'),
            func.avg(cls.memory_usage).label('avg_memory_usage')
        ).filter_by(user_id=user_id).group_by(cls.language).all()

        return {
            row.language: {
                'total_submissions': row.total_submissions,
                'successful_submissions': row.successful_submissions,
                'success_rate': (
                    row.successful_submissions / row.total_submissions * 100
                    if row.total_submissions > 0 else 0
                ),
                'avg_execution_time': round(row.avg_execution_time or 0, 3),
                'avg_memory_usage': round(row.avg_memory_usage or 0, 2)
            }
            for row in stats
        }

    @classmethod
    def cleanup_old_submissions(cls, db_session, days: int = 30):
        """Clean up old submissions."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        db_session.query(cls).filter(cls.created_at < cutoff_date).delete()
        db_session.commit()

    @classmethod
    def get_popular_exercises(cls, db_session, language: str = None, limit: int = 10) -> List[Dict]:
        """Get most attempted exercises."""
        query = db_session.query(
            cls.language,
            cls.exercise_id,
            func.count().label('attempt_count'),
            func.count(distinct(cls.user_id)).label('unique_users')
        )

        if language:
            query = query.filter_by(language=language)

        return query.group_by(
            cls.language, cls.exercise_id
        ).order_by(
            func.count().desc()
        ).limit(limit).all()

    def to_dict(self) -> Dict:
        """Convert submission to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'language': self.language,
            'topic_id': self.topic_id,
            'exercise_id': self.exercise_id,
            'code': self.code,
            'status': self.status,
            'results': self.results,
            'feedback': self.feedback,
            'execution_time': self.execution_time,
            'memory_usage': self.memory_usage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }