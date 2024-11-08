from content.models import Topic, Example, Exercise

def create_dom_manipulation_content() -> Topic:
    """Create and return JavaScript DOM Manipulation tutorial content."""
    return Topic(
        title="DOM Manipulation",
        description="Learn how to manipulate the Document Object Model (DOM) in JavaScript to interact with and modify HTML elements.",
        content="""
        <h1>JavaScript DOM Manipulation</h1>
        <p>The Document Object Model (DOM) represents the structure of a webpage, allowing JavaScript to interact with HTML elements. Using DOM manipulation, we can dynamically change content, styles, attributes, and even create new elements on the fly.</p>

        <h2>Selecting Elements</h2>
        <p>To manipulate the DOM, we first need to select elements using methods like <code>getElementById</code>, <code>getElementsByClassName</code>, <code>querySelector</code>, and <code>querySelectorAll</code>.</p>
        """,
        examples=[
            Example(
                title="Selecting and Modifying Elements",
                code="""
// Selecting an element by ID and modifying its content
document.getElementById("myTitle").innerText = "New Title";

// Selecting an element by class and modifying its style
const myElement = document.querySelector(".highlight");
myElement.style.color = "blue";
""",
                explanation="In this example, `getElementById` selects an element with the ID `myTitle` and updates its text content. `querySelector` selects the first element with the class `highlight` and changes its text color to blue."
            ),
            Example(
                title="Adding and Removing Elements",
                code="""
// Creating a new element
const newParagraph = document.createElement("p");
newParagraph.innerText = "This is a new paragraph.";

// Appending the new element to an existing div
document.getElementById("container").appendChild(newParagraph);

// Removing an element by reference
const elementToRemove = document.getElementById("oldElement");
elementToRemove.remove();
""",
                explanation="This example shows how to create a new paragraph element, set its text content, and append it to an existing div. It also demonstrates removing an element by selecting and calling `remove()` on it."
            )
        ],
        exercises=[
            Exercise(
                title="Change Element Content and Style",
                description="Select an element with the ID 'mainTitle' and change its text content to 'Welcome to My Site'. Then, select all elements with the class 'menu-item' and change their background color to 'lightgray'.",
                starter_code="""
// Change content of element with ID 'mainTitle'

// Change background color of elements with class 'menu-item'
""",
                solution="""
// Change content of element with ID 'mainTitle'
document.getElementById("mainTitle").innerText = "Welcome to My Site";

// Change background color of elements with class 'menu-item'
const menuItems = document.querySelectorAll(".menu-item");
menuItems.forEach(item => {
    item.style.backgroundColor = "lightgray";
});
""",
                difficulty="Beginner",
                hints=[
                    "Use `getElementById` for the mainTitle",
                    "Use `querySelectorAll` to select all menu items",
                    "Use a loop or `forEach` to apply styles to each menu item"
                ]
            ),
            Exercise(
                title="Create and Insert New Elements",
                description="Write code that creates a new list item element with the text 'New Item' and appends it to an unordered list with the ID 'itemList'.",
                starter_code="""
// Create a new list item

// Set the list item's text

// Append it to the unordered list
""",
                solution="""
// Create a new list item
const newItem = document.createElement("li");

// Set the list item's text
newItem.innerText = "New Item";

// Append it to the unordered list
document.getElementById("itemList").appendChild(newItem);
""",
                difficulty="Beginner",
                hints=[
                    "Use `createElement` to create a new `li` element",
                    "Set `innerText` to add text to the list item",
                    "Use `getElementById` to select the `itemList` unordered list"
                ]
            )
        ],
        best_practices=[
            "Use `getElementById` and `querySelector` to select elements efficiently",
            "When possible, use `querySelectorAll` to apply changes to multiple elements",
            "Use `createElement` and `appendChild` to dynamically add new elements",
            "Remove elements using `removeChild` or directly calling `remove()`",
            "Use meaningful variable names to clarify what elements are being modified",
            "Add event listeners to handle user interactions in real-time"
        ]
    )
