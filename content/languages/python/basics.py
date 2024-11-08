# content/languages/python/basics.py

from content.models import Topic, Example, Exercise

def create_python_basics_content() -> Topic:
    """Create and return Python basics tutorial content."""
    return Topic(
        title="Python Basics",
        description="Learn the fundamental concepts of Python programming.",
        content="""
        <h1>Introduction to Python</h1>
        <p>Python is a high-level, interpreted programming language known for its simplicity and readability.</p>

        <h2>Your First Python Program</h2>
        <p>Let's start with the traditional "Hello, World!" program:</p>
        """,
        examples=[
            Example(
                title="Hello World",
                code='print("Hello, World!")',
                explanation="This simple program outputs 'Hello, World!' to the console. The print() function is used to display text."
            ),
            Example(
                title="Variables and Data Types",
                code="""# String variable
name = "Deebya"
print(f"Hello, {name}!")

# Numeric variables
age = 25
height = 1.75

print(f"Age: {age} years")
print(f"Height: {height} meters")""",
                explanation="This example shows how to work with variables of different types (string, integer, and float) and use f-strings for formatting."
            )
        ],
        exercises=[
            Exercise(
                title="Basic Print Statement",
                description="Create a program that prints your name and age.",
                starter_code="""# Create variables for your name and age
name = "Your Name"
age = 0

# Print a message using these variables
""",
                solution="""# Create variables for your name and age
name = "John Doe"
age = 25

# Print a message using these variables
print(f"My name is {name} and I am {age} years old.")""",
                difficulty="Beginner",
                hints=[
                    "Use variables to store your name and age",
                    "Use an f-string to combine text and variables",
                    "Remember to use quotes around string values"
                ]
            ),
            Exercise(
                title="Basic Calculations",
                description="Create a program that calculates and prints the sum and product of two numbers.",
                starter_code="""# Create two number variables
num1 = 10
num2 = 5

# Calculate and print their sum and product
""",
                solution="""# Create two number variables
num1 = 10
num2 = 5

# Calculate and print their sum and product
sum_result = num1 + num2
product_result = num1 * num2

print(f"Sum of {num1} and {num2} is: {sum_result}")
print(f"Product of {num1} and {num2} is: {product_result}")""",
                difficulty="Beginner",
                hints=[
                    "Use the + operator for addition",
                    "Use the * operator for multiplication",
                    "Store results in variables before printing"
                ]
            )
        ],
        best_practices=[
            "Use meaningful variable names",
            "Add comments to explain your code",
            "Use f-strings for string formatting",
            "Follow Python's PEP 8 style guide",
            "Keep your code simple and readable"
        ]
    )