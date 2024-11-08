"""C# tutorial content initialization module."""

from typing import List
from content.models import Language

# Import topic modules
from .basics import create_csharp_basics_content
from .data_types import create_data_types_content
from .control_structure import create_control_structures_content
from .methods import create_methods_and_parameters_content
from .classes import create_classes_content
from .inheritance import create_inheritance_content
from .interfaces import create_inheritance_content
from .collections import create_collections_content
from .linq import create_linq_content
from .file_io import create_file_io_content
from .async_programming import create_async_programming_content
from .windows_forms import create_windows_forms_content


def get_csharp_content() -> Language:
    """Create and return the complete C# tutorial content structure."""
    topics = [
        create_csharp_basics_content(),
        create_data_types_content(),
        create_control_structures_content(),
        create_methods_and_parameters_content(),
        create_classes_content(),
        create_inheritance_content(),
        create_inheritance_content(),
        create_collections_content(),
        create_linq_content(),
        create_file_io_content(),
        create_async_programming_content(),
        create_windows_forms_content()
    ]

    csharp_content = Language(
        name="C#",
        description="""C# (C-Sharp) is a modern, object-oriented programming language 
        developed by Microsoft. It combines the power of C++ with the simplicity of 
        Visual Basic, offering a robust platform for Windows, web, and game development.""",
        topics=topics,
        prerequisites=[
            ".NET SDK installed",
            "Visual Studio or Visual Studio Code",
            "Basic understanding of programming concepts",
            "Windows OS recommended (but not required)"
        ],
        learning_path=[
            "C# Basics",
            "Data Types and Variables",
            "Control Structures",
            "Methods and Parameters",
            "Classes and Objects",
            "Inheritance and Polymorphism",
            "Interfaces and Abstract Classes",
            "Collections and Generics",
            "LINQ",
            "File I/O and Exception Handling",
            "Async Programming",
            "Windows Forms/WPF"
        ],
        resources=[
            {
                "name": "Official C# Documentation",
                "url": "https://docs.microsoft.com/en-us/dotnet/csharp/"
            },
            {
                "name": "Official .NET Documentation",
                "url": "https://docs.microsoft.com/en-us/dotnet/"
            },
            {
                "name": "C# Corner",
                "url": "https://www.c-sharpcorner.com/"
            },
            {
                "name": "Unity Learn - C# Programming",
                "url": "https://learn.unity.com/course/intermediate-programming"
            }
        ]
    )

    return csharp_content


def get_topic_dependencies(topic_name: str) -> List[str]:
    """Get the prerequisite topics for a given topic."""
    dependencies = {
        "Control Structures": ["C# Basics", "Data Types and Variables"],
        "Methods and Parameters": ["Control Structures"],
        "Classes and Objects": ["Methods and Parameters"],
        "Inheritance and Polymorphism": ["Classes and Objects"],
        "Interfaces and Abstract Classes": ["Inheritance and Polymorphism"],
        "Collections and Generics": ["Interfaces and Abstract Classes"],
        "LINQ": ["Collections and Generics"],
        "File I/O and Exception Handling": ["LINQ"],
        "Async Programming": ["File I/O and Exception Handling"],
        "Windows Forms/WPF": ["Async Programming"]
    }

    if topic_name not in dependencies and topic_name != "C# Basics":
        raise ValueError(f"Topic '{topic_name}' not found")

    return dependencies.get(topic_name, [])


# Version information
__version__ = "1.0.0"
__author__ = "Aryan Yadav"
__email__ = "support@tutorialagent.com"
