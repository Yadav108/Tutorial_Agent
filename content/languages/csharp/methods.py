from content.models import Topic, Example, Exercise

def create_methods_and_parameters_content() -> Topic:
    """Create and return Methods and Parameters tutorial content."""
    return Topic(
        title="Methods and Parameters",
        description="Learn how to create and use methods in C#, including parameter passing and return types.",
        content="""
        <h1>Methods and Parameters in C#</h1>
        <p>Methods allow you to organize your code into reusable blocks. Parameters let you pass values into methods, 
        while return types specify the kind of result the method returns.</p>

        <h2>Defining a Method</h2>
        <p>To define a method, specify its return type, name, and any parameters it takes. Here's an example:</p>

        <h2>Parameter Passing</h2>
        <p>C# supports parameter passing by value (default), by reference (using <code>ref</code>), and output parameters 
        (using <code>out</code>).</p>
        """,
        examples=[
            Example(
                title="Basic Method Example",
                code="""
                int Add(int a, int b)
                {
                    return a + b;
                }

                // Using the method
                int result = Add(5, 3);
                Console.WriteLine("Result: " + result);
                """,
                explanation="This method 'Add' takes two integers as parameters, adds them, and returns the result."
            ),
            Example(
                title="Method with Ref Parameter",
                code="""
                void DoubleValue(ref int number)
                {
                    number = number * 2;
                }

                int value = 10;
                DoubleValue(ref value);
                Console.WriteLine("Doubled Value: " + value);
                """,
                explanation="The 'DoubleValue' method doubles the value of the variable passed to it by reference using 'ref'."
            ),
            Example(
                title="Method with Out Parameter",
                code="""
                bool TryParseNumber(string input, out int result)
                {
                    return int.TryParse(input, out result);
                }

                if (TryParseNumber("123", out int number))
                {
                    Console.WriteLine("Parsed Number: " + number);
                }
                else
                {
                    Console.WriteLine("Invalid input.");
                }
                """,
                explanation="The 'TryParseNumber' method uses 'out' to return a parsed integer from a string input."
            )
        ],
        exercises=[
            Exercise(
                title="Area of a Rectangle",
                description="Create a method that calculates the area of a rectangle given its length and width.",
                starter_code="""
                // Define the method 'CalculateArea' that takes two doubles (length and width) and returns a double.

                // Sample usage:
                // double area = CalculateArea(5.5, 3.2);
                """,
                solution="""
                double CalculateArea(double length, double width)
                {
                    return length * width;
                }

                // Usage example
                double area = CalculateArea(5.5, 3.2);
                Console.WriteLine("Area: " + area);
                """,
                difficulty="Beginner",
                hints=[
                    "The formula for the area of a rectangle is length * width.",
                    "Ensure the method has a 'double' return type."
                ]
            ),
            Exercise(
                title="Temperature Converter",
                description="Create a method that converts Celsius to Fahrenheit.",
                starter_code="""
                // Define the method 'ConvertToFahrenheit' that takes a double (Celsius temperature) 
                // and returns a double (Fahrenheit temperature).

                // Sample usage:
                // double fahrenheit = ConvertToFahrenheit(25);
                """,
                solution="""
                double ConvertToFahrenheit(double celsius)
                {
                    return (celsius * 9 / 5) + 32;
                }

                // Usage example
                double fahrenheit = ConvertToFahrenheit(25);
                Console.WriteLine("Fahrenheit: " + fahrenheit);
                """,
                difficulty="Beginner",
                hints=[
                    "The formula to convert Celsius to Fahrenheit is (C * 9/5) + 32.",
                    "Return the converted value from the method."
                ]
            )
        ],
        best_practices=[
            "Use descriptive names for methods that clearly indicate their purpose.",
            "Use parameters to make methods more flexible and reusable.",
            "Use 'ref' only when necessary to modify the caller's variable.",
            "Use 'out' when a method needs to return multiple values.",
            "Avoid overly complex methods; keep them focused on a single task."
        ]
    )