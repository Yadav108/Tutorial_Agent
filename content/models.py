"""
Content Models for Tutorial Agent

This module defines the data models used throughout the Tutorial Agent
application for representing tutorial content, exercises, and user progress.

Classes:
    - DifficultyLevel: Enumeration of difficulty levels
    - ResourceType: Enumeration of resource types
    - QuizType: Enumeration of quiz question types
    - Resource: External learning resource
    - Example: Code example with explanation
    - Exercise: Programming exercise
    - QuizQuestion: Quiz question
    - Topic: Tutorial topic containing content
    - Language: Programming language with topics
    - UserProgress: User's progress tracking
    - Achievement: User achievement
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime
import uuid


class DifficultyLevel(Enum):
    """Enumeration for content difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ResourceType(Enum):
    """Enumeration for external resource types."""
    DOCUMENTATION = "documentation"
    TUTORIAL = "tutorial" 
    VIDEO = "video"
    BOOK = "book"
    ARTICLE = "article"
    INTERACTIVE = "interactive"
    TOOL = "tool"


class QuizType(Enum):
    """Enumeration for quiz question types."""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    CODE_COMPLETION = "code_completion"
    DRAG_DROP = "drag_drop"

@dataclass
class Resource:
    """External learning resource with metadata."""
    title: str
    url: str
    resource_type: ResourceType = ResourceType.DOCUMENTATION
    description: str = ""
    is_free: bool = True
    language: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    estimated_time_minutes: Optional[int] = None
    rating: Optional[float] = None
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate resource data after initialization."""
        if not self.title.strip():
            raise ValueError("Resource title cannot be empty")
        if not self.url.strip():
            raise ValueError("Resource URL cannot be empty")
        if self.rating is not None and not (0 <= self.rating <= 5):
            raise ValueError("Rating must be between 0 and 5")


@dataclass
class Example:
    """Code example with explanation and metadata."""
    title: str
    code: str
    explanation: str = ""
    language: Optional[str] = None
    output: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    tags: List[str] = field(default_factory=list)
    runnable: bool = True
    
    def __post_init__(self):
        """Validate example data after initialization."""
        if not self.title.strip():
            raise ValueError("Example title cannot be empty")
        if not self.code.strip():
            raise ValueError("Example code cannot be empty")


@dataclass
class Exercise:
    """Programming exercise with validation and metadata."""
    id: str
    title: str
    description: str
    starter_code: str
    solution: str
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    hints: List[str] = field(default_factory=list)
    test_cases: List[Dict[str, Any]] = field(default_factory=list)
    estimated_time_minutes: int = 15
    points: int = 10
    tags: List[str] = field(default_factory=list)
    language: Optional[str] = None
    
    def __post_init__(self):
        """Validate exercise data after initialization."""
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.title.strip():
            raise ValueError("Exercise title cannot be empty")
        if not self.description.strip():
            raise ValueError("Exercise description cannot be empty")
        if self.estimated_time_minutes <= 0:
            raise ValueError("Estimated time must be positive")
        if self.points <= 0:
            raise ValueError("Points must be positive")


# Legacy compatibility for existing content
def create_legacy_exercise(title: str, description: str, starter_code: str = "", 
                         solution: str = "", difficulty: str = "Beginner", 
                         hints: List[str] = None) -> Exercise:
    """Create an Exercise with legacy parameters for backward compatibility."""
    # Convert old string difficulty to new enum
    difficulty_map = {
        "Beginner": DifficultyLevel.BEGINNER,
        "Intermediate": DifficultyLevel.INTERMEDIATE, 
        "Advanced": DifficultyLevel.ADVANCED,
        "beginner": DifficultyLevel.BEGINNER,
        "intermediate": DifficultyLevel.INTERMEDIATE,
        "advanced": DifficultyLevel.ADVANCED
    }
    
    diff_enum = difficulty_map.get(difficulty, DifficultyLevel.BEGINNER)
    
    return Exercise(
        id=str(uuid.uuid4()),
        title=title,
        description=description,
        starter_code=starter_code,
        solution=solution,
        difficulty=diff_enum,
        hints=hints or []
    )


@dataclass
class QuizQuestion:
    """Quiz question with multiple choice support."""
    id: str
    question_text: str
    quiz_type: QuizType = QuizType.MULTIPLE_CHOICE
    options: List[str] = field(default_factory=list)
    correct_answers: List[Union[str, int]] = field(default_factory=list)
    explanation: str = ""
    points: int = 1
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate quiz question data."""
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.question_text.strip():
            raise ValueError("Question text cannot be empty")
        if self.quiz_type == QuizType.MULTIPLE_CHOICE and len(self.options) < 2:
            raise ValueError("Multiple choice questions must have at least 2 options")
        if not self.correct_answers:
            raise ValueError("At least one correct answer must be provided")
        if self.points <= 0:
            raise ValueError("Points must be positive")
    
    def is_correct(self, user_answers: List[Union[str, int]]) -> bool:
        """Check if the user's answers are correct."""
        return sorted(user_answers) == sorted(self.correct_answers)

