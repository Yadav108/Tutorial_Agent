# content/languages/python/__init__.py

from content.models import Language, Resource

# Import topic modules
from .basics import create_python_basics_content
from .control_flow import create_control_flow_content
from .functions import create_functions_modules_content
from .data_structure import create_data_structures_content
from .oop import create_object_oriented_programming_content
from .file_handling import create_file_handling_content
from .error_handling import create_error_handling_content
from .Libraries_and_Packages import create_libraries_and_packages_content
from .Testing_and_Debugging import create_testing_and_debugging_content
from .advanced import create_advanced_concepts_content


def get_python_content() -> Language:
    """Create and return the complete Python tutorial content structure."""
    # Create available topics
    topics = [
        create_python_basics_content(),
        create_control_flow_content(),
        create_functions_modules_content(),
        create_data_structures_content(),
        create_object_oriented_programming_content(),
        create_file_handling_content(),
        create_error_handling_content(),
        create_libraries_and_packages_content(),
        create_testing_and_debugging_content(),
        create_advanced_concepts_content(),
    ]

    return Language(
        id="python",  # Added id
        name="Python",
        description="""Python is a high-level, interpreted programming language known for 
        its simplicity and readability. It's perfect for beginners while being powerful 
        enough for professional development.""",
        icon="python.svg",  # Added icon
        color="#3776AB",  # Added color
        topics=topics,
        prerequisites=[
            "Basic computer skills",
            "Understanding of basic math concepts",
            "Text editor or IDE installed",
            "Python 3.x installed on your computer"
        ],
        learning_path=[
            "Python Basics",
            "Control Flow",
            "Functions and Modules",
            "Data Structures",
            "Object-Oriented Programming",
            "File Handling",
            "Error Handling",
            "Libraries and Packages",
            "Testing and Debugging",
            "Advanced Topics"
        ],
        resources=[  # Changed to Resource objects
            Resource(
                title="Official Python Documentation",
                url="https://docs.python.org/3/",
                type="documentation",
                description="Comprehensive Python documentation",
                free=True
            ),
            Resource(
                title="Python Package Index (PyPI)",
                url="https://pypi.org/",
                type="package_repository",
                description="Python package repository",
                free=True
            ),
            Resource(
                title="Real Python Tutorials",
                url="https://realpython.com/",
                type="tutorial",
                description="In-depth Python tutorials and articles",
                free=True
            )
        ]
    )
