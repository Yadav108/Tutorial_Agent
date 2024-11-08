from content.models import Topic, Example, Exercise

def create_control_structures_content() -> Topic:
    """Create and return Control Structures tutorial content."""
    return Topic(
        title="Control Structures",
        description="Learn about control flow in C#, including if statements, loops, and switch cases.",
        content="""
        <h1>Control Structures in C#</h1>
        <p>Control structures manage the flow of execution in a program. C# provides several types of control structures,
        including conditional statements and loops.</p>

        <h2>If-Else Statements</h2>
        <p>If-else statements allow the program to make decisions based on conditions.</p>

        <h2>Switch Statements</h2>
        <p>Switch statements provide an efficient way to handle multiple conditions based on a single variable.</p>

        <h2>Loops</h2>
        <p>Loops allow repetitive tasks to be performed with less code. C# supports <code>for</code>, <code>while</code>, 
        and <code>do-while</code> loops.</p>
        """,
        examples=[
            Example(
                title="If-Else Example",
                code="""
                int age = 20;

                if (age >= 18)
                {
                    Console.WriteLine("You are an adult.");
                }
                else
                {
                    Console.WriteLine("You are a minor.");
                }
                """,
                explanation="The program checks if the age is 18 or more to determine adulthood."
            ),
            Example(
                title="Switch Case Example",
                code="""
                int day = 3;

                switch (day)
                {
                    case 1:
                        Console.WriteLine("Monday");
                        break;
                    case 2:
                        Console.WriteLine("Tuesday");
                        break;
                    case 3:
                        Console.WriteLine("Wednesday");
                        break;
                    default:
                        Console.WriteLine("Other day");
                        break;
                }
                """,
                explanation="This example prints the day of the week based on the value of the 'day' variable."
            ),
            Example(
                title="For Loop Example",
                code="""
                for (int i = 0; i < 5; i++)
                {
                    Console.WriteLine("Count: " + i);
                }
                """,
                explanation="A for loop that repeats five times, incrementing 'i' from 0 to 4."
            )
        ],
        exercises=[
            Exercise(
                title="Even or Odd",
                description="Create a program that checks if a given number is even or odd.",
                starter_code="""
                int number = 0;

                // Check if the number is even or odd
                """,
                solution="""
                int number = 4;

                if (number % 2 == 0)
                {
                    Console.WriteLine("Even");
                }
                else
                {
                    Console.WriteLine("Odd");
                }
                """,
                difficulty="Beginner",
                hints=[
                    "Use the modulus operator (%) to determine if the number is divisible by 2.",
                    "An even number has no remainder when divided by 2."
                ]
            ),
            Exercise(
                title="Simple Calculator",
                description="Write a simple calculator using if-else or switch-case to perform basic arithmetic operations.",
                starter_code="""
                char operation = '+';
                int num1 = 5, num2 = 3;

                // Add code to perform the operation and display the result
                """,
                solution="""
                char operation = '+';
                int num1 = 5, num2 = 3;

                switch (operation)
                {
                    case '+':
                        Console.WriteLine(num1 + num2);
                        break;
                    case '-':
                        Console.WriteLine(num1 - num2);
                        break;
                    case '*':
                        Console.WriteLine(num1 * num2);
                        break;
                    case '/':
                        Console.WriteLine(num1 / num2);
                        break;
                    default:
                        Console.WriteLine("Invalid operation");
                        break;
                }
                """,
                difficulty="Intermediate",
                hints=[
                    "Use a switch-case statement to handle different operations.",
                    "Handle division by zero if applicable."
                ]
            )
        ],
        best_practices=[
            "Use if-else statements for simple conditions.",
            "Use switch statements when comparing the same variable against multiple values.",
            "Prefer for-loops for counting-based iterations.",
            "Use while-loops when the number of iterations is not known in advance."
        ]
    )
