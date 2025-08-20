"""Python control flow tutorial content."""

from content.legacy_models import Topic, Exercise
from content.models import Example


def create() -> Topic:
    """Create and return Python control flow tutorial content."""
    return Topic(
        title="Control Flow",
        description="Learn about Python's control flow statements including if conditions, loops, and more.",
        content="""
        <h1>Control Flow in Python</h1>
        <p>Control flow is the order in which individual statements, instructions, or function calls are executed.</p>

        <h2>Conditional Statements</h2>
        <p>Python uses if, elif, and else statements for conditional execution.</p>
        """,
        examples=[
            Example(
                title="If Statements",
                code="""# Basic if-else statement
age = 18
if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")

# Multiple conditions using elif
score = 85
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: D")""",
                explanation="This example demonstrates how to use if, elif, and else statements to make decisions in your code."
            ),
            Example(
                title="For Loops",
                code="""# Basic for loop with a list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"I like {fruit}")

# Using range
for i in range(5):
    print(f"Count: {i}")

# Nested loops
for i in range(3):
    for j in range(2):
        print(f"i: {i}, j: {j}")""",
                explanation="This example shows different ways to use for loops in Python, including iterating over lists and using the range function."
            ),
            Example(
                title="While Loops",
                code="""# Basic while loop
count = 0
while count < 5:
    print(f"Count is {count}")
    count += 1

# While loop with break
number = 0
while True:
    if number >= 5:
        break
    print(f"Number is {number}")
    number += 1""",
                explanation="This example demonstrates while loops and how to use the break statement to exit a loop."
            )
        ],
        exercises=[
            Exercise(
                title="Number Classifier",
                description="Create a program that classifies numbers as positive, negative, or zero.",
                starter_code="""def classify_number(num):
    # Write your code here to classify the number
    pass

# Test your function
numbers = [5, -3, 0, 10, -8]
for num in numbers:
    classify_number(num)""",
                solution="""def classify_number(num):
    if num > 0:
        print(f"{num} is positive")
    elif num < 0:
        print(f"{num} is negative")
    else:
        print(f"{num} is zero")

# Test your function
numbers = [5, -3, 0, 10, -8]
for num in numbers:
    classify_number(num)""",
                difficulty="Beginner",
                hints=[
                    "Use if-elif-else statements",
                    "Compare the number with 0",
                    "Don't forget to handle the case when the number is exactly 0"
                ]
            ),
            Exercise(
                title="Sum of Even Numbers",
                description="Write a program that calculates the sum of even numbers from 1 to n.",
                starter_code="""def sum_even_numbers(n):
    # Write your code here to sum even numbers
    pass

# Test your function
print(sum_even_numbers(10))  # Should print the sum of even numbers from 1 to 10""",
                solution="""def sum_even_numbers(n):
    total = 0
    for num in range(1, n + 1):
        if num % 2 == 0:
            total += num
    return total

# Test your function
print(sum_even_numbers(10))  # Prints: 30 (2 + 4 + 6 + 8 + 10)""",
                difficulty="Beginner",
                hints=[
                    "Use a for loop with range",
                    "Use the modulo operator (%) to check if a number is even",
                    "Keep a running total of the even numbers"
                ]
            )
        ],
        best_practices=[
            "Keep your conditions simple and readable",
            "Use meaningful variable names in loops",
            "Avoid deep nesting of control structures",
            "Consider using guard clauses",
            "Use appropriate loop types for different scenarios",
            "Remember to handle edge cases in your conditions"
        ]
    )