"""Python object-oriented programming tutorial content."""

from content.models import Topic, Example, Exercise


def create_object_oriented_programming_content() -> Topic:
    """Create and return Python OOP tutorial content."""
    return Topic(
        title="Object-Oriented Programming",
        description="Learn about classes, objects, inheritance, and other OOP concepts in Python.",
        content="""
        <h1>Object-Oriented Programming in Python</h1>
        <p>Object-Oriented Programming (OOP) is a programming paradigm that organizes code into objects that contain both data and behavior.</p>

        <h2>Classes and Objects</h2>
        <p>Classes are blueprints for creating objects, which are instances of the class:</p>
        """,
        examples=[
            Example(
                title="Basic Class Definition",
                code="""class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name} says Woof!"

# Creating and using objects
buddy = Dog("Buddy", 5)
max = Dog("Max", 3)

print(buddy.bark())  # Output: Buddy says Woof!
print(f"{max.name} is {max.age} years old")""",
                explanation="This example shows how to create a basic class with attributes (name, age) and a method (bark). The __init__ method is the constructor that initializes new objects."
            ),
            Example(
                title="Inheritance",
                code="""class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def make_sound(self):
        return "Some sound"

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, species="Cat")
        self.color = color

    def make_sound(self):
        return "Meow!"

# Using inheritance
kitty = Cat("Whiskers", "Orange")
print(f"{kitty.name} is a {kitty.species}")
print(f"{kitty.name} says: {kitty.make_sound()}")""",
                explanation="This example demonstrates inheritance, where Cat class inherits from Animal class. It shows method overriding (make_sound) and using super() to call the parent class's methods."
            )
        ],
        exercises=[
            Exercise(
                title="Create a Bank Account Class",
                description="Create a BankAccount class that can handle deposits, withdrawals, and maintain a balance.",
                starter_code="""class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        # Initialize the account
        pass

    def deposit(self, amount):
        # Handle deposit
        pass

    def withdraw(self, amount):
        # Handle withdrawal
        pass

    def get_balance(self):
        # Return current balance
        pass

# Test your class
account = BankAccount("John Doe", 1000)
account.deposit(500)
account.withdraw(200)
print(account.get_balance())  # Should print 1300""",
                solution="""class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited ${amount}. New balance: ${self.balance}"
        return "Invalid deposit amount"

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        return "Insufficient funds or invalid amount"

    def get_balance(self):
        return f"Current balance: ${self.balance}"

# Test your class
account = BankAccount("John Doe", 1000)
print(account.deposit(500))
print(account.withdraw(200))
print(account.get_balance())""",
                difficulty="Intermediate",
                hints=[
                    "Store the balance as an instance variable",
                    "Check for valid amounts in deposit and withdraw",
                    "Make sure withdrawal amount doesn't exceed balance",
                    "Return informative messages for each operation"
                ]
            ),
            Exercise(
                title="Shape Hierarchy",
                description="Create a hierarchy of shapes with a base Shape class and derived classes Circle and Rectangle.",
                starter_code="""import math

class Shape:
    # Add base class implementation
    pass

class Circle(Shape):
    # Add circle implementation
    pass

class Rectangle(Shape):
    # Add rectangle implementation
    pass

# Test your classes
circle = Circle(radius=5)
rectangle = Rectangle(width=4, height=6)

print(f"Circle area: {circle.area()}")
print(f"Rectangle area: {rectangle.area()}")""",
                solution="""import math

class Shape:
    def area(self):
        raise NotImplementedError("Subclass must implement area()")

    def perimeter(self):
        raise NotImplementedError("Subclass must implement perimeter()")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# Test your classes
circle = Circle(radius=5)
rectangle = Rectangle(width=4, height=6)

print(f"Circle area: {circle.area():.2f}")
print(f"Circle perimeter: {circle.perimeter():.2f}")
print(f"Rectangle area: {rectangle.area()}")
print(f"Rectangle perimeter: {rectangle.perimeter()}")""",
                difficulty="Intermediate",
                hints=[
                    "Use abstract methods in the base class",
                    "Remember to import math for pi",
                    "Override area() and perimeter() in each shape",
                    "Use proper initialization in __init__"
                ]
            )
        ],
        best_practices=[
            "Use clear and descriptive class names",
            "Follow the single responsibility principle",
            "Use proper encapsulation with private attributes when needed",
            "Write clear docstrings for classes and methods",
            "Implement special methods (__str__, __repr__) for better object representation",
            "Use inheritance only when there's a clear 'is-a' relationship",
            "Keep class interfaces simple and intuitive"
        ]
    )