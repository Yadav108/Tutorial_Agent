from content.models import Exercise


def get_control_flow_exercises() -> list[Exercise]:
    """Return a list of exercises for the Control Flow topic."""

    exercises = [
        Exercise(
            title="Temperature Converter",
            description="""Create a function that converts temperatures between Celsius and Fahrenheit.
            Requirements:
            1. Accept a temperature value and unit ('C' or 'F')
            2. Convert to the other unit
            3. Return the converted value rounded to 1 decimal place

            Examples:
            convert_temperature(32, 'F') should return 0.0 (Celsius)
            convert_temperature(0, 'C') should return 32.0 (Fahrenheit)""",
            starter_code="""def convert_temperature(temp, unit):
    # Your code here
    pass""",
            solution="""def convert_temperature(temp, unit):
    if unit.upper() == 'C':
        return round((temp * 9/5) + 32, 1)
    elif unit.upper() == 'F':
        return round((temp - 32) * 5/9, 1)
    else:
        raise ValueError("Unit must be 'C' or 'F')""",
            hints=[
                "Use if/elif to handle different units",
                "Remember the conversion formulas:\n  °F = (°C × 9/5) + 32\n  °C = (°F - 32) × 5/9",
                "Use the round() function to format the result"
            ],
            test_cases=[
                {"input": (32, 'F'), "expected": 0.0},
                {"input": (0, 'C'), "expected": 32.0},
                {"input": (100, 'C'), "expected": 212.0},
                {"input": (-40, 'F'), "expected": -40.0}
            ],
            difficulty="Beginner"
        ),

        Exercise(
            title="Number Classifier",
            description="""Create a function that classifies a number based on multiple criteria.
            Requirements:
            1. If the number is divisible by both 3 and 5, return "FizzBuzz"
            2. If the number is divisible by 3, return "Fizz"
            3. If the number is divisible by 5, return "Buzz"
            4. Otherwise, return the number as a string

            Examples:
            classify_number(15) should return "FizzBuzz"
            classify_number(9) should return "Fizz"
            classify_number(10) should return "Buzz"
            classify_number(7) should return "7\"""",
            starter_code="""def classify_number(num):
    # Your code here
    pass""",
            solution="""def classify_number(num):
    if num % 3 == 0 and num % 5 == 0:
        return "FizzBuzz"
    elif num % 3 == 0:
        return "Fizz"
    elif num % 5 == 0:
        return "Buzz"
    else:
        return str(num)""",
            hints=[
                "Use the modulo operator (%) to check divisibility",
                "Check the most specific condition first (divisible by both)",
                "Remember to convert the number to string in the default case"
            ],
            test_cases=[
                {"input": (15,), "expected": "FizzBuzz"},
                {"input": (9,), "expected": "Fizz"},
                {"input": (10,), "expected": "Buzz"},
                {"input": (7,), "expected": "7"}
            ],
            difficulty="Beginner"
        ),

        Exercise(
            title="Pattern Printer",
            description="""Create a function that prints a triangle pattern of asterisks.
            Requirements:
            1. Accept a positive integer n as input
            2. Print n rows forming a right triangle
            3. Each row should have increasing number of asterisks

            Example for n=4:
            *
            **
            ***
            ****""",
            starter_code="""def print_triangle(n):
    # Your code here
    pass""",
            solution="""def print_triangle(n):
    for i in range(1, n + 1):
        print('*' * i)""",
            hints=[
                "Use a for loop to iterate through rows",
                "Each row number corresponds to the number of asterisks",
                "String multiplication (*) can repeat characters"
            ],
            test_cases=[
                {"input": (3,), "expected": "*\n**\n***"},
                {"input": (1,), "expected": "*"},
                {"input": (5,), "expected": "*\n**\n***\n****\n*****"}
            ],
            difficulty="Beginner"
        ),

        Exercise(
            title="Command Processor",
            description="""Create a function that processes commands using match/case.
            Requirements:
            1. Accept a command string
            2. Process different commands using match/case
            3. Support the following commands:
               - "sum x y": Add two numbers
               - "diff x y": Subtract y from x
               - "quit": Return "Goodbye!"
               - Any other input: Return "Invalid command"

            Examples:
            process_command("sum 5 3") should return "8"
            process_command("diff 10 4") should return "6"
            process_command("quit") should return "Goodbye!"
            process_command("hello") should return "Invalid command\"""",
            starter_code="""def process_command(cmd):
    # Your code here (requires Python 3.10+)
    pass""",
            solution="""def process_command(cmd):
    match cmd.split():
        case ["sum", x, y]:
            return str(float(x) + float(y))
        case ["diff", x, y]:
            return str(float(x) - float(y))
        case ["quit"]:
            return "Goodbye!"
        case _:
            return "Invalid command\"""",
            hints=[
                "Use match/case statement (Python 3.10+)",
                "Split the command string to process arguments",
                "Convert string numbers to float for calculations",
                "Include a catch-all case with _"
            ],
            test_cases=[
                {"input": ("sum 5 3",), "expected": "8.0"},
                {"input": ("diff 10 4",), "expected": "6.0"},
                {"input": ("quit",), "expected": "Goodbye!"},
                {"input": ("hello",), "expected": "Invalid command"}
            ],
            difficulty="Intermediate"
        )
    ]

    return exercises