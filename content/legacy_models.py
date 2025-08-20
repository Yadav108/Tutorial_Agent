"""
Legacy compatibility models for Tutorial Agent

This module provides backward compatibility for existing content files
that use the old model structure.
"""

from typing import List, Optional
from dataclasses import dataclass, field
import uuid

from .models import (
    DifficultyLevel, ResourceType, QuizType, 
    Resource as NewResource,
    Example as NewExample,
    Exercise as NewExercise,
    Topic as NewTopic,
    QuizQuestion as NewQuizQuestion
)


@dataclass 
class Exercise:
    """Legacy Exercise class for backward compatibility."""
    title: str
    description: str
    starter_code: str
    solution: str
    difficulty: str = "Beginner"
    hints: List[str] = field(default_factory=list)
    
    def to_new_exercise(self) -> NewExercise:
        """Convert to new Exercise format."""
        # Convert string difficulty to enum
        difficulty_map = {
            "Beginner": DifficultyLevel.BEGINNER,
            "Intermediate": DifficultyLevel.INTERMEDIATE,
            "Advanced": DifficultyLevel.ADVANCED,
            "beginner": DifficultyLevel.BEGINNER,
            "intermediate": DifficultyLevel.INTERMEDIATE,
            "advanced": DifficultyLevel.ADVANCED
        }
        
        diff_enum = difficulty_map.get(self.difficulty, DifficultyLevel.BEGINNER)
        
        return NewExercise(
            id=str(uuid.uuid4()),
            title=self.title,
            description=self.description,
            starter_code=self.starter_code,
            solution=self.solution,
            difficulty=diff_enum,
            hints=self.hints
        )


@dataclass
class Topic:
    """Legacy Topic class for backward compatibility."""
    title: str
    description: str
    content: str
    examples: List[NewExample] = field(default_factory=list)
    exercises: List[Exercise] = field(default_factory=list)  # Use legacy Exercise
    best_practices: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    def to_new_topic(self) -> NewTopic:
        """Convert to new Topic format."""
        # Convert legacy exercises to new format
        new_exercises = [ex.to_new_exercise() for ex in self.exercises]
        
        return NewTopic(
            id=str(uuid.uuid4()),
            title=self.title,
            description=self.description,
            content=self.content,
            examples=self.examples,
            exercises=new_exercises,
            best_practices=self.best_practices,
            dependencies=self.dependencies
        )


# Export legacy classes for use in content files
__all__ = ['Exercise', 'Topic']