"""Quiz model definition."""
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Quiz(Base, TimestampMixin):
    """Model for storing quiz information."""

    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, ForeignKey('contents.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    questions = Column(JSON, nullable=False)  # List of questions with answers
    time_limit = Column(Integer)  # Time limit in minutes
    passing_score = Column(Float, default=70.0)  # Minimum score to pass
    difficulty = Column(Integer)  # 1-5 scale
    max_attempts = Column(Integer, default=3)  # Maximum number of attempts allowed

    # Relationships
    submissions = relationship("QuizSubmission", back_populates="quiz")
    content = relationship("Content", back_populates="quizzes")

    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}')>"

    def to_dict(self):
        """Convert quiz to dictionary representation."""
        return {
            'id': self.id,
            'content_id': self.content_id,
            'title': self.title,
            'description': self.description,
            'time_limit': self.time_limit,
            'passing_score': self.passing_score,
            'difficulty': self.difficulty,
            'max_attempts': self.max_attempts
        }


class QuizSubmission(Base, TimestampMixin):
    """Model for storing quiz submission information."""

    __tablename__ = 'quiz_submissions'

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    answers = Column(JSON)  # User's submitted answers
    score = Column(Float)  # Score achieved (percentage)
    time_taken = Column(Integer)  # Time taken in seconds
    attempt_number = Column(Integer, default=1)  # Which attempt this is
    status = Column(String(50))  # started, completed, abandoned
    feedback = Column(JSON)  # Feedback for each question

    # Relationships
    quiz = relationship("Quiz", back_populates="submissions")
    user = relationship("User", back_populates="quiz_submissions")

    def __repr__(self):
        return f"<QuizSubmission(quiz_id={self.quiz_id}, user_id={self.user_id}, score={self.score})>"

    def to_dict(self):
        """Convert submission to dictionary representation."""
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'user_id': self.user_id,
            'score': self.score,
            'time_taken': self.time_taken,
            'attempt_number': self.attempt_number,
            'status': self.status
        }

    @property
    def is_passing(self):
        """Check if submission achieved passing score."""
        return self.score >= self.quiz.passing_score if self.score is not None else False

    def calculate_score(self):
        """Calculate score based on submitted answers."""
        if not self.answers or not self.quiz.questions:
            return 0.0

        correct_count = 0
        total_questions = len(self.quiz.questions)

        for q_idx, answer in self.answers.items():
            question = self.quiz.questions[int(q_idx)]
            if answer == question.get('correct_answer'):
                correct_count += 1

        self.score = (correct_count / total_questions) * 100.0
        return self.score