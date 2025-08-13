# content/enhanced_models.py

import logging
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Union, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
import re

logger = logging.getLogger('TutorialAgent.Models')


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class DifficultyLevel(Enum):
    """Enumeration for difficulty levels."""
    BEGINNER = "Beginner"
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class ContentType(Enum):
    """Enumeration for content types."""
    TUTORIAL = "tutorial"
    EXAMPLE = "example"
    EXERCISE = "exercise"
    QUIZ = "quiz"
    PROJECT = "project"


class ProgressStatus(Enum):
    """Enumeration for progress status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    REVIEW = "review"


def validate_not_empty(value: str, field_name: str) -> str:
    """Validate that a string is not empty."""
    if not value or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")
    return value.strip()


def validate_code(code: str, language: str = None) -> str:
    """Validate code content."""
    if not code or not code.strip():
        raise ValidationError("Code cannot be empty")

    # Basic syntax validation (can be extended)
    code = code.strip()

    # Check for potential security issues
    dangerous_patterns = [
        r'import\s+os',
        r'import\s+subprocess',
        r'exec\s*\(',
        r'eval\s*\(',
        r'__import__',
        r'open\s*\([^)]*["\'][^"\']*["\'][^)]*["\']w',  # File writing
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            logger.warning(f"Potentially dangerous code pattern detected: {pattern}")
            # Don't raise exception, just log warning for now

    return code


def validate_url(url: str) -> str:
    """Validate URL format."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not url_pattern.match(url):
        raise ValidationError("Invalid URL format")

    return url


@dataclass
class BaseModel:
    """Base model with common functionality."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        self.validate()

    def validate(self):
        """Validate the model. Override in subclasses."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper serialization."""
        result = asdict(self)

        # Convert datetime objects to ISO format
        if isinstance(result.get('created_at'), datetime):
            result['created_at'] = self.created_at.isoformat()
        if isinstance(result.get('updated_at'), datetime):
            result['updated_at'] = self.updated_at.isoformat()

        # Convert enums to values
        for key, value in result.items():
            if isinstance(value, Enum):
                result[key] = value.value

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from dictionary."""
        # Convert datetime strings back to datetime objects
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])

        return cls(**data)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str):
        """Create instance from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)


@dataclass
class Example(BaseModel):
    """Enhanced example model with validation."""
    title: str = ""
    code: str = ""
    explanation: str = ""
    language: str = "python"
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    tags: List[str] = field(default_factory=list)
    expected_output: Optional[str] = None
    execution_time_ms: Optional[int] = None
    memory_usage_kb: Optional[int] = None

    def validate(self):
        """Validate example data."""
        super().validate()

        self.title = validate_not_empty(self.title, "Example title")
        self.code = validate_code(self.code, self.language)
        self.explanation = validate_not_empty(self.explanation, "Example explanation")

        # Validate language
        if not self.language or not self.language.strip():
            raise ValidationError("Language cannot be empty")
        self.language = self.language.lower().strip()

        # Validate tags
        if self.tags:
            self.tags = [tag.strip().lower() for tag in self.tags if tag.strip()]

        # Validate difficulty
        if isinstance(self.difficulty, str):
            try:
                self.difficulty = DifficultyLevel(self.difficulty)
            except ValueError:
                raise ValidationError(f"Invalid difficulty level: {self.difficulty}")

    def get_complexity_score(self) -> int:
        """Calculate complexity score based on code analysis."""
        if not self.code:
            return 0

        score = 0
        lines = self.code.split('\n')

        # Line count factor
        score += len([line for line in lines if line.strip()])

        # Control structures
        control_patterns = [r'\bif\b', r'\bfor\b', r'\bwhile\b', r'\btry\b', r'\bclass\b', r'\bdef\b']
        for pattern in control_patterns:
            score += len(re.findall(pattern, self.code, re.IGNORECASE))

        return score

    def estimate_reading_time(self) -> int:
        """Estimate reading time in seconds."""
        # Average reading speed: 200 words per minute
        word_count = len(self.explanation.split()) if self.explanation else 0
        code_lines = len([line for line in self.code.split('\n') if line.strip()]) if self.code else 0

        # Code takes longer to read
        total_words = word_count + (code_lines * 3)  # Each line of code = 3 words
        reading_time_minutes = total_words / 200

        return max(30, int(reading_time_minutes * 60))  # Minimum 30 seconds


