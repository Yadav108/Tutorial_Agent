# content/models.py

from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum

class DifficultyLevel(Enum):
    """Enum for content difficulty levels."""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

@dataclass
class Resource:
    """External learning resource."""
    title: str
    url: str
    type: str = "documentation"  # documentation, tutorial, video, etc.
    description: str = ""
    free: bool = True

@dataclass
class Example:
    """Code example with explanation."""
    title: str
    code: str
    explanation: str = ""

@dataclass
class Exercise:
    """Programming exercise."""
    title: str
    description: str
    starter_code: str
    solution: str
    difficulty: str = "Beginner"
    hints: List[str] = field(default_factory=list)

@dataclass
class Topic:
    """Tutorial topic containing content and exercises."""
    title: str
    description: str
    content: str
    examples: List[Example] = field(default_factory=list)
    exercises: List[Exercise] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

@dataclass
class Language:
    """Programming language course structure."""
    name: str
    description: str
    topics: List[Topic]
    prerequisites: List[str] = field(default_factory=list)
    learning_path: List[str] = field(default_factory=list)
    resources: List[Resource] = field(default_factory=list)
    id: str = ""
    icon: str = ""
    color: str = ""
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    estimated_hours: int = 40
    category: str = ""
    recommended_tools: List[Dict[str, Any]] = field(default_factory=list)
    project_ideas: List[Dict[str, Any]] = field(default_factory=list)

    def get_topic_dependencies(self, topic_name: str) -> List[str]:
        """Get prerequisites for a specific topic."""
        for topic in self.topics:
            if topic.title == topic_name:
                return topic.dependencies
        return []