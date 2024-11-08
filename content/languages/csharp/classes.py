from content.models import Topic, Example, Exercise


def create_classes_content() -> Topic:
    """Create and return Classes tutorial content."""
    return Topic(
        title="Classes",
        description="Learn about creating and using classes in C#, including attributes, methods, constructors, and encapsulation.",
        content="""
        <h1>Classes in C#</h1>
        <p>Classes are blueprints for creating objects in C#. They can contain data (fields or properties) and behaviors (methods).</p>

        <h2>Defining a Class</h2>
        <p>To define a class in C#, use the <code>class</code> keyword followed by the class name:</p>

        <pre><code>class Person
{
    // Fields
    private string name;
    private int age;

    // Constructor
    public Person(string name, int age)
    {
        this.name = name;
        this.age = age;
    }

    // Method
    public void Greet()
    {
        Console.WriteLine($"Hello, my name is {name} and I am {age} years old.");
    }
}</code></pre>

        <h2>Creating an Object</h2>
        <p>Once a class is defined, you can create an object (instance) of that class using the <code>new</code> keyword:</p>
        <pre><code>Person person = new Person("Alice", 30);</code></pre>

        <h2>Encapsulation</h2>
        <p>Encapsulation is a core principle of object-oriented programming that restricts access to certain parts of an object. 
        You can use <code>private</code> to hide fields and expose them with public properties or methods.</p>
        """,
        examples=[
            Example(
                title="Defining and Using a Class",
                code="""
                using System;

                class Car
                {
                    // Fields
                    private string make;
                    private string model;
                    private int year;

                    // Constructor
                    public Car(string make, string model, int year)
                    {
                        this.make = make;
                        this.model = model;
                        this.year = year;
                    }

                    // Method
                    public void DisplayInfo()
                    {
                        Console.WriteLine($"Car: {year} {make} {model}");
                    }
                }

                class Program
                {
                    static void Main()
                    {
                        Car car = new Car("Toyota", "Camry", 2020);
                        car.DisplayInfo();
                    }
                }
                """,
                explanation="This example demonstrates how to define a class with fields, a constructor, and a method, and then create an instance of the class to use the method."
            ),
            Example(
                title="Encapsulation with Properties",
                code="""
                using System;

                class BankAccount
                {
                    // Private field
                    private double balance;

                    // Property for balance
                    public double Balance
                    {
                        get { return balance; }
                        private set { balance = value; }
                    }

                    // Constructor
                    public BankAccount(double initialBalance)
                    {
                        balance = initialBalance;
                    }

                    // Method to deposit money
                    public void Deposit(double amount)
                    {
                        if (amount > 0)
                        {
                            Balance += amount;
                            Console.WriteLine($"Deposited: ${amount}");
                        }
                    }
                }

                class Program
                {
                    static void Main()
                    {
                        BankAccount account = new BankAccount(100);
                        account.Deposit(50);
                        Console.WriteLine($"Balance: ${account.Balance}");
                    }
                }
                """,
                explanation="This example shows encapsulation using a property to control access to the balance field."
            )
        ],
        exercises=[
            Exercise(
                title="Define a Simple Class",
                description="Create a class named 'Book' with fields for title, author, and pages. Add a constructor and a method to display book details.",
                starter_code="""
                // Define the Book class

                // Add fields for title, author, and pages

                // Add a constructor to initialize the fields

                // Add a method to display book details
                """,
                solution="""
                using System;

                class Book
                {
                    // Fields
                    private string title;
                    private string author;
                    private int pages;

                    // Constructor
                    public Book(string title, string author, int pages)
                    {
                        this.title = title;
                        this.author = author;
                        this.pages = pages;
                    }

                    // Method
                    public void DisplayInfo()
                    {
                        Console.WriteLine($"Title: {title}, Author: {author}, Pages: {pages}");
                    }
                }

                class Program
                {
                    static void Main()
                    {
                        Book book = new Book("The Great Gatsby", "F. Scott Fitzgerald", 180);
                        book.DisplayInfo();
                    }
                }
                """,
                difficulty="Beginner",
                hints=[
                    "Define a constructor to initialize the fields.",
                    "Create a method that prints the book details."
                ]
            ),
            Exercise(
                title="Encapsulate Fields with Properties",
                description="Create a class named 'Rectangle' with fields for length and width, and properties to get and set these fields. Add a method to calculate the area.",
                starter_code="""
                // Define the Rectangle class

                // Add fields for length and width

                // Add properties for length and width

                // Add a method to calculate and return the area
                """,
                solution="""
                using System;

                class Rectangle
                {
                    // Fields
                    private double length;
                    private double width;

                    // Properties
                    public double Length
                    {
                        get { return length; }
                        set { length = value; }
                    }

                    public double Width
                    {
                        get { return width; }
                        set { width = value; }
                    }

                    // Constructor
                    public Rectangle(double length, double width)
                    {
                        this.Length = length;
                        this.Width = width;
                    }

                    // Method to calculate area
                    public double CalculateArea()
                    {
                        return length * width;
                    }
                }

                class Program
                {
                    static void Main()
                    {
                        Rectangle rect = new Rectangle(5.0, 3.0);
                        Console.WriteLine($"Area: {rect.CalculateArea()}");
                    }
                }
                """,
                difficulty="Intermediate",
                hints=[
                    "Use properties to encapsulate length and width fields.",
                    "Create a method that multiplies length and width to calculate the area."
                ]
            )
        ],
        best_practices=[
            "Use private fields to encapsulate data.",
            "Create constructors to initialize objects with default values.",
            "Use properties to control access to fields.",
            "Use meaningful names for classes, fields, and methods.",
            "Create methods to perform specific actions, encapsulating functionality."
        ]
    )
