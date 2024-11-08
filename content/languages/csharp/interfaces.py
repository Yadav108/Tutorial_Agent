from content.models import Topic, Example, Exercise

def create_inheritance_content() -> Topic:
    """Create and return Inheritance tutorial content."""
    return Topic(
        title="Inheritance",
        description="Learn how to use inheritance in C# to create relationships between classes, enabling code reuse and creating a hierarchy of classes.",
        content="""
        <h1>Inheritance in C#</h1>
        <p>Inheritance allows one class (called the derived or child class) to inherit the fields and methods of another class (called the base or parent class). It promotes code reuse and establishes a hierarchy between classes.</p>

        <h2>Defining a Base and Derived Class</h2>
        <p>To create a derived class in C#, use the <code>:</code> symbol after the class name, followed by the base class name.</p>

        <pre><code>class Animal
{
    public void Eat()
    {
        Console.WriteLine("Eating...");
    }
}

class Dog : Animal
{
    public void Bark()
    {
        Console.WriteLine("Barking...");
    }
}</code></pre>

        <h2>Using the Derived Class</h2>
        <p>The derived class can use its own methods as well as the inherited methods of the base class:</p>
        <pre><code>Dog dog = new Dog();
dog.Eat();  // Inherited from Animal
dog.Bark(); // Defined in Dog</code></pre>

        <h2>Overriding Methods</h2>
        <p>To provide a different implementation of a method in a derived class, use the <code>virtual</code> keyword in the base class and the <code>override</code> keyword in the derived class:</p>

        <pre><code>class Animal
{
    public virtual void Speak()
    {
        Console.WriteLine("Animal sound");
    }
}

class Dog : Animal
{
    public override void Speak()
    {
        Console.WriteLine("Bark");
    }
}</code></pre>
        """,
        examples=[
            Example(
                title="Basic Inheritance Example",
                code="""
                using System;

                // Base class
                class Vehicle
                {
                    public int Speed { get; set; }

                    public void Drive()
                    {
                        Console.WriteLine("Driving at speed " + Speed);
                    }
                }

                // Derived class
                class Car : Vehicle
                {
                    public int NumberOfDoors { get; set; }

                    public void DisplayCarInfo()
                    {
                        Console.WriteLine($"Car with {NumberOfDoors} doors, speed {Speed}");
                    }
                }

                class Program
                {
                    static void Main()
                    {
                        Car car = new Car();
                        car.Speed = 100;
                        car.NumberOfDoors = 4;
                        car.Drive();
                        car.DisplayCarInfo();
                    }
                }
                """,
                explanation="This example shows a base class `Vehicle` with a `Drive` method and a derived class `Car` with its own additional property and method."
            ),
            Example(
                title="Overriding Methods",
                code="""
                using System;

                // Base class
                class Animal
                {
                    public virtual void Speak()
                    {
                        Console.WriteLine("Animal sound");
                    }
                }

                // Derived class
                class Dog : Animal
                {
                    public override void Speak()
                    {
                        Console.WriteLine("Bark");
                    }
                }

                class Program
                {
                    static void Main()
                    {
                        Animal myAnimal = new Animal();
                        myAnimal.Speak(); // Animal sound

                        Dog myDog = new Dog();
                        myDog.Speak(); // Bark

                        Animal myPet = new Dog();
                        myPet.Speak(); // Bark (polymorphism)
                    }
                }
                """,
                explanation="This example demonstrates method overriding. The `Dog` class overrides the `Speak` method of the `Animal` base class."
            )
        ],
        exercises=[
            Exercise(
                title="Create a Derived Class",
                description="Create a base class `Person` with a method `Greet`. Create a derived class `Student` that adds a `Study` method.",
                starter_code="""
                // Define the Person class with a Greet method

                // Define the Student class that inherits from Person and adds a Study method
                """,
                solution="""
                using System;

                // Base class
                class Person
                {
                    public void Greet()
                    {
                        Console.WriteLine("Hello!");
                    }
                }

                // Derived class
                class Student : Person
                {
                    public void Study()
                    {
                        Console.WriteLine("Studying...");
                    }
                }

                class Program
                {
                    static void Main()
                    {
                        Student student = new Student();
                        student.Greet();
                        student.Study();
                    }
                }
                """,
                difficulty="Beginner",
                hints=[
                    "Define the `Greet` method in `Person`.",
                    "Inherit from `Person` in the `Student` class.",
                    "Add a `Study` method to `Student`."
                ]
            ),
            Exercise(
                title="Override a Method",
                description="Create a base class `Appliance` with a virtual method `Start`. Create a derived class `WashingMachine` that overrides `Start` to print a specific message.",
                starter_code="""
                // Define the Appliance class with a virtual Start method

                // Define the WashingMachine class that inherits from Appliance and overrides Start
                """,
                solution="""
                using System;

                // Base class
                class Appliance
                {
                    public virtual void Start()
                    {
                        Console.WriteLine("Appliance starting...");
                    }
                }

                // Derived class
                class WashingMachine : Appliance
                {
                    public override void Start()
                    {
                        Console.WriteLine("Washing machine starting...");
                    }
                }

                class Program
                {
                    static void Main()
                    {
                        Appliance appliance = new Appliance();
                        appliance.Start(); // Appliance starting...

                        WashingMachine washer = new WashingMachine();
                        washer.Start(); // Washing machine starting...
                    }
                }
                """,
                difficulty="Intermediate",
                hints=[
                    "Define the `Start` method as virtual in `Appliance`.",
                    "Override `Start` in `WashingMachine` with a specific message."
                ]
            )
        ],
        best_practices=[
            "Use inheritance to reuse code and create class hierarchies.",
            "Override methods only when the derived class needs to alter the base class behavior.",
            "Use the `base` keyword to access base class members from a derived class.",
            "Be mindful of the Liskov Substitution Principle: derived classes should be able to replace base classes without affecting program correctness.",
            "Avoid excessive inheritance hierarchies, as they can make code complex and harder to maintain."
        ]
    )