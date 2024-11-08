from content.models import Topic, Example, Exercise

def create_events_and_event_handling_content() -> Topic:
    """Create and return JavaScript Events and Event Handling tutorial content."""
    return Topic(
        title="Events and Event Handling",
        description="Learn how to respond to user interactions by handling events in JavaScript.",
        content="""
        <h1>JavaScript Events and Event Handling</h1>
        <p>Events in JavaScript allow you to respond to user interactions like clicks, keyboard actions, and form submissions. Event handling is crucial for creating dynamic, interactive web pages.</p>

        <h2>Adding Event Listeners</h2>
        <p>In JavaScript, you can attach an event listener to an element using the <code>addEventListener</code> method. This method takes two main arguments: the event type (e.g., 'click', 'input') and the function to execute when the event occurs.</p>
        """,
        examples=[
            Example(
                title="Handling Click Events",
                code="""
// Selecting a button element
const button = document.getElementById("myButton");

// Adding a click event listener
button.addEventListener("click", function() {
    alert("Button was clicked!");
});
""",
                explanation="This example selects a button with the ID `myButton` and adds a `click` event listener to it. When the button is clicked, an alert displays the message 'Button was clicked!'"
            ),
            Example(
                title="Responding to Keyboard Events",
                code="""
// Selecting an input element
const inputField = document.getElementById("myInput");

// Adding a keydown event listener
inputField.addEventListener("keydown", function(event) {
    console.log(`Key pressed: ${event.key}`);
});
""",
                explanation="In this example, a `keydown` event listener is added to an input field with the ID `myInput`. Each time a key is pressed, it logs the pressed key to the console."
            )
        ],
        exercises=[
            Exercise(
                title="Toggle Text Color on Button Click",
                description="Create a button that toggles the color of a paragraph between red and black each time the button is clicked.",
                starter_code="""
// Select the button and paragraph elements

// Add a click event listener to the button
""",
                solution="""
// Select the button and paragraph elements
const button = document.getElementById("toggleButton");
const paragraph = document.getElementById("text");

// Add a click event listener to the button
button.addEventListener("click", function() {
    // Toggle the text color
    paragraph.style.color = paragraph.style.color === "red" ? "black" : "red";
});
""",
                difficulty="Beginner",
                hints=[
                    "Use `getElementById` to select the button and paragraph",
                    "Inside the event listener, use a ternary operator to toggle the paragraph's color",
                    "Set the color property using `style.color`"
                ]
            ),
            Exercise(
                title="Display Input Value on Enter Key Press",
                description="Write code that listens for the Enter key in an input field. When Enter is pressed, display the input's value in a paragraph below the field.",
                starter_code="""
// Select the input field and output paragraph

// Add a keydown event listener to the input field
""",
                solution="""
// Select the input field and output paragraph
const inputField = document.getElementById("myInput");
const output = document.getElementById("output");

// Add a keydown event listener to the input field
inputField.addEventListener("keydown", function(event) {
    // Check if the Enter key is pressed
    if (event.key === "Enter") {
        // Display the input value
        output.innerText = inputField.value;
        // Clear the input field
        inputField.value = "";
    }
});
""",
                difficulty="Beginner",
                hints=[
                    "Use `event.key` to detect the Enter key",
                    "Set `innerText` to display the input value",
                    "Clear the input field after displaying the value"
                ]
            )
        ],
        best_practices=[
            "Use `addEventListener` instead of inline event attributes",
            "Detach event listeners when no longer needed to avoid memory leaks",
            "Use descriptive function names for event handler functions",
            "Use event delegation for handling events on dynamically created elements",
            "Avoid anonymous functions if you need to remove the event listener later",
            "Remember to handle different types of events, such as mouse, keyboard, and form events"
        ]
    )
