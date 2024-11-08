from content.models import Topic, Example, Exercise

def create_advanced_concepts_content() -> Topic:
    """Create and return Python advanced concepts tutorial content."""
    return Topic(
        title="Advanced Concepts",
        description="Dive into advanced Python concepts, including decorators, generators, context managers, and metaclasses.",
        content="""
        <h1>Advanced Python Concepts</h1>
        <p>This module explores advanced Python concepts that enhance code reusability, readability, and efficiency. Topics include decorators, generators, context managers, and metaclasses.</p>

        <h2>Decorators</h2>
        <p>Decorators are a powerful feature that allows you to modify the behavior of a function or class. They are commonly used for logging, access control, and more.</p>

        <h2>Generators</h2>
        <p>Generators allow you to iterate over a sequence of values without storing them in memory. They are useful for handling large datasets and creating efficient code.</p>

        <h2>Context Managers</h2>
        <p>Context managers ensure that resources are properly managed. The <code>with</code> statement is commonly used to simplify resource management, such as file handling and network connections.</p>

        <h2>Metaclasses</h2>
        <p>Metaclasses are a way to customize class creation. They are an advanced concept that allows you to define how classes behave and can be used to implement patterns like singletons.</p>
        """,
        examples=[
            Example(
                title="Using Decorators for Logging",
                code="""
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function '{func.__name__}' with arguments {args} and {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function '{func.__name__}' returned {result}")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

# Test the decorated function
add(5, 3)
                """,
                explanation="This example demonstrates a decorator that logs function calls and their arguments, making it useful for debugging and monitoring."
            ),
            Example(
                title="Creating a Generator for Fibonacci Sequence",
                code="""
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Using the generator
fib = fibonacci_generator()
for _ in range(10):
    print(next(fib))
                """,
                explanation="This example shows a generator for the Fibonacci sequence, which produces each value on demand without storing the entire sequence in memory."
            ),
            Example(
                title="Context Manager for File Handling",
                code="""
class FileHandler:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

# Using the custom context manager
with FileHandler('sample.txt', 'w') as file:
    file.write("Hello, world!")
                """,
                explanation="This example demonstrates a custom context manager that safely opens and closes a file, even if an error occurs during file operations."
            ),
            Example(
                title="Using Metaclasses for Singleton Pattern",
                code="""
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class SingletonClass(metaclass=SingletonMeta):
    pass

# Testing Singleton behavior
s1 = SingletonClass()
s2 = SingletonClass()
print(s1 is s2)  # Output: True, both references point to the same instance
                """,
                explanation="This example demonstrates how to create a singleton class using a metaclass. Singleton classes restrict instantiation to one object, useful in scenarios where only one instance is required."
            )
        ],
        exercises=[
            Exercise(
                title="Create a Decorator for Timing Execution",
                description="Write a decorator that measures the execution time of a function and prints it. Use the decorator on a function that performs basic mathematical calculations.",
                starter_code="""import time

def timing_decorator(func):
    # Define the wrapper function to measure time
    pass

# Test function
@timing_decorator
def sample_calculation():
    # Perform some calculations
    pass
sample_calculation()""",
                solution="""import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds to execute")
        return result
    return wrapper

@timing_decorator
def sample_calculation():
    sum([i ** 2 for i in range(100000)])

sample_calculation()""",
                difficulty="Advanced",
                hints=[
                    "Use time.time() to get the current time.",
                    "Calculate elapsed time by subtracting start time from end time.",
                    "Print the elapsed time after function execution."
                ]
            ),
            Exercise(
                title="Create a Custom Context Manager",
                description="Implement a context manager that temporarily changes the current working directory to a given path and then restores the original path upon exit.",
                starter_code="""import os

class DirectoryChanger:
    def __init__(self, new_path):
        self.new_path = new_path
        # Store the current directory

    def __enter__(self):
        # Change to the new directory
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        # Restore the original directory
        pass

# Test the context manager
with DirectoryChanger('/some/path'):
    # Code that runs in the new directory
    pass""",
                solution="""import os

class DirectoryChanger:
    def __init__(self, new_path):
        self.new_path = new_path
        self.original_path = os.getcwd()

    def __enter__(self):
        os.chdir(self.new_path)
        return self.new_path

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.original_path)

# Test the context manager
try:
    with DirectoryChanger('/some/path'):
        print("Inside new directory:", os.getcwd())
    print("Back to original directory:", os.getcwd())
except FileNotFoundError:
    print("Directory does not exist.")
""",
                difficulty="Advanced",
                hints=[
                    "Use os.getcwd() to get the current directory.",
                    "Use os.chdir() to change directories.",
                    "Remember to restore the original directory in the __exit__ method."
                ]
            )
        ],
        best_practices=[
            "Use decorators for code reuse, especially in logging, authentication, and caching.",
            "Opt for generators for memory-efficient iteration over large datasets.",
            "Use context managers to handle resource management and prevent resource leaks.",
            "Metaclasses should be used sparingly, as they add complexity. Only use them for advanced object-oriented patterns.",
            "Test advanced features thoroughly to ensure they behave as expected.",
            "Avoid excessive use of advanced features in simple codebases, as they may reduce readability.",
            "Ensure your team understands these features if you plan to use them extensively in shared projects."
        ]
    )