@dataclass
class Exercise(BaseModel):
    """Enhanced exercise model with validation and auto-grading."""
    title: str = ""
    description: str = ""
    instructions: str = ""
    starter_code: str = ""
    solution: str = ""
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    estimated_time_minutes: int = 15
    tags: List[str] = field(default_factory=list)
    hints: List[str] = field(default_factory=list)
    test_cases: List[Dict[str, Any]] = field(default_factory=list)
    max_attempts: int = 5
    points: int = 10
    language: str = "python"

    def validate(self):
        """Validate exercise data."""
        super().validate()

        self.title = validate_not_empty(self.title, "Exercise title")
        self.description = validate_not_empty(self.description, "Exercise description")

        if self.starter_code:
            self.starter_code = validate_code(self.starter_code, self.language)

        if self.solution:
            self.solution = validate_code(self.solution, self.language)

        # Validate difficulty
        if isinstance(self.difficulty, str):
            try:
                self.difficulty = DifficultyLevel(self.difficulty)
            except ValueError:
                raise ValidationError(f"Invalid difficulty level: {self.difficulty}")

        # Validate timing and scoring
        if self.estimated_time_minutes < 1:
            raise ValidationError("Estimated time must be at least 1 minute")

        if self.points < 0:
            raise ValidationError("Points cannot be negative")

        if self.max_attempts < 1:
            raise ValidationError("Max attempts must be at least 1")

        # Validate language
        if not self.language or not self.language.strip():
            raise ValidationError("Language cannot be empty")
        self.language = self.language.lower().strip()

    def add_test_case(self, input_data: Any, expected_output: Any, description: str = ""):
        """Add a test case for automatic grading."""
        test_case = {
            'id': str(uuid.uuid4()),
            'input': input_data,
            'expected_output': expected_output,
            'description': description,
            'weight': 1.0  # Default weight
        }
        self.test_cases.append(test_case)

    def get_difficulty_multiplier(self) -> float:
        """Get point multiplier based on difficulty."""
        multipliers = {
            DifficultyLevel.BEGINNER: 0.8,
            DifficultyLevel.EASY: 1.0,
            DifficultyLevel.MEDIUM: 1.2,
            DifficultyLevel.HARD: 1.5,
            DifficultyLevel.ADVANCED: 2.0,
            DifficultyLevel.EXPERT: 2.5
        }
        return multipliers.get(self.difficulty, 1.0)

    def calculate_max_points(self) -> int:
        """Calculate maximum possible points including difficulty multiplier."""
        return int(self.points * self.get_difficulty_multiplier())


