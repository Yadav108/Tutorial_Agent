"""Python error handling tutorial content."""

from content.models import Topic, Example, Exercise


def create_error_handling_content() -> Topic:
    """Create and return Python error handling tutorial content."""
    return Topic(
        title="Error Handling",
        description="Learn how to handle errors and exceptions in Python using try-except blocks.",
        content="""
        <h1>Error Handling in Python</h1>
        <p>Error handling is crucial for writing robust programs that can handle unexpected situations gracefully.</p>

        <h2>Try-Except Blocks</h2>
        <p>Python uses try-except blocks to handle errors and exceptions:</p>
        """,
        examples=[
            Example(
                title="Basic Exception Handling",
                code="""try:
    # Attempt to convert string to integer
    number = int("abc")
    print(number)
except ValueError:
    print("Error: Could not convert string to integer")

# Another example with multiple operations
try:
    numbers = [1, 2, 3]
    print(numbers[5])  # This will raise an IndexError
except IndexError:
    print("Error: Index is out of range")""",
                explanation="This example shows basic exception handling using try-except blocks. It catches specific exceptions (ValueError, IndexError) and provides appropriate error messages."
            ),
            Example(
                title="Multiple Exception Types",
                code="""def divide_numbers(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None
    except TypeError:
        print("Error: Please provide numbers only!")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Test the function with different scenarios
print(divide_numbers(10, 2))    # Works fine
print(divide_numbers(10, 0))    # Division by zero
print(divide_numbers(10, "2"))  # Type error""",
                explanation="This example demonstrates handling multiple types of exceptions. It catches specific exceptions first (ZeroDivisionError, TypeError) and then uses a general Exception catch-all for unexpected errors."
            )
        ],
        exercises=[
            Exercise(
                title="File Reader with Error Handling",
                description="Create a function that safely reads a file and handles various potential errors.",
                starter_code="""def safe_read_file(filename):
    # Implement a function that:
    # 1. Attempts to read a file
    # 2. Handles FileNotFoundError
    # 3. Handles PermissionError
    # 4. Handles other potential errors
    # 5. Returns the file contents or appropriate error message
    pass

# Test cases
print(safe_read_file("existing.txt"))
print(safe_read_file("nonexistent.txt"))""",
                solution="""def safe_read_file(filename):
    try:
        with open(filename, 'r') as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        return f"Error: The file '{filename}' does not exist"
    except PermissionError:
        return f"Error: Permission denied to read '{filename}'"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Test cases
print("Testing with existing file:")
print(safe_read_file("existing.txt"))
print("\\nTesting with nonexistent file:")
print(safe_read_file("nonexistent.txt"))""",
                difficulty="Beginner",
                hints=[
                    "Use a try-except block to catch different exceptions",
                    "Handle specific exceptions before general ones",
                    "Always use with statement for file operations",
                    "Return meaningful error messages"
                ]
            ),
            Exercise(
                title="Input Validator",
                description="Create a function that validates user input for age and handles various input errors.",
                starter_code="""def get_valid_age():
    # Implement a function that:
    # 1. Prompts user for their age
    # 2. Validates the input is a positive integer
    # 3. Ensures age is between 0 and 120
    # 4. Handles ValueError and other exceptions
    # 5. Returns the validated age or None if invalid
    pass

# Test the function
age = get_valid_age()
if age is not None:
    print(f"Valid age entered: {age}")""",
                solution="""def get_valid_age():
    try:
        age = int(input("Please enter your age: "))

        if age < 0:
            raise ValueError("Age cannot be negative")
        if age > 120:
            raise ValueError("Age cannot be greater than 120")

        return age

    except ValueError as ve:
        if str(ve).startswith("Age"):
            print(f"Error: {ve}")
        else:
            print("Error: Please enter a valid number")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Test the function
age = get_valid_age()
if age is not None:
    print(f"Valid age entered: {age}")""",
                difficulty="Intermediate",
                hints=[
                    "Use int() to convert string input to integer",
                    "Check for valid age range",
                    "Handle both conversion and validation errors",
                    "Use custom error messages for different cases"
                ]
            )
        ],
        best_practices=[
            "Always use specific exception types when possible",
            "Handle exceptions at the appropriate level",
            "Don't use bare 'except' clauses",
            "Clean up resources using try-finally or with statements",
            "Provide meaningful error messages",
            "Don't suppress exceptions without good reason",
            "Log errors appropriately in production code"
        ]
    )