@dataclass
class Topic:
    """Tutorial topic with comprehensive content structure."""
    id: str
    title: str
    description: str
    content: str
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    examples: List[Example] = field(default_factory=list)
    exercises: List[Exercise] = field(default_factory=list)
    quiz_questions: List[QuizQuestion] = field(default_factory=list)
    resources: List[Resource] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    common_mistakes: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_time_minutes: int = 30
    order_index: int = 0
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate topic data after initialization."""
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.title.strip():
            raise ValueError("Topic title cannot be empty")
        if not self.description.strip():
            raise ValueError("Topic description cannot be empty")
        if not self.content.strip():
            raise ValueError("Topic content cannot be empty")
        if self.estimated_time_minutes <= 0:
            raise ValueError("Estimated time must be positive")
    
    def get_total_exercises(self) -> int:
        """Get total number of exercises in this topic."""
        return len(self.exercises)
    
    def get_total_quiz_questions(self) -> int:
        """Get total number of quiz questions in this topic."""
        return len(self.quiz_questions)
    
    def get_total_points(self) -> int:
        """Calculate total points available from exercises and quizzes."""
        exercise_points = sum(ex.points for ex in self.exercises)
        quiz_points = sum(q.points for q in self.quiz_questions)
        return exercise_points + quiz_points


@dataclass
class Language:
    """Programming language course with comprehensive structure."""
    id: str
    name: str
    description: str
    topics: List[Topic]
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    prerequisites: List[str] = field(default_factory=list)
    learning_path: List[str] = field(default_factory=list)
    resources: List[Resource] = field(default_factory=list)
    icon_path: str = ""
    color_theme: str = "#007bff"
    estimated_hours: int = 40
    category: str = "programming"
    version: str = "1.0"
    recommended_tools: List[Dict[str, Any]] = field(default_factory=list)
    project_ideas: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate language data after initialization."""
        if not self.id:
            self.id = self.name.lower().replace(' ', '_')
        if not self.name.strip():
            raise ValueError("Language name cannot be empty")
        if not self.description.strip():
            raise ValueError("Language description cannot be empty")
        if not self.topics:
            raise ValueError("Language must have at least one topic")
        if self.estimated_hours <= 0:
            raise ValueError("Estimated hours must be positive")
    
    def get_topic_by_id(self, topic_id: str) -> Optional[Topic]:
        """Get topic by ID."""
        for topic in self.topics:
            if topic.id == topic_id:
                return topic
        return None
    
    def get_topic_by_title(self, title: str) -> Optional[Topic]:
        """Get topic by title."""
        for topic in self.topics:
            if topic.title == title:
                return topic
        return None
    
    def get_topic_dependencies(self, topic_id: str) -> List[str]:
        """Get prerequisites for a specific topic."""
        topic = self.get_topic_by_id(topic_id)
        return topic.dependencies if topic else []
    
    def get_ordered_topics(self) -> List[Topic]:
        """Get topics ordered by their order_index."""
        return sorted(self.topics, key=lambda t: t.order_index)
    
    def get_topics_by_difficulty(self, difficulty: DifficultyLevel) -> List[Topic]:
        """Get topics filtered by difficulty level."""
        return [topic for topic in self.topics if topic.difficulty == difficulty]
    
    def get_total_exercises(self) -> int:
        """Get total number of exercises across all topics."""
        return sum(topic.get_total_exercises() for topic in self.topics)
    
    def get_total_quiz_questions(self) -> int:
        """Get total number of quiz questions across all topics."""
        return sum(topic.get_total_quiz_questions() for topic in self.topics)
    
    def get_total_points(self) -> int:
        """Get total points available across all topics."""
        return sum(topic.get_total_points() for topic in self.topics)


