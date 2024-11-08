from content.models import Topic, Example, Exercise


def create_data_types_content() -> Topic:
    """Create and return Data Types tutorial content."""
    return Topic(
        title="Data Types",
        description="Learn about different data types in C#, including integer, floating-point, and boolean types.",
        content="""
        <h1>Data Types in C#</h1>
        <p>C# provides a variety of data types to store different kinds of values. The main categories of data types include 
        integral types, floating-point types, boolean, and more.</p>

        <h2>Integral Types</h2>
        <p>Integral types represent whole numbers. Examples include:</p>
        <ul>
            <li><code>int</code>: a 32-bit signed integer.</li>
            <li><code>long</code>: a 64-bit signed integer.</li>
            <li><code>byte</code>: an 8-bit unsigned integer.</li>
        </ul>

        <h2>Floating-Point Types</h2>
        <p>Floating-point types are used for numbers with fractional parts. Examples include:</p>
        <ul>
            <li><code>float</code>: a 32-bit floating-point number.</li>
            <li><code>double</code>: a 64-bit floating-point number.</li>
        </ul>

        <h2>Other Data Types</h2>
        <ul>
            <li><code>bool</code>: stores <code>true</code> or <code>false</code> values.</li>
            <li><code>char</code>: a single 16-bit Unicode character.</li>
            <li><code>string</code>: represents a sequence of characters.</li>
        </ul>
        """,
        examples=[
            Example(
                title="Declaring and Initializing Variables",
                code="""
                int age = 25;           // Integer type
                double height = 1.75;    // Double type
                bool isStudent = true;   // Boolean type
                char initial = 'A';      // Character type
                string name = "Alice";   // String type

                Console.WriteLine($"Name: {name}, Age: {age}, Height: {height}, Student: {isStudent}");
                """,
                explanation="This example shows how to declare variables of different data types and print them."
            ),
            Example(
                title="Type Casting",
                code="""
                int wholeNumber = 10;
                double decimalNumber = 5.75;

                // Implicit casting: int to double
                double result = wholeNumber + decimalNumber;

                // Explicit casting: double to int
                int truncatedResult = (int)decimalNumber;

                Console.WriteLine("Implicit cast result: " + result);
                Console.WriteLine("Explicit cast result: " + truncatedResult);
                """,
                explanation="This example demonstrates implicit and explicit casting between data types."
            )
        ],
        exercises=[
            Exercise(
                title="Variable Declarations",
                description="Declare variables to store a person's age, height, and marital status, then print them.",
                starter_code="""
                // Declare an integer for age
                // Declare a double for height
                // Declare a boolean for marital status

                // Print all the values
                """,
                solution="""
                int age = 30;
                double height = 1.80;
                bool isMarried = false;

                Console.WriteLine($"Age: {age}, Height: {height}, Married: {isMarried}");
                """,
                difficulty="Beginner",
                hints=[
                    "Use int for age, double for height, and bool for marital status.",
                    "Print values using Console.WriteLine() and string interpolation."
                ]
            ),
            Exercise(
                title="Simple Arithmetic",
                description="Write a program that declares two integers and performs basic arithmetic operations.",
                starter_code="""
                // Declare two integers

                // Perform addition, subtraction, multiplication, and division

                // Print each result
                """,
                solution="""
                int num1 = 15;
                int num2 = 4;

                Console.WriteLine($"Addition: {num1 + num2}");
                Console.WriteLine($"Subtraction: {num1 - num2}");
                Console.WriteLine($"Multiplication: {num1 * num2}");
                Console.WriteLine($"Division: {num1 / num2}");
                """,
                difficulty="Beginner",
                hints=[
                    "Declare variables for the two numbers.",
                    "Use +, -, *, and / operators for arithmetic operations.",
                    "Use Console.WriteLine() to display each result."
                ]
            )
        ],
        best_practices=[
            "Choose the appropriate data type for the value being stored.",
            "Use implicit casting when possible to avoid data loss.",
            "Use explicit casting when converting between incompatible types.",
            "Initialize variables with meaningful values when possible.",
            "Use descriptive variable names that reflect the data they store."
        ]
    )
