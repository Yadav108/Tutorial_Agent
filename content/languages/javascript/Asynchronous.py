from content.legacy_models import Topic, Exercise
from content.models import Example

def create() -> Topic:
    """Create and return Asynchronous JavaScript tutorial content."""
    return Topic(
        title="Asynchronous JavaScript",
        description="Understand how to handle asynchronous tasks in JavaScript using callbacks, promises, and async/await.",
        content="""
        <h1>Asynchronous JavaScript</h1>
        <p>JavaScript is single-threaded, meaning it can only execute one task at a time. However, JavaScript can manage asynchronous operations, such as API requests or time-based functions, without blocking other code execution. Asynchronous programming is essential for responsive and efficient applications.</p>

        <h2>Using Callbacks</h2>
        <p>A callback is a function passed into another function as an argument, which is then executed once the operation completes.</p>

        <h2>Promises</h2>
        <p>Promises are objects that represent the eventual completion or failure of an asynchronous operation and its resulting value. Promises have three states: pending, fulfilled, or rejected.</p>

        <h2>Async/Await</h2>
        <p>The <code>async</code> and <code>await</code> keywords provide a syntactic sugar over promises, making asynchronous code look and behave more like synchronous code.</p>
        """,
        examples=[
            Example(
                title="Using Callbacks",
                code="""
// A function that simulates an asynchronous task with a callback
function fetchData(callback) {
    setTimeout(() => {
        callback("Data fetched!");
    }, 1000);
}

// Using the function with a callback
fetchData((result) => {
    console.log(result);
});
""",
                explanation="This example shows a function `fetchData` that takes a callback. After a 1-second delay, it calls the callback with 'Data fetched!'."
            ),
            Example(
                title="Using Promises",
                code="""
// A function that simulates fetching data with a Promise
function fetchData() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve("Data fetched with promise!");
        }, 1000);
    });
}

// Using the promise with .then() and .catch()
fetchData()
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
""",
                explanation="This example demonstrates a promise-based `fetchData` function. It returns a promise that resolves after 1 second. The `.then()` method is used to handle the resolved data."
            ),
            Example(
                title="Using Async/Await",
                code="""
// A function that simulates data fetching
function fetchData() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve("Data fetched asynchronously!");
        }, 1000);
    });
}

// Using async/await
async function displayData() {
    const result = await fetchData();
    console.log(result);
}

// Calling the async function
displayData();
""",
                explanation="In this example, `fetchData` returns a promise, and `displayData` uses `async/await` to handle the promise, waiting until the promise resolves before proceeding."
            )
        ],
        exercises=[
            Exercise(
                title="Simulate an API Request with Callback",
                description="Create a function `getUserData` that simulates a user data fetch with a 2-second delay. Pass in a callback to handle the result.",
                starter_code="""
// Define the getUserData function

// Call getUserData with a callback
""",
                solution="""
// Define the getUserData function
function getUserData(callback) {
    setTimeout(() => {
        callback("User data fetched!");
    }, 2000);
}

// Call getUserData with a callback
getUserData((result) => {
    console.log(result);
});
""",
                difficulty="Beginner",
                hints=[
                    "Use `setTimeout` to simulate the delay",
                    "Pass the callback function as an argument to `getUserData`",
                    "Use `callback()` inside `setTimeout` to call it after the delay"
                ]
            ),
            Exercise(
                title="Use Async/Await with Fetch",
                description="Create a function `fetchAndDisplayData` that fetches data from an API and logs it. Use async/await.",
                starter_code="""
// Define the fetchAndDisplayData function using async

// Call fetchAndDisplayData
""",
                solution="""
// Define the fetchAndDisplayData function using async
async function fetchAndDisplayData() {
    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/todos/1');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Call fetchAndDisplayData
fetchAndDisplayData();
""",
                difficulty="Intermediate",
                hints=[
                    "Use the `await` keyword to wait for the fetch request",
                    "Convert the response to JSON using `await response.json()`",
                    "Use a try/catch block to handle potential errors"
                ]
            )
        ],
        best_practices=[
            "Use async/await for readability in asynchronous code",
            "Always handle errors in promises with `.catch()` or a try/catch block",
            "Avoid callback hell by using promises or async/await",
            "Use meaningful function names for clarity",
            "Be cautious with blocking asynchronous code, especially in loops",
            "Use Promise.all() when waiting for multiple promises to resolve"
        ]
    )