@dataclass
class UserProgress:
    """Track user's learning progress."""
    user_id: str
    language_id: str
    topic_progresses: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    completed_exercises: List[str] = field(default_factory=list)
    completed_quizzes: List[str] = field(default_factory=list)
    total_points_earned: int = 0
    total_time_spent_minutes: int = 0
    current_topic_id: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    completion_percentage: float = 0.0
    
    def update_topic_progress(self, topic_id: str, progress_data: Dict[str, Any]):
        """Update progress for a specific topic."""
        self.topic_progresses[topic_id] = {
            **self.topic_progresses.get(topic_id, {}),
            **progress_data,
            'last_updated': datetime.now().isoformat()
        }
        self.last_activity = datetime.now()
    
    def mark_exercise_completed(self, exercise_id: str, points_earned: int = 0):
        """Mark an exercise as completed."""
        if exercise_id not in self.completed_exercises:
            self.completed_exercises.append(exercise_id)
            self.total_points_earned += points_earned
            self.last_activity = datetime.now()
    
    def mark_quiz_completed(self, quiz_id: str, points_earned: int = 0):
        """Mark a quiz as completed."""
        if quiz_id not in self.completed_quizzes:
            self.completed_quizzes.append(quiz_id)
            self.total_points_earned += points_earned
            self.last_activity = datetime.now()
    
    def get_topic_completion(self, topic_id: str) -> float:
        """Get completion percentage for a specific topic."""
        return self.topic_progresses.get(topic_id, {}).get('completion', 0.0)


@dataclass
class Achievement:
    """User achievement/badge."""
    id: str
    title: str
    description: str
    icon_path: str = ""
    points_required: int = 0
    exercises_required: int = 0
    topics_required: int = 0
    language_specific: Optional[str] = None
    unlocked_at: Optional[datetime] = None
    rarity: str = "common"  # common, rare, epic, legendary
    
    def __post_init__(self):
        """Validate achievement data."""
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.title.strip():
            raise ValueError("Achievement title cannot be empty")
        if not self.description.strip():
            raise ValueError("Achievement description cannot be empty")
    
    def is_unlocked(self, user_progress: UserProgress) -> bool:
        """Check if this achievement should be unlocked for the user."""
        if self.unlocked_at is not None:
            return True
        
        # Check requirements
        if self.points_required > 0 and user_progress.total_points_earned < self.points_required:
            return False
            
        if self.exercises_required > 0 and len(user_progress.completed_exercises) < self.exercises_required:
            return False
            
        if self.topics_required > 0:
            completed_topics = sum(1 for progress in user_progress.topic_progresses.values() 
                                 if progress.get('completion', 0) >= 100)
            if completed_topics < self.topics_required:
                return False
        
        return True


# Utility functions for working with models
def create_sample_language() -> Language:
    """Create a sample language for testing purposes."""
    sample_topic = Topic(
        id="intro",
        title="Introduction",
        description="Getting started with programming",
        content="This is the introduction to programming...",
        examples=[
            Example(
                title="Hello World",
                code='print("Hello, World!")',
                explanation="This prints a greeting to the console"
            )
        ]
    )
    
    return Language(
        id="python",
        name="Python",
        description="Learn Python programming from basics to advanced",
        topics=[sample_topic],
        icon_path="assets/icons/python.svg",
        color_theme="#3776ab"
    )


def validate_content_structure(language: Language) -> List[str]:
    """Validate the structure of language content and return any issues."""
    issues = []
    
    try:
        # Validate language itself
        language.__post_init__()
        
        # Validate all topics
        for topic in language.topics:
            try:
                topic.__post_init__()
                
                # Validate examples
                for example in topic.examples:
                    example.__post_init__()
                
                # Validate exercises
                for exercise in topic.exercises:
                    exercise.__post_init__()
                
                # Validate quiz questions
                for question in topic.quiz_questions:
                    question.__post_init__()
                    
            except ValueError as e:
                issues.append(f"Topic '{topic.title}': {str(e)}")
                
    except ValueError as e:
        issues.append(f"Language '{language.name}': {str(e)}")
    
    return issues