@dataclass
class Topic(BaseModel):
    """Enhanced topic model with comprehensive content management."""
    title: str = ""
    description: str = ""
    content: str = ""
    learning_objectives: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    examples: List[Example] = field(default_factory=list)
    exercises: List[Exercise] = field(default_factory=list)
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    estimated_duration_minutes: int = 30
    tags: List[str] = field(default_factory=list)
    order_index: int = 0
    is_published: bool = True
    best_practices: List[str] = field(default_factory=list)
    common_mistakes: List[str] = field(default_factory=list)
    additional_resources: List[Dict[str, str]] = field(default_factory=list)

    def validate(self):
        """Validate topic data."""
        super().validate()

        self.title = validate_not_empty(self.title, "Topic title")
        self.description = validate_not_empty(self.description, "Topic description")
        self.content = validate_not_empty(self.content, "Topic content")

        # Validate difficulty
        if isinstance(self.difficulty, str):
            try:
                self.difficulty = DifficultyLevel(self.difficulty)
            except ValueError:
                raise ValidationError(f"Invalid difficulty level: {self.difficulty}")

        # Validate duration
        if self.estimated_duration_minutes < 1:
            raise ValidationError("Estimated duration must be at least 1 minute")

        # Validate examples
        for i, example in enumerate(self.examples):
            if not isinstance(example, Example):
                raise ValidationError(f"Example {i} is not a valid Example instance")
            example.validate()

        # Validate exercises
        for i, exercise in enumerate(self.exercises):
            if not isinstance(exercise, Exercise):
                raise ValidationError(f"Exercise {i} is not a valid Exercise instance")
            exercise.validate()

        # Validate additional resources
        for resource in self.additional_resources:
            if 'title' not in resource or 'url' not in resource:
                raise ValidationError("Additional resources must have 'title' and 'url'")
            validate_url(resource['url'])

    def add_example(self, title: str, code: str, explanation: str, **kwargs) -> Example:
        """Add a new example to the topic."""
        example = Example(
            title=title,
            code=code,
            explanation=explanation,
            **kwargs
        )
        self.examples.append(example)
        self.update_timestamp()
        return example

    def add_exercise(self, title: str, description: str, **kwargs) -> Exercise:
        """Add a new exercise to the topic."""
        exercise = Exercise(
            title=title,
            description=description,
            **kwargs
        )
        self.exercises.append(exercise)
        self.update_timestamp()
        return exercise

    def get_total_estimated_time(self) -> int:
        """Get total estimated time including examples and exercises."""
        total_time = self.estimated_duration_minutes

        # Add example reading time
        for example in self.examples:
            total_time += example.estimate_reading_time() // 60  # Convert to minutes

        # Add exercise time
        for exercise in self.exercises:
            total_time += exercise.estimated_time_minutes

        return total_time

    def get_content_stats(self) -> Dict[str, int]:
        """Get statistics about the topic content."""
        return {
            'word_count': len(self.content.split()) if self.content else 0,
            'examples_count': len(self.examples),
            'exercises_count': len(self.exercises),
            'total_estimated_minutes': self.get_total_estimated_time(),
            'learning_objectives_count': len(self.learning_objectives),
            'prerequisites_count': len(self.prerequisites)
        }

    def search_content(self, query: str) -> List[Dict[str, Any]]:
        """Search within topic content."""
        results = []
        query_lower = query.lower()

        # Search in title and description
        if query_lower in self.title.lower():
            results.append({
                'type': 'title',
                'content': self.title,
                'relevance': 10
            })

        if query_lower in self.description.lower():
            results.append({
                'type': 'description',
                'content': self.description,
                'relevance': 8
            })

        # Search in content
        if query_lower in self.content.lower():
            results.append({
                'type': 'content',
                'content': self.content,
                'relevance': 5
            })

        # Search in examples
        for example in self.examples:
            if (query_lower in example.title.lower() or
                    query_lower in example.explanation.lower() or
                    query_lower in example.code.lower()):
                results.append({
                    'type': 'example',
                    'content': example,
                    'relevance': 6
                })

        # Search in exercises
        for exercise in self.exercises:
            if (query_lower in exercise.title.lower() or
                    query_lower in exercise.description.lower()):
                results.append({
                    'type': 'exercise',
                    'content': exercise,
                    'relevance': 6
                })

        return sorted(results, key=lambda x: x['relevance'], reverse=True)


