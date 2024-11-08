"""Python data structures tutorial content."""

from content.models import Topic, Example, Exercise


def create_data_structures_content() -> Topic:
    """Create and return Python data structures tutorial content."""
    return Topic(
        title="Data Structures",
        description="Learn about Python's built-in data structures like lists, tuples, dictionaries, and sets.",
        content="""
        <h1>Python Data Structures</h1>
        <p>Python provides several built-in data structures to store and organize data efficiently.</p>

        <h2>Lists</h2>
        <p>Lists are ordered, mutable sequences of elements:</p>
        """,
        examples=[
            Example(
                title="Working with Lists",
                code="""# Creating and using lists
fruits = ["apple", "banana", "orange"]
print(f"Original list: {fruits}")

# Adding elements
fruits.append("grape")
print(f"After append: {fruits}")

# Accessing elements
print(f"First fruit: {fruits[0]}")
print(f"Last fruit: {fruits[-1]}")

# Slicing
print(f"First two fruits: {fruits[0:2]}")""",
                explanation="This example shows basic list operations including creation, adding elements, accessing items, and slicing."
            ),
            Example(
                title="Dictionaries",
                code="""# Creating a dictionary
student = {
    "name": "John Doe",
    "age": 20,
    "grades": [85, 90, 88]
}

# Accessing values
print(f"Student name: {student['name']}")
print(f"Student age: {student['age']}")

# Adding new key-value pair
student['city'] = 'New York'
print(f"Updated student info: {student}")

# Getting keys and values
print(f"Dictionary keys: {list(student.keys())}")
print(f"Dictionary values: {list(student.values())}")""",
                explanation="This example demonstrates dictionary operations including creation, accessing values, adding new items, and getting keys/values."
            )
        ],
        exercises=[
            Exercise(
                title="List Operations",
                description="Create a program that performs various operations on a list of numbers.",
                starter_code="""numbers = [1, 2, 3, 4, 5]

# 1. Add the number 6 to the end of the list
# 2. Insert the number 0 at the beginning
# 3. Calculate the sum of all numbers
# 4. Find the maximum number
# 5. Print all numbers greater than 3""",
                solution="""numbers = [1, 2, 3, 4, 5]

# 1. Add the number 6 to the end
numbers.append(6)
print(f"After append: {numbers}")

# 2. Insert 0 at the beginning
numbers.insert(0, 0)
print(f"After insert: {numbers}")

# 3. Calculate sum
total = sum(numbers)
print(f"Sum of numbers: {total}")

# 4. Find maximum
maximum = max(numbers)
print(f"Maximum number: {maximum}")

# 5. Print numbers greater than 3
greater_than_three = [num for num in numbers if num > 3]
print(f"Numbers greater than 3: {greater_than_three}")""",
                difficulty="Beginner",
                hints=[
                    "Use append() to add to the end of a list",
                    "Use insert(0, value) to add at the beginning",
                    "Python has built-in sum() and max() functions",
                    "Use a list comprehension or loop for filtering"
                ]
            ),
            Exercise(
                title="Dictionary Management",
                description="Create a program to manage a contact list using a dictionary.",
                starter_code="""# Create a dictionary to store contacts
contacts = {}

# Add these contacts:
# - John Doe: 123-456-7890
# - Jane Smith: 987-654-3210

# Write code to:
# 1. Add the contacts
# 2. Print all contacts
# 3. Update John's number to: 555-555-5555
# 4. Print John's updated number""",
                solution="""# Create a dictionary to store contacts
contacts = {}

# 1. Add contacts
contacts["John Doe"] = "123-456-7890"
contacts["Jane Smith"] = "987-654-3210"

# 2. Print all contacts
print("All contacts:")
for name, number in contacts.items():
    print(f"{name}: {number}")

# 3. Update John's number
contacts["John Doe"] = "555-555-5555"

# 4. Print John's updated number
print(f"John's new number: {contacts['John Doe']}")""",
                difficulty="Beginner",
                hints=[
                    "Use dictionary[key] = value to add or update entries",
                    "Use .items() to iterate over key-value pairs",
                    "Remember that dictionary keys are case-sensitive",
                    "You can update values using the same syntax as adding them"
                ]
            )
        ],
        best_practices=[
            "Choose the appropriate data structure for your needs",
            "Use lists for ordered collections of items",
            "Use dictionaries when you need key-value pairs",
            "Remember that lists are mutable (changeable)",
            "Keep dictionary keys simple and meaningful",
            "Use list comprehensions for readable list operations",
            "Consider using tuples for immutable sequences"
        ]
    )