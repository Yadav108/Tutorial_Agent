from content.models import Topic, Example, Exercise

def create_working_with_api_content() -> Topic:
    """Create and return a tutorial content on Working with APIs in JavaScript."""
    return Topic(
        title="Working with APIs",
        description="Learn how to work with APIs in JavaScript to fetch and send data.",
        content="""
        <h1>Working with APIs in JavaScript</h1>
        <p>APIs (Application Programming Interfaces) allow you to interact with external services and data sources. In JavaScript, the <code>fetch</code> API and the <code>XMLHttpRequest</code> object are commonly used to make HTTP requests to APIs and handle responses.</p>

        <h2>Using fetch</h2>
        <p>The <code>fetch</code> function provides a modern way to make HTTP requests. It returns a Promise that resolves to the Response object, which contains information about the response, including methods to read data as JSON, text, or blob.</p>

        <h2>Making GET and POST Requests</h2>
        <p>GET requests are used to retrieve data, while POST requests are used to send data to the server. With <code>fetch</code>, you can specify the request method, headers, and body to configure your request as needed.</p>

        <h2>Handling Responses and Errors</h2>
        <p>To work with API responses effectively, handle JSON parsing, status checks, and potential errors. Using <code>async/await</code> makes it easier to work with asynchronous fetch requests.</p>
        """,
        examples=[
            Example(
                title="Making a Simple GET Request",
                code="""
fetch('https://api.example.com/data')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.error('There was a problem with the fetch operation:', error));
""",
                explanation="This example shows a basic GET request using fetch. If the response is not okay (status code is not in the 200-299 range), an error is thrown and handled in the catch block."
            ),
            Example(
                title="Using async/await for API Requests",
                code="""
async function fetchData() {
    try {
        const response = await fetch('https://api.example.com/data');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

fetchData();
""",
                explanation="Using async/await makes the code cleaner and easier to read. Errors are caught in the try-catch block, simplifying error handling for API requests."
            ),
            Example(
                title="Making a POST Request",
                code="""
async function createUser(user) {
    try {
        const response = await fetch('https://api.example.com/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });
        if (!response.ok) throw new Error('Failed to create user');
        const data = await response.json();
        console.log('User created:', data);
    } catch (error) {
        console.error('Error creating user:', error);
    }
}

createUser({ name: 'John Doe', email: 'johndoe@example.com' });
""",
                explanation="This example demonstrates a POST request where a JSON object is sent as the request body. The JSON object is stringified before being sent to the server, and appropriate headers are set."
            ),
            Example(
                title="Handling API Errors Gracefully",
                code="""
async function fetchUserData(userId) {
    try {
        const response = await fetch(\`https://api.example.com/users/\${userId}\`);
        if (!response.ok) {
            if (response.status === 404) throw new Error('User not found');
            else throw new Error('An unexpected error occurred');
        }
        const data = await response.json();
        console.log('User data:', data);
    } catch (error) {
        console.error('Error fetching user data:', error.message);
    }
}

fetchUserData(123);
""",
                explanation="This example checks for specific response status codes to provide more informative error messages based on the situation, allowing for more user-friendly error handling."
            )
        ],
        exercises=[
            Exercise(
                title="Fetch and Display Data from an API",
                description="Write an async function `fetchPosts` that fetches posts from a sample API and logs each post’s title to the console.",
                starter_code="""
// Define the async fetchPosts function
async function fetchPosts() {
    // Add your code here
}

// Test the function
fetchPosts();
""",
                solution="""
// Define the async fetchPosts function
async function fetchPosts() {
    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/posts');
        if (!response.ok) throw new Error('Failed to fetch posts');
        const posts = await response.json();
        posts.forEach(post => console.log(post.title));
    } catch (error) {
        console.error('Error fetching posts:', error.message);
    }
}

// Test the function
fetchPosts();
""",
                difficulty="Beginner",
                hints=[
                    "Use async/await syntax for fetching data",
                    "Check if the response is okay with `response.ok`",
                    "Use the `.forEach` method to iterate over the posts"
                ]
            ),
            Exercise(
                title="POST Request to Add New Data",
                description="Create an async function `addPost` that sends a new post (title and body) to a sample API using POST and logs the response.",
                starter_code="""
// Define the async addPost function
async function addPost(post) {
    // Add your code here
}

// Test the function
addPost({ title: 'New Post', body: 'This is a new post' });
""",
                solution="""
// Define the async addPost function
async function addPost(post) {
    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/posts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(post)
        });
        if (!response.ok) throw new Error('Failed to add post');
        const data = await response.json();
        console.log('New post added:', data);
    } catch (error) {
        console.error('Error adding post:', error.message);
    }
}

// Test the function
addPost({ title: 'New Post', body: 'This is a new post' });
""",
                difficulty="Intermediate",
                hints=[
                    "Use the fetch method with `POST` to send data",
                    "Set the Content-Type header to 'application/json'",
                    "Use JSON.stringify to convert the post object to a JSON string"
                ]
            )
        ],
        best_practices=[
            "Always check if the response is okay (e.g., `response.ok`) before parsing data",
            "Use async/await for readability in asynchronous API calls",
            "Handle errors gracefully by providing informative messages",
            "Use headers to define content types and other important request information",
            "Structure API calls in reusable functions for easier testing and maintenance"
        ]
    )
