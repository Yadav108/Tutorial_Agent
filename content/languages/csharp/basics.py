"""C# basics tutorial content."""

from content.models import Topic, Example, Exercise


def create_csharp_basics_content() -> Topic:
    """Create and return C# basics tutorial content."""
    return Topic(
        title="C# Basics",
        description="Learn the fundamental concepts of C# programming, including basic syntax, variables, and input/output operations.",
        content="""
        <h1>Introduction to C#</h1>
        <p>C# is a modern, object-oriented programming language developed by Microsoft. 
        Let's start with the basic concepts that form the foundation of C# programming.</p>

        <h2>Your First C# Program</h2>
        <p>Every C# program starts with a basic structure. Here's a simple "Hello, World!" program:</p>
        """,
        examples=[
            Example(
                title="Hello World Program",
                code="""
                using System;

                namespace MyFirstProgram
                {
                    class Program
                    {
                        static void Main(string[] args)
                        {
                            Console.WriteLine("Hello, World!");
                        }
                    }
                }
                """,
                explanation="""This is a basic C# program that prints 'Hello, World!' to the console.
                Let's break down its components:
                - 'using System': Imports the System namespace
                - 'namespace': Groups related code
                - 'class Program': Contains the program's code
                - 'static void Main': The entry point of the program
                """
            ),
            Example(
                title="Working with Variables",
                code="""
                using System;

                class Program
                {
                    static void Main()
                    {
                        // Declaring variables
                        string name = "John";
                        int age = 25;
                        double height = 1.75;

                        // String interpolation
                        Console.WriteLine($"Name: {name}");
                        Console.WriteLine($"Age: {age}");
                        Console.WriteLine($"Height: {height}m");
                    }
                }
                """,
                explanation="This example shows how to declare variables of different types and use string interpolation to display their values."
            )
        ],
        exercises=[
            Exercise(
                title="Create a Simple Program",
                description="""Create a program that asks for the user's name and age, 
                then displays a personalized greeting with the user's age in months.
                The program should:
                1. Prompt for and read the user's name
                2. Prompt for and read the user's age
                3. Calculate the age in months
                4. Display a greeting with both pieces of information""",
                starter_code="""
                using System;

                class Program
                {
                    static void Main()
                    {
                        // Declare variables for name and age
                        string name;
                        int age;

                        // Ask for user's name
                        Console.Write("Enter your name: ");

                        // Read the name from console

                        // Ask for user's age
                        Console.Write("Enter your age: ");

                        // Read the age and convert to integer

                        // Calculate age in months

                        // Display personalized greeting using string interpolation

                    }
                }
                """,
                solution="""
                using System;

                class Program
                {
                    static void Main()
                    {
                        // Declare variables for name and age
                        string name;
                        int age;

                        // Ask for user's name
                        Console.Write("Enter your name: ");
                        name = Console.ReadLine();

                        // Ask for user's age
                        Console.Write("Enter your age: ");
                        age = Convert.ToInt32(Console.ReadLine());

                        // Calculate age in months
                        int ageInMonths = age * 12;

                        // Display personalized greeting
                        Console.WriteLine($"Hello, {name}! You are {age} years old ({ageInMonths} months).");
                    }
                }
                """,
                difficulty="Beginner",
                hints=[
                    "Use Console.ReadLine() to get user input",
                    "Remember to convert the age input to an integer using Convert.ToInt32()",
                    "To calculate months, multiply years by 12",
                    "Use string interpolation ($\"\") for the output message"
                ]
            ),
            Exercise(
                title="Basic Calculations",
                description="""Create a program that calculates the area and perimeter of a rectangle.
                The program should:
                1. Ask for the length and width
                2. Calculate both the area and perimeter
                3. Display the results with two decimal places""",
                starter_code="""
                using System;

                class Program
                {
                    static void Main()
                    {
                        // Declare variables for length and width
                        double length, width;

                        // Get length from user
                        Console.Write("Enter rectangle length: ");

                        // Get width from user
                        Console.Write("Enter rectangle width: ");

                        // Calculate area and perimeter

                        // Display results

                    }
                }
                """,
                solution="""
                using System;

                class Program
                {
                    static void Main()
                    {
                        // Declare variables for length and width
                        double length, width;

                        // Get length from user
                        Console.Write("Enter rectangle length: ");
                        length = Convert.ToDouble(Console.ReadLine());

                        // Get width from user
                        Console.Write("Enter rectangle width: ");
                        width = Convert.ToDouble(Console.ReadLine());

                        // Calculate area and perimeter
                        double area = length * width;
                        double perimeter = 2 * (length + width);

                        // Display results
                        Console.WriteLine($"Area: {area:F2} square units");
                        Console.WriteLine($"Perimeter: {perimeter:F2} units");
                    }
                }
                """,
                difficulty="Beginner",
                hints=[
                    "Use Convert.ToDouble() to convert string input to double",
                    "Area formula: length × width",
                    "Perimeter formula: 2 × (length + width)",
                    "Use :F2 format specifier for two decimal places"
                ]
            )
        ],
        best_practices=[
            "Always use appropriate data types for variables",
            "Use meaningful variable names",
            "Use string interpolation instead of string concatenation",
            "Include appropriate comments in your code",
            "Follow C# naming conventions",
            "Always handle user input appropriately",
            "Use Console.WriteLine() for output with newline",
            "Use Console.Write() when you don't want a newline"
        ]
    )