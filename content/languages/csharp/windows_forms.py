from content.models import Topic, Example, Exercise


def create_windows_forms_content() -> Topic:
    """Create and return Windows Forms tutorial content."""
    return Topic(
        title="Windows Forms",
        description="Learn to create basic desktop applications using Windows Forms in C#.",
        content="""
        <h1>Windows Forms in C#</h1>
        <p>Windows Forms, or WinForms, is a UI framework in .NET for building desktop applications with a graphical user interface. It provides a visual designer to drag-and-drop controls, making it easy to build interactive applications.</p>

        <h2>Getting Started with Windows Forms</h2>
        <p>To create a Windows Forms application, you'll need Visual Studio. When creating a new project, select 'Windows Forms App (.NET Framework)' or 'Windows Forms App (.NET Core)'.</p>

        <h3>Main Components</h3>
        <ul>
            <li><strong>Form</strong>: The main window of the application.</li>
            <li><strong>Controls</strong>: Elements like buttons, labels, and textboxes that users can interact with.</li>
            <li><strong>Event Handlers</strong>: Code that executes in response to user actions, like button clicks.</li>
        </ul>

        <h2>Example: Basic Windows Form Application</h2>
        <p>This example demonstrates creating a simple form with a button that displays a message when clicked.</p>

        <pre><code>using System;
using System.Windows.Forms;

namespace MyWinFormsApp
{
    public class MainForm : Form
    {
        private Button myButton;

        public MainForm()
        {
            // Initialize the button
            myButton = new Button();
            myButton.Text = "Click Me!";
            myButton.Location = new System.Drawing.Point(50, 50);

            // Add a click event handler
            myButton.Click += new EventHandler(MyButton_Click);

            // Add button to the form
            Controls.Add(myButton);
        }

        private void MyButton_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Hello, Windows Forms!");
        }

        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.Run(new MainForm());
        }
    }
}</code></pre>

        <p>In this example, a button is added to the form, and a click event handler displays a message box when the button is clicked.</p>
        """,
        examples=[
            Example(
                title="Creating a Basic Form with Textbox and Button",
                code="""
                using System;
                using System.Windows.Forms;

                namespace MyWinFormsApp
                {
                    public class MainForm : Form
                    {
                        private TextBox inputTextBox;
                        private Button showButton;

                        public MainForm()
                        {
                            // Initialize TextBox
                            inputTextBox = new TextBox();
                            inputTextBox.Location = new System.Drawing.Point(20, 20);

                            // Initialize Button
                            showButton = new Button();
                            showButton.Text = "Show Text";
                            showButton.Location = new System.Drawing.Point(20, 60);
                            showButton.Click += ShowButton_Click;

                            // Add controls to the form
                            Controls.Add(inputTextBox);
                            Controls.Add(showButton);
                        }

                        private void ShowButton_Click(object sender, EventArgs e)
                        {
                            MessageBox.Show("You entered: " + inputTextBox.Text);
                        }

                        [STAThread]
                        public static void Main()
                        {
                            Application.EnableVisualStyles();
                            Application.Run(new MainForm());
                        }
                    }
                }
                """,
                explanation="This example adds a textbox and button to the form. When the button is clicked, it displays the text entered in the textbox using a message box."
            ),
            Example(
                title="Basic Calculator with Windows Forms",
                code="""
                using System;
                using System.Windows.Forms;

                namespace CalculatorApp
                {
                    public class CalculatorForm : Form
                    {
                        private TextBox input1, input2;
                        private Button addButton;
                        private Label resultLabel;

                        public CalculatorForm()
                        {
                            // Initialize components
                            input1 = new TextBox() { Location = new System.Drawing.Point(20, 20) };
                            input2 = new TextBox() { Location = new System.Drawing.Point(20, 60) };
                            addButton = new Button() { Text = "Add", Location = new System.Drawing.Point(20, 100) };
                            resultLabel = new Label() { Location = new System.Drawing.Point(20, 140) };

                            // Add event handler for the button
                            addButton.Click += AddButton_Click;

                            // Add components to the form
                            Controls.Add(input1);
                            Controls.Add(input2);
                            Controls.Add(addButton);
                            Controls.Add(resultLabel);
                        }

                        private void AddButton_Click(object sender, EventArgs e)
                        {
                            if (double.TryParse(input1.Text, out double num1) && double.TryParse(input2.Text, out double num2))
                            {
                                double sum = num1 + num2;
                                resultLabel.Text = "Result: " + sum;
                            }
                            else
                            {
                                resultLabel.Text = "Please enter valid numbers.";
                            }
                        }

                        [STAThread]
                        public static void Main()
                        {
                            Application.EnableVisualStyles();
                            Application.Run(new CalculatorForm());
                        }
                    }
                }
                """,
                explanation="This example shows a simple calculator form with two input boxes, an 'Add' button, and a label to display the result."
            )
        ],
        exercises=[
            Exercise(
                title="Create a User Info Form",
                description="Create a form with fields for entering a name, age, and a button that displays a greeting message including the entered details.",
                starter_code="""
                using System;
                using System.Windows.Forms;

                namespace UserInfoApp
                {
                    public class UserInfoForm : Form
                    {
                        // Define components here

                        public UserInfoForm()
                        {
                            // Initialize and arrange components
                        }

                        // Define event handler here

                        [STAThread]
                        public static void Main()
                        {
                            Application.EnableVisualStyles();
                            Application.Run(new UserInfoForm());
                        }
                    }
                }
                """,
                solution="""
                using System;
                using System.Windows.Forms;

                namespace UserInfoApp
                {
                    public class UserInfoForm : Form
                    {
                        private TextBox nameBox, ageBox;
                        private Button greetButton;

                        public UserInfoForm()
                        {
                            // Initialize components
                            nameBox = new TextBox { Location = new System.Drawing.Point(20, 20), PlaceholderText = "Name" };
                            ageBox = new TextBox { Location = new System.Drawing.Point(20, 60), PlaceholderText = "Age" };
                            greetButton = new Button { Text = "Greet", Location = new System.Drawing.Point(20, 100) };

                            // Event handler for button
                            greetButton.Click += (sender, e) =>
                            {
                                MessageBox.Show($"Hello, {nameBox.Text}! You are {ageBox.Text} years old.");
                            };

                            // Add controls to the form
                            Controls.Add(nameBox);
                            Controls.Add(ageBox);
                            Controls.Add(greetButton);
                        }

                        [STAThread]
                        public static void Main()
                        {
                            Application.EnableVisualStyles();
                            Application.Run(new UserInfoForm());
                        }
                    }
                }
                """,
                difficulty="Intermediate",
                hints=[
                    "Use TextBox for name and age input fields.",
                    "Add an event handler to the button to show a message box with the user's input."
                ]
            ),
            Exercise(
                title="Create a Counter Application",
                description="Create a form with a label to display a counter and two buttons: one to increment and one to decrement the counter.",
                starter_code="""
                using System;
                using System.Windows.Forms;

                namespace CounterApp
                {
                    public class CounterForm : Form
                    {
                        // Define components and event handlers

                        [STAThread]
                        public static void Main()
                        {
                            Application.EnableVisualStyles();
                            Application.Run(new CounterForm());
                        }
                    }
                }
                """,
                solution="""
                using System;
                using System.Windows.Forms;

                namespace CounterApp
                {
                    public class CounterForm : Form
                    {
                        private int counter = 0;
                        private Label counterLabel;
                        private Button incrementButton, decrementButton;

                        public CounterForm()
                        {
                            // Initialize components
                            counterLabel = new Label { Text = "0", Location = new System.Drawing.Point(100, 20) };
                            incrementButton = new Button { Text = "Increment", Location = new System.Drawing.Point(20, 60) };
                            decrementButton = new Button { Text = "Decrement", Location = new System.Drawing.Point(120, 60) };

                            // Add event handlers
                            incrementButton.Click += (sender, e) => UpdateCounter(1);
                            decrementButton.Click += (sender, e) => UpdateCounter(-1);

                            // Add controls to the form
                            Controls.Add(counterLabel);
                            Controls.Add(incrementButton);
                            Controls.Add(decrementButton);
                        }

                        private void UpdateCounter(int value)
                        {
                            counter += value;
                            counterLabel.Text = counter.ToString();
                        }

                        [STAThread]
                        public static void Main()
                        {
                            Application.EnableVisualStyles();
                            Application.Run(new CounterForm());
                        }
                    }
                }
                """,
                difficulty="Intermediate",
                hints=[
                    "Use a Label to display the counter value.",
                    "Add event handlers to increment or decrement the counter",
                    "Use a separate method to update the counter value and display it on the label."
                ]
            )
        ],
        best_practices=[
            "Organize your controls with consistent layout for better readability and user experience.",
            "Use meaningful control names (e.g., `submitButton`, `nameTextBox`) for clarity in your code.",
            "Keep event handler methods concise; move any complex logic to separate helper methods.",
            "Add comments to explain the purpose of each control and event handler.",
            "Avoid hardcoding layout values; use anchors or dock properties for responsive design when possible.",
            "Test your application to handle different user inputs, especially edge cases.",
            "Use Visual Studio’s designer for faster layout adjustments, but review auto-generated code carefully."
        ]
    )

