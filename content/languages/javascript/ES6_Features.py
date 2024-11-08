from content.models import Topic, Example, Exercise

def create_es6_plus_features_content() -> Topic:
    """Create and return ES6+ JavaScript features tutorial content."""
    return Topic(
        title="ES6+ Features",
        description="Explore the modern features introduced in ES6 and later versions of JavaScript, including arrow functions, destructuring, template literals, and more.",
        content="""
        <h1>ES6+ Features</h1>
        <p>ES6 (ECMAScript 2015) and subsequent updates have brought numerous improvements to JavaScript. These features enhance readability, reduce boilerplate, and make coding in JavaScript more efficient. Let's go over some of the most commonly used ES6+ features.</p>

        <h2>Arrow Functions</h2>
        <p>Arrow functions provide a shorter syntax for writing functions and automatically bind the context of <code>this</code>.</p>

        <h2>Template Literals</h2>
        <p>Template literals allow embedding expressions within strings, making string interpolation easier.</p>

        <h2>Destructuring</h2>
        <p>Destructuring allows you to unpack values from arrays or properties from objects into distinct variables.</p>

        <h2>Spread and Rest Operators</h2>
        <p>The spread operator (...) can expand arrays and objects, while the rest operator (...) can condense multiple elements into a single array.</p>

        <h2>Modules</h2>
        <p>Modules allow you to export and import code between different files, enabling better organization and reuse of code.</p>
        """,
        examples=[
            Example(
                title="Arrow Functions",
                code="""
// Traditional function
function add(a, b) {
    return a + b;
}

// Arrow function
const add = (a, b) => a + b;
console.log(add(2, 3)); // Output: 5
""",
                explanation="The arrow function `add` is a shorter version of a traditional function. For single-expression functions, you can omit the return statement and braces."
            ),
            Example(
                title="Template Literals",
                code="""
// Using traditional string concatenation
const name = 'Alice';
console.log('Hello, ' + name + '!');

// Using template literals
console.log(`Hello, ${name}!`); // Output: Hello, Alice!
""",
                explanation="Template literals use backticks and allow embedding variables directly within strings with `${variable}` syntax."
            ),
            Example(
                title="Destructuring",
                code="""
// Array destructuring
const [a, b] = [10, 20];
console.log(a); // Output: 10

// Object destructuring
const user = { name: 'Alice', age: 25 };
const { name, age } = user;
console.log(name); // Output: Alice
""",
                explanation="Destructuring allows extracting values from arrays or objects and assigning them to variables in a single, concise syntax."
            ),
            Example(
                title="Spread and Rest Operators",
                code="""
// Spread operator with arrays
const arr1 = [1, 2];
const arr2 = [...arr1, 3, 4];
console.log(arr2); // Output: [1, 2, 3, 4]

// Rest operator in function arguments
function sum(...numbers) {
    return numbers.reduce((acc, num) => acc + num, 0);
}
console.log(sum(1, 2, 3, 4)); // Output: 10
""",
                explanation="The spread operator (`...`) expands elements in arrays or objects, while the rest operator (`...`) collects multiple arguments into a single array."
            ),
            Example(
                title="Modules (import/export)",
                code="""
// In math.js
export function add(a, b) {
    return a + b;
}

// In main.js
import { add } from './math.js';
console.log(add(5, 3)); // Output: 8
""",
                explanation="Modules allow you to export functions or variables from one file and import them in another, promoting modular code organization."
            )
        ],
        exercises=[
            Exercise(
                title="Create a Function Using Arrow Syntax",
                description="Rewrite the following function as an arrow function: `function multiply(a, b) { return a * b; }`",
                starter_code="""
// Convert this function to arrow syntax
function multiply(a, b) {
    return a * b;
}

// Call the function with sample values
""",
                solution="""
// Converted arrow function
const multiply = (a, b) => a * b;

// Call the function with sample values
console.log(multiply(3, 4)); // Output: 12
""",
                difficulty="Beginner",
                hints=[
                    "Use `const` to define the arrow function",
                    "For single-expression functions, omit `return` and curly braces"
                ]
            ),
            Exercise(
                title="Use Template Literals",
                description="Create a function `greet` that takes a name and returns a greeting using template literals.",
                starter_code="""
// Define the greet function

// Test the function
""",
                solution="""
// Define the greet function
const greet = (name) => `Hello, ${name}!`;

// Test the function
console.log(greet('Alice')); // Output: Hello, Alice!
""",
                difficulty="Beginner",
                hints=[
                    "Use backticks (`) for the string",
                    "Use `${}` to insert the name variable into the string"
                ]
            ),
            Exercise(
                title="Destructure an Object",
                description="Use object destructuring to extract `name` and `age` from the following `person` object: `{ name: 'Bob', age: 30 }`.",
                starter_code="""
// Use destructuring to extract name and age
const person = { name: 'Bob', age: 30 };

// Log the extracted values
""",
                solution="""
// Use destructuring to extract name and age
const { name, age } = person;

// Log the extracted values
console.log(name); // Output: Bob
console.log(age);  // Output: 30
""",
                difficulty="Beginner",
                hints=[
                    "Use `{}` for object destructuring",
                    "Match the property names with variables"
                ]
            ),
            Exercise(
                title="Combine Arrays Using Spread",
                description="Create an array `combined` by combining `arr1 = [1, 2, 3]` and `arr2 = [4, 5, 6]` using the spread operator.",
                starter_code="""
// Combine arr1 and arr2 using the spread operator
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];

// Log the combined array
""",
                solution="""
// Combine arr1 and arr2 using the spread operator
const combined = [...arr1, ...arr2];

// Log the combined array
console.log(combined); // Output: [1, 2, 3, 4, 5, 6]
""",
                difficulty="Beginner",
                hints=[
                    "Use `[...arr1, ...arr2]` to combine the arrays",
                    "Log the combined array"
                ]
            )
        ],
        best_practices=[
            "Use arrow functions for concise syntax and to avoid `this` binding issues",
            "Utilize template literals for clean and readable string concatenation",
            "Destructure arrays and objects to easily access their values",
            "Use spread and rest operators for flexible function arguments and array manipulation",
            "Organize code into modules to promote reusability and maintainability"
        ]
    )
