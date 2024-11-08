"""Achievement model definition."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, List, Optional
from .base import Base, TimestampMixin


class Achievement(Base, TimestampMixin):
    """Model for storing user achievements."""

    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    criteria = Column(JSON)
    icon = Column(String(255))
    points = Column(Integer, nullable=False, default=0)
    earned_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="achievements")

    # Achievement categories
    CATEGORIES = {
        'LEARNING': 'learning',
        'QUIZ': 'quiz',
        'EXERCISE': 'exercise',
        'STREAK': 'streak',
        'COMMUNITY': 'community',
        'SPECIAL': 'special'
    }

    # Predefined achievements
    PREDEFINED_ACHIEVEMENTS = {
        'first_lesson': {
            'name': 'First Steps',
            'description': 'Complete your first lesson',
            'category': CATEGORIES['LEARNING'],
            'points': 10,
            'icon': 'first_steps.png'
        },
        'perfect_quiz': {
            'name': 'Perfect Score',
            'description': 'Get 100% on a quiz',
            'category': CATEGORIES['QUIZ'],
            'points': 50,
            'icon': 'perfect_score.png'
        },
        'streak_7': {
            'name': 'Week Warrior',
            'description': 'Maintain a 7-day learning streak',
            'category': CATEGORIES['STREAK'],
            'points': 100,
            'icon': 'streak_7.png'
        },
        'language_master': {
            'name': 'Language Master',
            'description': 'Complete all topics in a language',
            'category': CATEGORIES['LEARNING'],
            'points': 500,
            'icon': 'master.png'
        }
    }

    def __repr__(self):
        return f"<Achievement(id={self.id}, name='{self.name}', user_id={self.user_id})>"

    @classmethod
    def get_for_user(cls, db_session, user_id: int) -> List['Achievement']:
        """Get all achievements for a user."""
        return db_session.query(cls).filter_by(user_id=user_id).order_by(cls.earned_at.desc()).all()

    @classmethod
    def award_achievement(cls, db_session, user_id: int, achievement_key: str) -> Optional['Achievement']:
        """Award an achievement to a user."""
        if achievement_key not in cls.PREDEFINED_ACHIEVEMENTS:
            return None

        # Check if already earned
        existing = db_session.query(cls).filter_by(
            user_id=user_id,
            name=cls.PREDEFINED_ACHIEVEMENTS[achievement_key]['name']
        ).first()

        if existing:
            return None

        # Create new achievement
        achievement_data = cls.PREDEFINED_ACHIEVEMENTS[achievement_key].copy()
        achievement_data.update({
            'user_id': user_id,
            'earned_at': datetime.utcnow()
        })

        achievement = cls(**achievement_data)
        db_session.add(achievement)
        db_session.commit()
        return achievement

    @classmethod
    def check_achievements(cls, db_session, user_id: int) -> List['Achievement']:
        """Check and award any newly earned achievements."""
        new_achievements = []

        # Check learning progress
        completed_topics = db_session.query(Progress).filter_by(
            user_id=user_id,
            status='completed'
        ).count()

        if completed_topics > 0:
            achievement = cls.award_achievement(db_session, user_id, 'first_lesson')
            if achievement:
                new_achievements.append(achievement)

        # Check quiz performance
        perfect_quizzes = db_session.query(QuizSubmission).filter_by(
            user_id=user_id,
            score=100
        ).count()

        if perfect_quizzes > 0:
            achievement = cls.award_achievement(db_session, user_id, 'perfect_quiz')
            if achievement:
                new_achievements.append(achievement)

        # Add more achievement checks as needed...
        return new_achievements

    @classmethod
    def get_leaderboard(cls, db_session, limit: int = 10) -> List[Dict]:
        """Get achievement leaderboard."""
        from sqlalchemy import func
        from .user import User

        return db_session.query(
            User.username,
            func.count(cls.id).label('total_achievements'),
            func.sum(cls.points).label('total_points')
        ).join(
            cls, User.id == cls.user_id
        ).group_by(
            User.id
        ).order_by(
            func.sum(cls.points).desc()
        ).limit(limit).all()

    def to_dict(self) -> Dict:
        """Convert achievement to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'criteria': self.criteria,
            'icon': self.icon,
            'points': self.points,
            'earned_at': self.earned_at.isoformat() if self.earned_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }