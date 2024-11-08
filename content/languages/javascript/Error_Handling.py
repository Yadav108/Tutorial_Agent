from content.models import Topic, Example, Exercise

def create_error_handling_content() -> Topic:
    """Create and return a tutorial content on Error Handling in JavaScript."""
    return Topic(
        title="Error Handling",
        description="Learn how to handle runtime errors in JavaScript using try-catch blocks, custom error objects, and best practices for debugging.",
        content="""
        <h1>Error Handling in JavaScript</h1>
        <p>Handling errors properly is crucial to building robust JavaScript applications. JavaScript provides the <code>try-catch</code> construct, custom error objects, and async error handling to help manage runtime errors effectively.</p>

        <h2>try-catch</h2>
        <p>The <code>try</code> block lets you define code to test for errors, and the <code>catch</code> block handles any errors that occur. This construct helps you capture exceptions and prevent the program from crashing unexpectedly.</p>

        <h2>throw</h2>
        <p>The <code>throw</code> statement lets you create custom error messages or conditions. You can throw an error manually in situations where you want to signal an exceptional condition or validate data.</p>

        <h2>finally</h2>
        <p>The <code>finally</code> block executes after <code>try</code> and <code>catch</code>, regardless of whether an error occurred. It’s useful for cleanup operations like closing connections or freeing resources.</p>

        <h2>Custom Error Objects</h2>
        <p>You can create custom error classes to define specific types of errors in your application, extending JavaScript's built-in <code>Error</code> class.</p>

        <h2>Error Handling in Async Code</h2>
        <p>Handling errors in asynchronous code, like Promises or async/await, requires special attention to ensure errors don’t go unhandled.</p>
        """,
        examples=[
            Example(
                title="Basic try-catch Example",
                code="""
try {
    let result = 10 / 0;
    console.log(result);
} catch (error) {
    console.error("An error occurred:", error.message);
}
""",
                explanation="This example uses try-catch to capture and handle any potential errors that occur in the try block. The catch block logs a custom error message to the console."
            ),
            Example(
                title="Using throw to Create a Custom Error",
                code="""
function divide(a, b) {
    if (b === 0) {
        throw new Error("Cannot divide by zero");
    }
    return a / b;
}

try {
    console.log(divide(10, 0));
} catch (error) {
    console.error(error.message);
}
""",
                explanation="This function throws an error if there’s an attempt to divide by zero. The catch block captures this error and logs the custom message."
            ),
            Example(
                title="finally Block Example",
                code="""
try {
    console.log("Trying...");
    throw new Error("An error has occurred!");
} catch (error) {
    console.error(error.message);
} finally {
    console.log("Cleanup code in finally block executed.");
}
""",
                explanation="The finally block executes after the try and catch blocks, regardless of whether an error occurs. This is ideal for cleanup or logging operations."
            ),
            Example(
                title="Creating a Custom Error Class",
                code="""
class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = "ValidationError";
    }
}

try {
    throw new ValidationError("Invalid email address");
} catch (error) {
    console.error(error.name + ": " + error.message);
}
""",
                explanation="This custom error class, `ValidationError`, extends the built-in Error class. It allows you to create specific error types for different scenarios."
            ),
            Example(
                title="Handling Errors in Async/Await Functions",
                code="""
async function fetchData() {
    try {
        let response = await fetch('https://api.example.com/data');
        if (!response.ok) throw new Error("Network response was not ok");
        let data = await response.json();
        console.log(data);
    } catch (error) {
        console.error("Error fetching data:", error.message);
    }
}

fetchData();
""",
                explanation="In this async function, the try-catch structure captures any errors that might occur during the async operations, like network issues or response errors."
            )
        ],
        exercises=[
            Exercise(
                title="Custom Error Handling Function",
                description="Create a function `calculateSquareRoot(number)` that throws an error if the input is negative. Use try-catch to handle the error and log a custom message.",
                starter_code="""
// Define the calculateSquareRoot function
function calculateSquareRoot(number) {
    // Throw an error if number is negative
}

// Test the function
try {
    calculateSquareRoot(-9);
} catch (error) {
    console.error(error.message);
}
""",
                solution="""
// Define the calculateSquareRoot function
function calculateSquareRoot(number) {
    if (number < 0) {
        throw new Error("Cannot calculate square root of a negative number");
    }
    return Math.sqrt(number);
}

// Test the function
try {
    console.log(calculateSquareRoot(9)); // Output: 3
    calculateSquareRoot(-9); // Error: Cannot calculate square root of a negative number
} catch (error) {
    console.error(error.message);
}
""",
                difficulty="Intermediate",
                hints=[
                    "Use `throw` to create a custom error message",
                    "Check if `number` is negative and throw an error if so",
                    "Use try-catch to handle any thrown errors"
                ]
            ),
            Exercise(
                title="Fetch Data with Error Handling",
                description="Write an async function `fetchUserData(url)` that fetches data from the given URL and handles any errors. Use try-catch to catch errors and log a message.",
                starter_code="""
// Define the async fetchUserData function
async function fetchUserData(url) {
    // Add your code here
}

// Test the function with a sample URL
""",
                solution="""
// Define the async fetchUserData function
async function fetchUserData(url) {
    try {
        let response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch data");
        let data = await response.json();
        console.log(data);
    } catch (error) {
        console.error("Error:", error.message);
    }
}

// Test the function with a sample URL
fetchUserData("https://api.example.com/users");
""",
                difficulty="Intermediate",
                hints=[
                    "Use async-await syntax within the function",
                    "Use try-catch to capture any potential errors",
                    "Check if the response is okay with `response.ok` before processing the data"
                ]
            )
        ],
        best_practices=[
            "Always use try-catch for operations that may fail, especially in async code",
            "Use custom error classes to provide more detailed error information",
            "Add a finally block when cleanup is necessary, regardless of success or failure",
            "Throw custom errors when specific conditions are met to avoid silent failures",
            "Log errors for easier debugging, especially in production environments"
        ]
    )
