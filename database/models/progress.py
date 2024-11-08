from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from database.models.base import Base


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class AchievementType(Enum):
    COMPLETION = "completion"
    STREAK = "streak"
    MASTERY = "mastery"
    SPEED = "speed"
    PERFECT_SCORE = "perfect_score"

class Progress(Base):
    __tablename__ = 'progress'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    language = Column(String(50))
    topic = Column(String(100))
    subtopic = Column(String(100))
    completion_percentage = Column(Float, default=0.0)
    exercises_completed = Column(Integer, default=0)
    exercises_total = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    assessment_scores = Column(JSON)

    user = relationship("User", back_populates="progress")

class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String(50))
    name = Column(String(100))
    description = Column(String(500))
    criteria = Column(JSON)
    earned_date = Column(DateTime)
    language = Column(String(50))
    icon = Column(String(100))

    user = relationship("User", back_populates="achievements")

class ProgressTracker:
    def __init__(self, session):
        self.session = session

    def update_progress(self, user_id: int, language: str, topic: str,
                       subtopic: str, completion: float, exercises_done: int,
                       total_exercises: int) -> Progress:
        """Update user's progress for a specific topic."""
        progress = self.session.query(Progress).filter_by(
            user_id=user_id,
            language=language,
            topic=topic,
            subtopic=subtopic
        ).first()

        if not progress:
            progress = Progress(
                user_id=user_id,
                language=language,
                topic=topic,
                subtopic=subtopic
            )
            self.session.add(progress)

        progress.completion_percentage = completion
        progress.exercises_completed = exercises_done
        progress.exercises_total = total_exercises
        progress.last_accessed = datetime.utcnow()
        progress.completed = (completion >= 100.0)

        self.session.commit()
        self._check_achievements(user_id, language)
        return progress

    def get_user_progress(self, user_id: int, language: str = None) -> List[Progress]:
        """Get user's progress, optionally filtered by language."""
        query = self.session.query(Progress).filter_by(user_id=user_id)
        if language:
            query = query.filter_by(language=language)
        return query.all()

    def _check_achievements(self, user_id: int, language: str):
        """Check and award achievements based on user's progress."""
        achievements_to_check = [
            self._check_language_completion,
            self._check_exercise_streak,
            self._check_topic_mastery,
            self._check_speed_learning,
            self._check_perfect_scores
        ]

        for check_function in achievements_to_check:
            achievement = check_function(user_id, language)
            if achievement:
                self._award_achievement(user_id, achievement)

    def _check_language_completion(self, user_id: int, language: str) -> Optional[Dict]:
        """Check if user has completed all topics in a language."""
        progress = self.get_user_progress(user_id, language)
        if not progress:
            return None

        total_completion = sum(p.completion_percentage for p in progress) / len(progress)
        if total_completion >= 100.0:
            return {
                "type": AchievementType.COMPLETION.value,
                "name": f"{language} Master",
                "description": f"Completed all {language} tutorials",
                "language": language,
                "icon": "trophy"
            }
        return None

    def _check_exercise_streak(self, user_id: int, language: str) -> Optional[Dict]:
        """Check for consecutive days of completed exercises."""
        progress = self.get_user_progress(user_id, language)
        if not progress:
            return None

        # Calculate streak based on last_accessed dates
        dates = sorted(set(p.last_accessed.date() for p in progress))
        current_streak = 1
        max_streak = 1

        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1

        if max_streak >= 7:  # One week streak
            return {
                "type": AchievementType.STREAK.value,
                "name": "Consistent Learner",
                "description": f"{max_streak} day learning streak in {language}",
                "language": language,
                "icon": "fire"
            }
        return None

    def _award_achievement(self, user_id: int, achievement_data: Dict):
        """Award an achievement to the user if they don't already have it."""
        existing = self.session.query(Achievement).filter_by(
            user_id=user_id,
            type=achievement_data["type"],
            name=achievement_data["name"]
        ).first()

        if not existing:
            achievement = Achievement(
                user_id=user_id,
                type=achievement_data["type"],
                name=achievement_data["name"],
                description=achievement_data["description"],
                language=achievement_data["language"],
                icon=achievement_data["icon"],
                earned_date=datetime.utcnow()
            )
            self.session.add(achievement)
            self.session.commit()