"""Python basics tutorial content - test version."""

from content.legacy_models import Topic, Exercise
from content.models import Example


def create() -> Topic:
    """Create and return Python basics tutorial content."""
    return Topic(
        title="Python Basics",
        description="Learn the fundamentals of Python programming",
        content="""
        <h1>Python Basics</h1>
        <p>Python is a powerful, easy-to-learn programming language.</p>

        <h2>Variables and Data Types</h2>
        <p>Python has several built-in data types including strings, numbers, and lists.</p>
        """,
        examples=[
            Example(
                title="Hello World",
                code='print("Hello, World!")',
                explanation="This prints a greeting message to the console."
            ),
            Example(
                title="Variables",
                code='''name = "Python"
age = 30
print(f"Language: {name}, Age: {age}")''',
                explanation="Variables store data values. Python determines the data type automatically."
            )
        ],
        exercises=[
            Exercise(
                title="First Program",
                description="Write a program that prints your name",
                starter_code="# Write your code here\n",
                solution='print("Your Name Here")',
                difficulty="Beginner",
                hints=["Use the print() function", "Put your name in quotes"]
            )
        ],
        best_practices=[
            "Use descriptive variable names",
            "Follow PEP 8 style guidelines",
            "Add comments to explain complex code"
        ]
    )