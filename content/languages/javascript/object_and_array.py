from content.models import Topic, Example, Exercise


def create_objects_and_arrays_content() -> Topic:
    """Create and return JavaScript Objects and Arrays tutorial content."""
    return Topic(
        title="Objects and Arrays",
        description="Learn how to work with objects and arrays in JavaScript, which are essential data structures for organizing and managing data.",
        content="""
        <h1>JavaScript Objects and Arrays</h1>
        <p>Objects and arrays are core data structures in JavaScript. Objects are used to store key-value pairs, while arrays store ordered lists of items.</p>

        <h2>Understanding Objects</h2>
        <p>In JavaScript, objects are collections of properties, where each property is a key-value pair:</p>
        """,
        examples=[
            Example(
                title="Creating and Accessing Objects",
                code="""
// Define an object
const person = {
    name: "Alice",
    age: 30,
    greet: function() {
        console.log("Hello, " + this.name);
    }
};

// Access properties
console.log(person.name);  // Outputs: Alice
console.log(person.age);   // Outputs: 30

// Call method
person.greet();  // Outputs: Hello, Alice
""",
                explanation="This example demonstrates how to define an object with properties and a method. The 'greet' method accesses object properties using 'this'."
            ),
            Example(
                title="Working with Arrays",
                code="""
// Define an array
const fruits = ["apple", "banana", "cherry"];

// Access elements
console.log(fruits[0]);  // Outputs: apple

// Add an element
fruits.push("orange");
console.log(fruits);  // Outputs: ['apple', 'banana', 'cherry', 'orange']

// Remove an element
fruits.pop();
console.log(fruits);  // Outputs: ['apple', 'banana', 'cherry']
""",
                explanation="This example shows how to create an array, access elements, add items using 'push', and remove items with 'pop'."
            )
        ],
        exercises=[
            Exercise(
                title="Create a Simple Object",
                description="Create an object called 'book' with properties: title, author, and pages. Add a method that displays book details.",
                starter_code="""
const book = {
    // Define properties for title, author, and pages
    title: "",
    author: "",
    pages: 0,

    // Define a method to display details
    displayDetails: function() {
        // Add code here to display book details
    }
};

// Call displayDetails method
book.displayDetails();
""",
                solution="""
const book = {
    title: "JavaScript Basics",
    author: "John Doe",
    pages: 250,
    displayDetails: function() {
        console.log(`Title: ${this.title}, Author: ${this.author}, Pages: ${this.pages}`);
    }
};

book.displayDetails();  // Outputs: Title: JavaScript Basics, Author: John Doe, Pages: 250
""",
                difficulty="Beginner",
                hints=[
                    "Use 'this' to access properties within the method",
                    "Remember to set default values for properties"
                ]
            ),
            Exercise(
                title="Manipulate an Array",
                description="Create an array of numbers. Write functions to find the sum of all elements and to sort the array in ascending order.",
                starter_code="""
const numbers = [5, 3, 8, 1, 4];

// Function to find the sum of all elements
function sumArray(arr) {
    // Implement summation logic
}

// Function to sort array in ascending order
function sortArray(arr) {
    // Implement sorting logic
}

// Test the functions
console.log(sumArray(numbers));  // Expected output: 21
console.log(sortArray(numbers));  // Expected output: [1, 3, 4, 5, 8]
""",
                solution="""
const numbers = [5, 3, 8, 1, 4];

function sumArray(arr) {
    return arr.reduce((sum, num) => sum + num, 0);
}

function sortArray(arr) {
    return arr.slice().sort((a, b) => a - b);
}

console.log(sumArray(numbers));  // Outputs: 21
console.log(sortArray(numbers));  // Outputs: [1, 3, 4, 5, 8]
""",
                difficulty="Intermediate",
                hints=[
                    "Use the reduce method for summing elements",
                    "Use the sort method with a custom comparison function to sort in ascending order"
                ]
            )
        ],
        best_practices=[
            "Use meaningful property names for objects",
            "Access object properties using dot notation or bracket notation",
            "Use array methods like push, pop, shift, unshift for adding/removing items",
            "Use slice or spread syntax for array copies instead of direct assignment",
            "Consider using object destructuring to access multiple properties",
            "For larger data manipulation, consider chaining array methods like filter, map, and reduce"
        ]
    )
