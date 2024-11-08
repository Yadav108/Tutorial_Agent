from content.models import Topic, Example, Exercise

def create_javascript_functions_scope_content() -> Topic:
    """Create and return JavaScript Functions and Scope tutorial content."""
    return Topic(
        title="Functions and Scope",
        description="Learn about defining functions, parameters, and the concept of scope in JavaScript.",
        content="""
        <h1>Functions and Scope in JavaScript</h1>
        <p>Functions in JavaScript are blocks of code designed to perform a particular task. They allow you to reuse code and create modular applications.</p>

        <h2>Defining Functions</h2>
        <p>JavaScript functions can be defined using the <code>function</code> keyword, or with arrow function syntax for a shorter syntax. Functions can accept parameters and return values.</p>

        <h2>Function Parameters and Arguments</h2>
        <p>Parameters are the variables listed in the function definition, while arguments are the actual values passed to the function.</p>

        <h2>Scope</h2>
        <p>Scope determines the accessibility of variables in JavaScript. There are three main types of scope: global scope, function scope, and block scope.</p>

        <ul>
            <li><strong>Global Scope:</strong> Variables declared outside any function or block are globally scoped.</li>
            <li><strong>Function Scope:</strong> Variables declared within a function are only accessible within that function.</li>
            <li><strong>Block Scope:</strong> Variables declared with <code>let</code> or <code>const</code> within a block (e.g., inside an <code>if</code> or <code>for</code> loop) are block-scoped.</li>
        </ul>
        """,
        examples=[
            Example(
                title="Defining a Function",
                code="""
function greet(name) {
    return "Hello, " + name + "!";
}

console.log(greet("Alice")); // Output: Hello, Alice!
                """,
                explanation="This example demonstrates a simple function definition with one parameter. The function takes a name as an argument and returns a greeting message."
            ),
            Example(
                title="Arrow Function",
                code="""
const add = (a, b) => a + b;

console.log(add(5, 3)); // Output: 8
                """,
                explanation="This example shows an arrow function that takes two parameters and returns their sum. Arrow functions are a shorter syntax for writing functions."
            ),
            Example(
                title="Global and Local Scope",
                code="""
let globalVar = "I am global";

function showScope() {
    let localVar = "I am local";
    console.log(globalVar); // Accesses the global variable
    console.log(localVar);  // Accesses the local variable
}

showScope();
// console.log(localVar); // Uncaught ReferenceError: localVar is not defined
                """,
                explanation="This example shows global and local scope. 'globalVar' is accessible everywhere, but 'localVar' is only accessible within the function where it is declared."
            ),
            Example(
                title="Block Scope",
                code="""
if (true) {
    let blockScoped = "I am block-scoped";
    var functionScoped = "I am function-scoped";
}

console.log(functionScoped); // Output: I am function-scoped
// console.log(blockScoped); // Uncaught ReferenceError: blockScoped is not defined
                """,
                explanation="This example shows the difference between <code>let</code> (block scope) and <code>var</code> (function scope). The variable <code>blockScoped</code> is only accessible within the block where it is declared."
            )
        ],
        exercises=[
            Exercise(
                title="Area Calculator",
                description="Write a function that calculates the area of a rectangle, given its width and height as parameters.",
                starter_code="""function calculateArea(width, height) {
    // Implement the function to calculate area
}

// Test the function
console.log(calculateArea(5, 10)); // Should print 50
""",
                solution="""function calculateArea(width, height) {
    return width * height;
}

console.log(calculateArea(5, 10)); // 50
""",
                difficulty="Beginner",
                hints=[
                    "Use multiplication to calculate the area.",
                    "Ensure the function returns the area rather than printing it directly."
                ]
            ),
            Exercise(
                title="Scope Test",
                description="Write a function that defines a local variable and a global variable, and print both within the function and outside the function. Observe the differences.",
                starter_code="""let globalVariable = "I'm global";

function scopeTest() {
    let localVariable = "I'm local";
    // Print both variables here
}

// Call scopeTest
scopeTest();

// Try printing both variables here to observe differences
""",
                solution="""let globalVariable = "I'm global";

function scopeTest() {
    let localVariable = "I'm local";
    console.log(globalVariable); // Accessible within the function
    console.log(localVariable);  // Accessible within the function
}

scopeTest();
console.log(globalVariable);      // Accessible outside the function
// console.log(localVariable);    // Uncaught ReferenceError: localVariable is not defined
""",
                difficulty="Beginner",
                hints=[
                    "Define a variable outside the function to observe global scope.",
                    "Define a variable inside the function to observe function scope.",
                    "Try printing both variables inside and outside the function to understand scope."
                ]
            )
        ],
        best_practices=[
            "Use <code>const</code> and <code>let</code> for variables to control scope and prevent unintended side effects.",
            "Prefer function expressions or arrow functions for shorter syntax and clear code structure.",
            "Avoid declaring global variables whenever possible to prevent accidental overwrites.",
            "Use clear, descriptive names for functions and parameters.",
            "Always return a value from a function unless explicitly designed not to.",
            "Use block scoping (<code>let</code> or <code>const</code>) to prevent accidental use of variables outside intended contexts."
        ]
    )