@dataclass
class Language(BaseModel):
    """Enhanced language model with comprehensive metadata."""
    name: str = ""
    description: str = ""
    icon: str = "default.png"
    color: str = "#3498db"
    version: str = "1.0.0"
    topics: List[Topic] = field(default_factory=list)
    learning_path: List[str] = field(default_factory=list)
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    estimated_hours: int = 10
    popularity_score: float = 0.0
    is_active: bool = True
    official_docs_url: Optional[str] = None
    community_links: List[Dict[str, str]] = field(default_factory=list)

    def validate(self):
        """Validate language data."""
        super().validate()

        self.name = validate_not_empty(self.name, "Language name")
        self.description = validate_not_empty(self.description, "Language description")

        # Validate color (hex color)
        if not re.match(r'^#[0-9a-fA-F]{6}$', self.color):
            raise ValidationError("Color must be a valid hex color (e.g., #3498db)")

        # Validate version format
        if not re.match(r'^\d+\.\d+\.\d+$', self.version):
            raise ValidationError("Version must be in format X.Y.Z")

        # Validate difficulty
        if isinstance(self.difficulty, str):
            try:
                self.difficulty = DifficultyLevel(self.difficulty)
            except ValueError:
                raise ValidationError(f"Invalid difficulty level: {self.difficulty}")

        # Validate estimated hours
        if self.estimated_hours < 1:
            raise ValidationError("Estimated hours must be at least 1")

        # Validate popularity score
        if not 0 <= self.popularity_score <= 100:
            raise ValidationError("Popularity score must be between 0 and 100")

        # Validate official docs URL
        if self.official_docs_url:
            validate_url(self.official_docs_url)

        # Validate topics
        for i, topic in enumerate(self.topics):
            if not isinstance(topic, Topic):
                raise ValidationError(f"Topic {i} is not a valid Topic instance")
            topic.validate()

        # Validate community links
        for link in self.community_links:
            if 'title' not in link or 'url' not in link:
                raise ValidationError("Community links must have 'title' and 'url'")
            validate_url(link['url'])

    def add_topic(self, title: str, description: str, content: str, **kwargs) -> Topic:
        """Add a new topic to the language."""
        topic = Topic(
            title=title,
            description=description,
            content=content,
            order_index=len(self.topics),
            **kwargs
        )
        self.topics.append(topic)
        self.update_timestamp()
        return topic

    def get_topic_by_title(self, title: str) -> Optional[Topic]:
        """Get topic by title."""
        for topic in self.topics:
            if topic.title.lower() == title.lower():
                return topic
        return None

    def get_topics_by_difficulty(self, difficulty: DifficultyLevel) -> List[Topic]:
        """Get topics filtered by difficulty."""
        return [topic for topic in self.topics if topic.difficulty == difficulty]

    def get_language_stats(self) -> Dict[str, Any]:
        """Get comprehensive language statistics."""
        if not self.topics:
            return {'total_topics': 0}

        total_examples = sum(len(topic.examples) for topic in self.topics)
        total_exercises = sum(len(topic.exercises) for topic in self.topics)
        total_estimated_time = sum(topic.get_total_estimated_time() for topic in self.topics)

        difficulty_counts = {}
        for difficulty in DifficultyLevel:
            difficulty_counts[difficulty.value] = len(self.get_topics_by_difficulty(difficulty))

        return {
            'total_topics': len(self.topics),
            'total_examples': total_examples,
            'total_exercises': total_exercises,
            'total_estimated_minutes': total_estimated_time,
            'difficulty_distribution': difficulty_counts,
            'average_examples_per_topic': total_examples / len(self.topics),
            'average_exercises_per_topic': total_exercises / len(self.topics),
            'completion_percentage': 0  # To be calculated based on user progress
        }

    def reorder_topics(self, topic_ids: List[str]):
        """Reorder topics by providing list of topic IDs."""
        topic_dict = {topic.id: topic for topic in self.topics}
        reordered_topics = []

        for i, topic_id in enumerate(topic_ids):
            if topic_id in topic_dict:
                topic = topic_dict[topic_id]
                topic.order_index = i
                reordered_topics.append(topic)

        # Add any topics not in the reorder list
        existing_ids = set(topic_ids)
        for topic in self.topics:
            if topic.id not in existing_ids:
                topic.order_index = len(reordered_topics)
                reordered_topics.append(topic)

        self.topics = reordered_topics
        self.update_timestamp()

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search within language content."""
        results = []

        # Search in language name and description
        query_lower = query.lower()
        if query_lower in self.name.lower():
            results.append({
                'type': 'language',
                'content': self.name,
                'relevance': 15
            })

        if query_lower in self.description.lower():
            results.append({
                'type': 'language_description',
                'content': self.description,
                'relevance': 12
            })

        # Search in topics
        for topic in self.topics:
            topic_results = topic.search_content(query)
            for result in topic_results:
                result['topic_id'] = topic.id
                result['topic_title'] = topic.title
                results.append(result)

        return sorted(results, key=lambda x: x['relevance'], reverse=True)


@dataclass
class UserProgress(BaseModel):
    """Enhanced user progress tracking."""
    user_id: str = ""
    language_id: str = ""
    topic_id: str = ""
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    completion_percentage: float = 0.0
    time_spent_minutes: int = 0
    attempts: int = 0
    last_accessed: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_examples: List[str] = field(default_factory=list)
    completed_exercises: List[str] = field(default_factory=list)
    exercise_scores: Dict[str, float] = field(default_factory=dict)
    notes: str = ""
    bookmarked: bool = False

    def validate(self):
        """Validate user progress data."""
        super().validate()

        self.user_id = validate_not_empty(self.user_id, "User ID")
        self.language_id = validate_not_empty(self.language_id, "Language ID")
        self.topic_id = validate_not_empty(self.topic_id, "Topic ID")

        # Validate status
        if isinstance(self.status, str):
            try:
                self.status = ProgressStatus(self.status)
            except ValueError:
                raise ValidationError(f"Invalid progress status: {self.status}")

        # Validate completion percentage
        if not 0 <= self.completion_percentage <= 100:
            raise ValidationError("Completion percentage must be between 0 and 100")

        # Validate time spent
        if self.time_spent_minutes < 0:
            raise ValidationError("Time spent cannot be negative")

        # Validate attempts
        if self.attempts < 0:
            raise ValidationError("Attempts cannot be negative")

    def mark_example_completed(self, example_id: str):
        """Mark an example as completed."""
        if example_id not in self.completed_examples:
            self.completed_examples.append(example_id)
            self.update_progress()

    def mark_exercise_completed(self, exercise_id: str, score: float = 100.0):
        """Mark an exercise as completed with a score."""
        if exercise_id not in self.completed_exercises:
            self.completed_exercises.append(exercise_id)

        self.exercise_scores[exercise_id] = score
        self.update_progress()

    def update_progress(self):
        """Update overall progress based on completed items."""
        # This would be called by the content manager
        # to calculate progress based on completed examples and exercises
        self.last_accessed = datetime.now(timezone.utc)
        self.update_timestamp()

    def get_average_exercise_score(self) -> float:
        """Get average score across all exercises."""
        if not self.exercise_scores:
            return 0.0
        return sum(self.exercise_scores.values()) / len(self.exercise_scores)

    def add_time_spent(self, minutes: int):
        """Add time spent on this topic."""
        self.time_spent_minutes += minutes
        self.last_accessed = datetime.now(timezone.utc)
        self.update_timestamp()


# Helper functions for model management
def create_example_from_dict(data: Dict[str, Any]) -> Example:
    """Create Example instance from dictionary with proper type conversion."""
    if 'difficulty' in data and isinstance(data['difficulty'], str):
        data['difficulty'] = DifficultyLevel(data['difficulty'])
    return Example.from_dict(data)


def create_exercise_from_dict(data: Dict[str, Any]) -> Exercise:
    """Create Exercise instance from dictionary with proper type conversion."""
    if 'difficulty' in data and isinstance(data['difficulty'], str):
        data['difficulty'] = DifficultyLevel(data['difficulty'])
    return Exercise.from_dict(data)


def create_topic_from_dict(data: Dict[str, Any]) -> Topic:
    """Create Topic instance from dictionary with proper type conversion."""
    if 'difficulty' in data and isinstance(data['difficulty'], str):
        data['difficulty'] = DifficultyLevel(data['difficulty'])

    # Convert examples and exercises
    if 'examples' in data:
        data['examples'] = [create_example_from_dict(ex) for ex in data['examples']]

    if 'exercises' in data:
        data['exercises'] = [create_exercise_from_dict(ex) for ex in data['exercises']]

    return Topic.from_dict(data)


def create_language_from_dict(data: Dict[str, Any]) -> Language:
    """Create Language instance from dictionary with proper type conversion."""
    if 'difficulty' in data and isinstance(data['difficulty'], str):
        data['difficulty'] = DifficultyLevel(data['difficulty'])

    # Convert topics
    if 'topics' in data:
        data['topics'] = [create_topic_from_dict(topic) for topic in data['topics']]

    return Language.from_dict(data)