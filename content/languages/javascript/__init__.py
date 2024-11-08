# content/languages/javascript/__init__.py

from content.models import Language, Resource, DifficultyLevel, Topic, Example, Exercise
from typing import List, Dict

# Import topic modules
from .basics import create_javascript_basics_content
from .functions import create_javascript_functions_scope_content
from .object_and_array import create_objects_and_arrays_content
from .DOM_Manipulation import create_dom_manipulation_content
from .Events import create_events_and_event_handling_content
from .Asynchronous import create_asynchronous_javascript_content
from .ES6_Features import create_es6_plus_features_content
from .Error_Handling import create_error_handling_content
from .working_with_API import create_working_with_api_content
from .Modern_devolpment import create_modern_development_content

def get_javascript_content() -> Language:
    """Create and return the complete JavaScript tutorial content structure."""
    topics = [
        create_javascript_basics_content(),
        create_javascript_functions_scope_content(),
        create_objects_and_arrays_content(),
        create_dom_manipulation_content(),
        create_events_and_event_handling_content(),
        create_asynchronous_javascript_content(),
        create_es6_plus_features_content(),
        create_error_handling_content(),
        create_working_with_api_content(),
        create_modern_development_content()
    ]

    javascript_content = Language(
        id="javascript",
        name="JavaScript",
        description="""JavaScript is a versatile programming language primarily 
        used for web development. It allows you to create interactive websites,
        web applications, server-side applications, and even mobile and desktop apps.
        Its ease of learning and extensive ecosystem make it an excellent choice
        for both beginners and experienced developers.""",
        topics=topics,
        prerequisites=[
            "Basic understanding of HTML and CSS",
            "Text editor or IDE installed (VS Code recommended)",
            "Modern web browser with developer tools",
            "Node.js installed (for modern JavaScript development)"
        ],
        learning_path=[
            "JavaScript Basics",
            "Functions and Scope",
            "Objects and Arrays",
            "DOM Manipulation",
            "Events and Event Handling",
            "Asynchronous JavaScript",
            "ES6+ Features",
            "Error Handling",
            "Working with APIs",
            "Modern JavaScript Development"
        ],
        resources=[
            Resource(
                title="MDN JavaScript Guide",
                url="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
                type="documentation",
                description="Comprehensive JavaScript documentation by Mozilla",
                free=True
            ),
            Resource(
                title="JavaScript.info",
                url="https://javascript.info/",
                type="tutorial",
                description="Modern JavaScript Tutorial with interactive examples",
                free=True
            ),
            Resource(
                title="Node.js Documentation",
                url="https://nodejs.org/docs/latest/api/",
                type="documentation",
                description="Official Node.js documentation for server-side JavaScript",
                free=True
            ),
            Resource(
                title="Chrome DevTools Documentation",
                url="https://developers.google.com/web/tools/chrome-devtools",
                type="tool",
                description="Official guide for Chrome's built-in debugging tools",
                free=True
            )
        ],
        difficulty=DifficultyLevel.BEGINNER,
        icon="javascript-icon.svg",
        color="#F7DF1E",  # JavaScript yellow
        estimated_hours=45,
        category="web"
    )

    return javascript_content

def get_topic_dependencies(topic_name: str) -> List[str]:
    """Get the prerequisite topics for a given topic."""
    dependencies = {
        "Functions and Scope": ["JavaScript Basics"],
        "Objects and Arrays": ["Functions and Scope"],
        "DOM Manipulation": ["Objects and Arrays"],
        "Events and Event Handling": ["DOM Manipulation"],
        "Asynchronous JavaScript": ["Events and Event Handling"],
        "ES6+ Features": ["Functions and Scope", "Objects and Arrays"],
        "Error Handling": ["Asynchronous JavaScript"],
        "Working with APIs": ["Asynchronous JavaScript", "Error Handling"],
        "Modern JavaScript Development": [
            "ES6+ Features",
            "Working with APIs",
            "Error Handling"
        ]
    }

    if topic_name not in dependencies and topic_name != "JavaScript Basics":
        raise ValueError(f"Topic '{topic_name}' not found in the curriculum")

    return dependencies.get(topic_name, [])

def get_recommended_tools() -> List[Dict[str, str]]:
    """Get recommended development tools for JavaScript."""
    return [
        {
            "name": "Visual Studio Code",
            "type": "IDE",
            "url": "https://code.visualstudio.com/",
            "description": "Popular code editor with excellent JavaScript support",
            "recommended_extensions": [
                "ESLint",
                "Prettier",
                "JavaScript (ES6) code snippets",
                "Live Server"
            ]
        },
        {
            "name": "Node.js",
            "type": "Runtime",
            "url": "https://nodejs.org/",
            "description": "JavaScript runtime for server-side development",
            "installation_guide": "https://nodejs.org/en/download/"
        },
        {
            "name": "Chrome DevTools",
            "type": "Debug Tool",
            "url": "https://developers.google.com/web/tools/chrome-devtools",
            "description": "Built-in browser tools for debugging JavaScript",
            "key_features": [
                "Console debugging",
                "Network monitoring",
                "Performance profiling",
                "DOM inspection"
            ]
        },
        {
            "name": "Git",
            "type": "Version Control",
            "url": "https://git-scm.com/",
            "description": "Version control system for tracking code changes",
            "tutorials": [
                "https://www.atlassian.com/git/tutorials",
                "https://git-scm.com/book/en/v2"
            ]
        }
    ]

def get_project_ideas() -> List[Dict[str, str]]:
    """Get project ideas for practicing JavaScript."""
    return [
        {
            "title": "Interactive Todo List",
            "difficulty": DifficultyLevel.BEGINNER.value,
            "topics": ["DOM Manipulation", "Events", "Local Storage"],
            "description": "Create a todo list with CRUD operations and persistence",
            "learning_objectives": [
                "DOM manipulation",
                "Event handling",
                "Local storage usage",
                "Basic CRUD operations"
            ],
            "suggested_features": [
                "Add/Remove todos",
                "Mark as complete",
                "Filter by status",
                "Save to local storage"
            ]
        },
        {
            "title": "Weather Dashboard",
            "difficulty": DifficultyLevel.INTERMEDIATE.value,
            "topics": ["API Integration", "Async/Await", "DOM Updates"],
            "description": "Build a weather app using a weather API and geolocation",
            "learning_objectives": [
                "Working with APIs",
                "Async programming",
                "Geolocation API",
                "Dynamic DOM updates"
            ],
            "suggested_features": [
                "Current weather display",
                "5-day forecast",
                "Location search",
                "Geolocation support"
            ]
        },
        {
            "title": "Real-time Chat Application",
            "difficulty": DifficultyLevel.ADVANCED.value,
            "topics": ["WebSockets", "Events", "Modern JS"],
            "description": "Develop a chat app with real-time messaging capabilities",
            "learning_objectives": [
                "WebSocket implementation",
                "Real-time data handling",
                "User authentication",
                "Modern JS features"
            ],
            "suggested_features": [
                "Real-time messaging",
                "User presence",
                "Message history",
                "Private messaging"
            ]
        }
    ]

# Version information
__version__ = "1.0.0"
__author__ = "Aryan Yadav"
__email__ = "support@tutorialagent.com"