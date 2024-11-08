"""Python functions tutorial content."""

from content.models import Topic, Example, Exercise


def create_functions_modules_content() -> Topic:
    """Create and return Python functions tutorial content."""
    return Topic(
        title="Functions and Modules",
        description="Learn how to create and use functions to organize your code.",
        content="""
        <h1>Functions in Python</h1>
        <p>Functions are reusable blocks of code that perform specific tasks and help organize your programs.</p>

        <h2>Defining Functions</h2>
        <p>Functions are defined using the 'def' keyword, followed by the function name and parameters:</p>
        """,
        examples=[
            Example(
                title="Basic Function Definition",
                code="""def greet(name):
    print(f"Hello, {name}!")

# Using the function
greet("Alice")
greet("Bob")""",
                explanation="This shows how to define a simple function that takes a name parameter and prints a greeting. The function can be reused with different names."
            ),
            Example(
                title="Functions with Return Values",
                code="""def calculate_area(length, width):
    area = length * width
    return area

# Using the function
room_area = calculate_area(4, 5)
print(f"The room area is {room_area} square meters")

# Direct use in print
print(f"Another room area is {calculate_area(3, 6)} square meters")""",
                explanation="This example demonstrates how functions can calculate and return values. The returned value can be stored in a variable or used directly in expressions."
            )
        ],
        exercises=[
            Exercise(
                title="Temperature Converter",
                description="Create a function that converts temperatures from Celsius to Fahrenheit using the formula: (C × 9/5) + 32.",
                starter_code="""def celsius_to_fahrenheit(celsius):
    # Write your code here to convert celsius to fahrenheit
    pass

# Test cases
print(celsius_to_fahrenheit(0))    # Should print 32.0
print(celsius_to_fahrenheit(100))  # Should print 212.0
print(celsius_to_fahrenheit(25))   # Should print 77.0""",
                solution="""def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

# Test cases
print(f"0°C = {celsius_to_fahrenheit(0)}°F")
print(f"100°C = {celsius_to_fahrenheit(100)}°F")
print(f"25°C = {celsius_to_fahrenheit(25)}°F")""",
                difficulty="Beginner",
                hints=[
                    "Remember the formula: (C × 9/5) + 32 = F",
                    "Use parentheses to ensure correct calculation order",
                    "Return the calculated value from the function",
                    "Test with known values like 0°C = 32°F"
                ]
            ),
            Exercise(
                title="Simple Calculator",
                description="Create a function that takes two numbers and an operation (+, -, *, /) and returns the result of the calculation.",
                starter_code="""def calculator(num1, num2, operation):
    # Write your code here to perform the calculation
    pass

# Test your calculator
print(calculator(10, 5, '+'))  # Should print 15
print(calculator(10, 5, '-'))  # Should print 5
print(calculator(10, 5, '*'))  # Should print 50
print(calculator(10, 5, '/'))  # Should print 2.0""",
                solution="""def calculator(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero"
    else:
        return "Error: Invalid operation"

# Test the calculator
print(f"10 + 5 = {calculator(10, 5, '+')}")
print(f"10 - 5 = {calculator(10, 5, '-')}")
print(f"10 * 5 = {calculator(10, 5, '*')}")
print(f"10 / 5 = {calculator(10, 5, '/')}")
print(f"10 / 0 = {calculator(10, 0, '/')}")""",
                difficulty="Beginner",
                hints=[
                    "Use if/elif statements to handle different operations",
                    "Remember to handle division by zero",
                    "Return the result of each calculation",
                    "Test all operations and edge cases"
                ]
            )
        ],
        best_practices=[
            "Use clear and descriptive function names",
            "Add docstrings to document your functions",
            "Keep functions focused on a single task",
            "Handle errors and edge cases",
            "Return values consistently",
            "Use parameters to make functions flexible",
            "Test functions with different inputs"
        ]
    )