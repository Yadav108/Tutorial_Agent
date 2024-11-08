from content.models import Topic, Example, Exercise


def create_testing_and_debugging_content() -> Topic:
    """Create and return Python testing and debugging tutorial content."""
    return Topic(
        title="Testing and Debugging",
        description="Learn the fundamentals of testing and debugging in Python, including unit tests and common debugging techniques.",
        content="""
        <h1>Testing and Debugging in Python</h1>
        <p>Testing and debugging are essential practices for developing reliable and maintainable software. Python provides built-in modules like <code>unittest</code> for creating test cases and several tools for debugging code.</p>

        <h2>Introduction to Unit Testing with unittest</h2>
        <p>The <code>unittest</code> module provides a way to create automated tests for Python functions and classes to ensure that they behave as expected:</p>
        <code>python -m unittest my_test_file.py</code>

        <h2>Basic Debugging Techniques</h2>
        <p>Debugging involves identifying and resolving errors or unexpected behaviors in code. Techniques like using print statements, assertions, and the <code>pdb</code> debugger can help troubleshoot issues.</p>
        """,
        examples=[
            Example(
                title="Creating a Unit Test with unittest",
                code="""
import unittest

# Function to be tested
def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(3, 4), 7)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

    def test_add_mixed_numbers(self):
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()
                """,
                explanation="This example demonstrates writing unit tests for an addition function. The tests check for expected results when adding positive, negative, and mixed numbers."
            ),
            Example(
                title="Debugging with print Statements and pdb",
                code="""
# A simple function with an error
def divide(a, b):
    return a / b

# Debugging using print statements
def safe_divide(a, b):
    print(f"Attempting to divide {a} by {b}")
    if b == 0:
        print("Cannot divide by zero!")
        return None
    return divide(a, b)

# Using pdb for step-by-step debugging
import pdb; pdb.set_trace()
result = safe_divide(10, 0)
print("Result:", result)
                """,
                explanation="This example shows debugging with print statements and Python's built-in debugger, pdb. It checks for division by zero and uses pdb to pause execution for inspection."
            )
        ],
        exercises=[
            Exercise(
                title="Write Unit Tests for String Manipulation",
                description="Create unit tests for a function that reverses strings and removes whitespace. Ensure it handles normal and empty strings, as well as strings with only whitespace.",
                starter_code="""import unittest

# Function to be tested
def clean_and_reverse(string):
    # Implement function logic here
    pass

class TestStringManipulation(unittest.TestCase):
    # Write test methods for clean_and_reverse()
    pass

if __name__ == '__main__':
    unittest.main()""",
                solution="""import unittest

# Function to be tested
def clean_and_reverse(string):
    return ''.join(string.split())[::-1]

class TestStringManipulation(unittest.TestCase):
    def test_normal_string(self):
        self.assertEqual(clean_and_reverse("hello world"), "dlrowolleh")

    def test_empty_string(self):
        self.assertEqual(clean_and_reverse(""), "")

    def test_whitespace_string(self):
        self.assertEqual(clean_and_reverse("   "), "")

if __name__ == '__main__':
    unittest.main()""",
                difficulty="Intermediate",
                hints=[
                    "Use split() to remove whitespace and join() to combine characters.",
                    "Use [::-1] to reverse a string.",
                    "Test for different string inputs, including edge cases like empty strings."
                ]
            ),
            Exercise(
                title="Debug a Function with pdb",
                description="Use pdb to debug a function that calculates the factorial of a number, but it contains a logic error causing incorrect results.",
                starter_code="""import pdb

def factorial(n):
    # Incorrect logic here
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1) - 1  # Logic error

pdb.set_trace()  # Add breakpoints to inspect the variables
print(factorial(5))""",
                solution="""import pdb

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)  # Corrected logic

pdb.set_trace()
print(factorial(5))""",
                difficulty="Intermediate",
                hints=[
                    "Use pdb commands like step (s), next (n), and print to check variable values.",
                    "Check for common off-by-one errors in recursive functions.",
                    "Ensure the function correctly calculates factorial for different input values."
                ]
            )
        ],
        best_practices=[
            "Write tests to cover both typical and edge cases.",
            "Use descriptive test names and group related tests in a test class.",
            "Utilize assertions in testing to verify expected outcomes.",
            "Leverage the pdb module or other debugging tools to locate and resolve issues.",
            "Use logging over print statements in production code for better control over debug information.",
            "Isolate code changes and re-run tests to verify that changes do not introduce new errors.",
            "Practice 'test-driven development' (TDD) to catch issues early in the coding process."
        ]
    )
