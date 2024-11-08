from content.models import Topic, Example, Exercise

def create_javascript_basics_content() -> Topic:
    """Create and return JavaScript Basics tutorial content."""
    return Topic(
        title="JavaScript Basics",
        description="Learn the fundamentals of JavaScript, including variables, data types, functions, and control structures.",
        content="""
        <h1>JavaScript Basics</h1>
        <p>JavaScript is a versatile programming language essential for web development. In this module, we'll cover the basic concepts to get started with JavaScript programming.</p>

        <h2>Variables and Data Types</h2>
        <p>JavaScript variables are used to store data values. The <code>let</code>, <code>const</code>, and <code>var</code> keywords are used to declare variables.</p>

        <h2>Operators</h2>
        <p>Operators are used to perform operations on variables and values. Common types include arithmetic, assignment, comparison, and logical operators.</p>

        <h2>Control Structures</h2>
        <p>JavaScript provides control structures like <code>if</code> statements, loops, and switch statements to control the flow of execution in a program.</p>

        <h2>Functions</h2>
        <p>Functions allow you to reuse code. They are defined using the <code>function</code> keyword, or as arrow functions, and can take parameters to receive input values.</p>
        """,
        examples=[
            Example(
                title="Declaring Variables and Data Types",
                code="""
let age = 25;        // Number
const name = "John"; // String
let isStudent = true; // Boolean
let score = null;    // Null
let person = {name: "Alice", age: 30}; // Object

console.log(age, name, isStudent, score, person);
                """,
                explanation="This example demonstrates variable declaration and different data types in JavaScript: numbers, strings, booleans, null, and objects."
            ),
            Example(
                title="Basic Arithmetic Operations",
                code="""
let x = 10;
let y = 5;
console.log("Addition:", x + y);
console.log("Subtraction:", x - y);
console.log("Multiplication:", x * y);
console.log("Division:", x / y);
console.log("Modulus:", x % y);
                """,
                explanation="This example shows how to perform arithmetic operations using JavaScript's built-in operators."
            ),
            Example(
                title="Using If-Else Conditions",
                code="""
let age = 18;

if (age >= 18) {
    console.log("You are an adult.");
} else {
    console.log("You are a minor.");
}
                """,
                explanation="This example demonstrates a basic if-else statement to check if a person is an adult or a minor."
            ),
            Example(
                title="Creating and Using Functions",
                code="""
function greet(name) {
    return "Hello, " + name + "!";
}

console.log(greet("Alice"));
                """,
                explanation="This example defines a function that takes a name as a parameter and returns a greeting message."
            )
        ],
        exercises=[
            Exercise(
                title="Basic Calculator",
                description="Create a function that takes two numbers and an operator (+, -, *, /) as arguments and returns the result of the operation.",
                starter_code="""function calculate(num1, num2, operator) {
    // Implement the calculator logic here
}

// Test the function
console.log(calculate(10, 5, '+')); // Should print 15
console.log(calculate(10, 5, '-')); // Should print 5
""",
                solution="""function calculate(num1, num2, operator) {
    switch(operator) {
        case '+':
            return num1 + num2;
        case '-':
            return num1 - num2;
        case '*':
            return num1 * num2;
        case '/':
            return num1 / num2;
        default:
            return "Invalid operator";
    }
}

console.log(calculate(10, 5, '+')); // 15
console.log(calculate(10, 5, '-')); // 5
console.log(calculate(10, 5, '*')); // 50
console.log(calculate(10, 5, '/')); // 2
""",
                difficulty="Beginner",
                hints=[
                    "Use a switch statement to handle different operators.",
                    "Make sure to handle the default case for invalid operators.",
                    "Perform the corresponding calculation for each operator."
                ]
            ),
            Exercise(
                title="Even or Odd Checker",
                description="Write a function that takes a number as input and checks if it is even or odd. The function should return 'Even' or 'Odd' based on the input.",
                starter_code="""function checkEvenOrOdd(number) {
    // Add your code here
}

// Test the function
console.log(checkEvenOrOdd(10)); // Should print 'Even'
console.log(checkEvenOrOdd(7));  // Should print 'Odd'
""",
                solution="""function checkEvenOrOdd(number) {
    return number % 2 === 0 ? "Even" : "Odd";
}

console.log(checkEvenOrOdd(10)); // 'Even'
console.log(checkEvenOrOdd(7));  // 'Odd'
""",
                difficulty="Beginner",
                hints=[
                    "Use the modulus operator (%) to determine if a number is even or odd.",
                    "Remember: a number is even if it has no remainder when divided by 2."
                ]
            )
        ],
        best_practices=[
            "Use <code>const</code> for variables that won't change and <code>let</code> for variables that may change.",
            "Follow naming conventions for variables, using camelCase for readability.",
            "Always end your statements with semicolons to avoid unexpected errors.",
            "Use functions to encapsulate reusable code, especially for repetitive tasks.",
            "Prefer === over == for comparison to avoid type coercion issues.",
            "Test your code frequently to catch errors early in the development process."
        ]
    )
