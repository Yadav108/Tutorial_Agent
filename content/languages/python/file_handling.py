"""Python file handling tutorial content."""

from content.legacy_models import Topic, Exercise
from content.models import Example


def create() -> Topic:
    """Create and return Python file handling tutorial content."""
    return Topic(
        title="File Handling",
        description="Learn how to read from and write to files in Python.",
        content="""
        <h1>File Handling in Python</h1>
        <p>File handling is an important part of any programming language. Python makes it easy to work with files.</p>

        <h2>Opening and Reading Files</h2>
        <p>Python provides built-in functions and methods for working with files:</p>
        """,
        examples=[
            Example(
                title="Reading a Text File",
                code="""# Reading an entire file
with open('sample.txt', 'r') as file:
    content = file.read()
    print("File contents:")
    print(content)

# Reading line by line
with open('sample.txt', 'r') as file:
    for line in file:
        print(f"Line: {line.strip()}")""",
                explanation="This example shows how to open and read a file both all at once and line by line. The 'with' statement ensures the file is properly closed after use."
            ),
            Example(
                title="Writing to Files",
                code="""# Writing to a new file
with open('output.txt', 'w') as file:
    file.write("Hello, World!\\n")
    file.write("This is a new line.")

# Appending to a file
with open('output.txt', 'a') as file:
    file.write("\\nAppending a new line.")

# Writing multiple lines
lines = ['Line 1', 'Line 2', 'Line 3']
with open('output.txt', 'w') as file:
    file.writelines(f"{line}\\n" for line in lines)""",
                explanation="This example demonstrates different ways to write to files. The 'w' mode creates a new file or overwrites existing content, while 'a' mode appends to the existing content."
            )
        ],
        exercises=[
            Exercise(
                title="File Reader",
                description="Create a program that reads a text file and counts the number of lines, words, and characters.",
                starter_code="""def analyze_file(filename):
    # Initialize counters
    lines = 0
    words = 0
    chars = 0

    # Add your code here to count lines, words, and characters

    return lines, words, chars

# Test the function
try:
    lines, words, chars = analyze_file('sample.txt')
    print(f"Lines: {lines}")
    print(f"Words: {words}")
    print(f"Characters: {chars}")
except FileNotFoundError:
    print("File not found!")""",
                solution="""def analyze_file(filename):
    lines = 0
    words = 0
    chars = 0

    try:
        with open(filename, 'r') as file:
            for line in file:
                lines += 1
                chars += len(line)
                words += len(line.split())

        return lines, words, chars
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return 0, 0, 0
    except Exception as e:
        print(f"Error reading file: {e}")
        return 0, 0, 0

# Test the function
lines, words, chars = analyze_file('sample.txt')
print(f"Number of lines: {lines}")
print(f"Number of words: {words}")
print(f"Number of characters: {chars}")""",
                difficulty="Intermediate",
                hints=[
                    "Use a with statement to handle file operations",
                    "Split lines into words using split()",
                    "Remember to handle potential errors",
                    "Don't forget to count newline characters"
                ]
            ),
            Exercise(
                title="CSV File Handler",
                description="Create a program that reads a CSV file containing student grades and calculates their average scores.",
                starter_code="""def process_grades(filename):
    # Expected CSV format:
    # Name,Math,Science,English
    # John,85,92,78
    # Mary,90,88,95

    # Add your code here to:
    # 1. Read the CSV file
    # 2. Calculate average for each student
    # 3. Return a dictionary of students and their averages
    pass

# Test the function
try:
    student_averages = process_grades('grades.csv')
    for student, average in student_averages.items():
        print(f"{student}'s average: {average:.2f}")
except FileNotFoundError:
    print("Grades file not found!")""",
                solution="""def process_grades(filename):
    student_averages = {}

    try:
        with open(filename, 'r') as file:
            # Skip header line
            headers = file.readline()

            # Process each student's grades
            for line in file:
                # Remove whitespace and split by comma
                data = line.strip().split(',')
                if len(data) >= 4:  # Name + 3 grades
                    name = data[0]
                    # Convert grades to float and calculate average
                    grades = [float(grade) for grade in data[1:4]]
                    average = sum(grades) / len(grades)
                    student_averages[name] = average

        return student_averages

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}
    except Exception as e:
        print(f"Error processing file: {e}")
        return {}

# Test the function
try:
    student_averages = process_grades('grades.csv')
    if student_averages:
        print("Student Averages:")
        for student, average in student_averages.items():
            print(f"{student}'s average: {average:.2f}")
    else:
        print("No grades to process.")
except Exception as e:
    print(f"Error: {e}")""",
                difficulty="Intermediate",
                hints=[
                    "Remember to skip the header line",
                    "Convert string grades to float for calculations",
                    "Use try-except to handle potential errors",
                    "Check for valid data format in each line"
                ]
            )
        ],
        best_practices=[
            "Always use the 'with' statement to handle file operations",
            "Close files properly after using them",
            "Use appropriate file modes ('r', 'w', 'a')",
            "Handle file-related exceptions properly",
            "Check if file exists before trying to read it",
            "Use meaningful variable names for file handles",
            "Add error handling for different file operations"
        ]
    )