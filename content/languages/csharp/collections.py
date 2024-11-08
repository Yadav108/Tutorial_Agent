from content.models import Topic, Example, Exercise


def create_collections_content() -> Topic:
    """Create and return Collections tutorial content."""
    return Topic(
        title="Collections",
        description="Learn about collections in C#, including lists, dictionaries, queues, and stacks, to manage groups of objects flexibly and efficiently.",
        content="""
        <h1>Collections in C#</h1>
        <p>Collections are data structures that store groups of related objects. C# provides several built-in collections for handling data, each serving different purposes and offering different functionalities.</p>

        <h2>Types of Collections</h2>
        <ul>
            <li><strong>List&lt;T&gt;:</strong> A dynamic array that allows adding and removing elements easily.</li>
            <li><strong>Dictionary&lt;TKey, TValue&gt;:</strong> A collection of key-value pairs, ideal for quick lookups by key.</li>
            <li><strong>Queue&lt;T&gt;:</strong> A first-in, first-out (FIFO) collection.</li>
            <li><strong>Stack&lt;T&gt;:</strong> A last-in, first-out (LIFO) collection.</li>
        </ul>

        <h2>Using List&lt;T&gt;</h2>
        <p>The List&lt;T&gt; class represents a strongly-typed list that can dynamically resize as elements are added or removed. Here's an example:</p>

        <pre><code>using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        List&lt;int&gt; numbers = new List&lt;int&gt;() { 1, 2, 3 };
        numbers.Add(4);
        numbers.Remove(2);
        Console.WriteLine(string.Join(", ", numbers)); // Output: 1, 3, 4
    }
}</code></pre>

        <h2>Using Dictionary&lt;TKey, TValue&gt;</h2>
        <p>The Dictionary&lt;TKey, TValue&gt; class stores key-value pairs, providing efficient lookups by key:</p>

        <pre><code>using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        Dictionary&lt;string, int&gt; ages = new Dictionary&lt;string, int&gt;();
        ages["Alice"] = 30;
        ages["Bob"] = 25;
        Console.WriteLine(ages["Alice"]); // Output: 30
    }
}</code></pre>

        <h2>Using Queue&lt;T&gt;</h2>
        <p>The Queue&lt;T&gt; class represents a FIFO collection where elements are processed in the order they were added:</p>

        <pre><code>using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        Queue&lt;string&gt; tasks = new Queue&lt;string&gt;();
        tasks.Enqueue("Task 1");
        tasks.Enqueue("Task 2");
        Console.WriteLine(tasks.Dequeue()); // Output: Task 1
    }
}</code></pre>

        <h2>Using Stack&lt;T&gt;</h2>
        <p>The Stack&lt;T&gt; class represents a LIFO collection where elements are processed in the reverse order they were added:</p>

        <pre><code>using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        Stack&lt;string&gt; history = new Stack&lt;string&gt;();
        history.Push("Page 1");
        history.Push("Page 2");
        Console.WriteLine(history.Pop()); // Output: Page 2
    }
}</code></pre>
        """,
        examples=[
            Example(
                title="Using List",
                code="""
                using System;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        List<string> fruits = new List<string> { "Apple", "Banana", "Cherry" };
                        fruits.Add("Mango");
                        fruits.Remove("Banana");
                        Console.WriteLine(string.Join(", ", fruits)); // Output: Apple, Cherry, Mango
                    }
                }
                """,
                explanation="This example demonstrates basic operations on a `List` collection: adding and removing elements."
            ),
            Example(
                title="Using Dictionary",
                code="""
                using System;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        Dictionary<string, string> capitals = new Dictionary<string, string>
                        {
                            { "USA", "Washington, D.C." },
                            { "France", "Paris" },
                            { "Japan", "Tokyo" }
                        };
                        capitals["Germany"] = "Berlin";
                        Console.WriteLine(capitals["France"]); // Output: Paris
                    }
                }
                """,
                explanation="This example shows how to add key-value pairs to a `Dictionary` and retrieve values using keys."
            )
        ],
        exercises=[
            Exercise(
                title="Manage a To-Do List with List",
                description="Create a program that maintains a to-do list using `List<string>`. Allow the user to add, remove, and view tasks.",
                starter_code="""
                using System;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        // Initialize a List to hold tasks
                        List<string> tasks = new List<string>();

                        // Sample user actions: add, remove, and view tasks
                    }
                }
                """,
                solution="""
                using System;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        List<string> tasks = new List<string>();

                        tasks.Add("Finish project");
                        tasks.Add("Read book");
                        tasks.Remove("Read book");

                        Console.WriteLine("To-Do List:");
                        Console.WriteLine(string.Join(", ", tasks)); // Output: Finish project
                    }
                }
                """,
                difficulty="Beginner",
                hints=[
                    "Use `Add` to add a task to the list.",
                    "Use `Remove` to delete a task.",
                    "Display tasks with `string.Join()` or a `foreach` loop."
                ]
            ),
            Exercise(
                title="Track Inventory with Dictionary",
                description="Write a program to manage a store inventory using `Dictionary<string, int>`. Allow the user to add items, update quantities, and check stock levels.",
                starter_code="""
                using System;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        // Initialize a Dictionary to hold item quantities
                        Dictionary<string, int> inventory = new Dictionary<string, int>();

                        // Sample user actions: add, update, and check item quantities
                    }
                }
                """,
                solution="""
                using System;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        Dictionary<string, int> inventory = new Dictionary<string, int>
                        {
                            { "Apple", 50 },
                            { "Banana", 30 }
                        };

                        // Update stock
                        inventory["Apple"] += 20;

                        Console.WriteLine($"Apple stock: {inventory["Apple"]}"); // Output: Apple stock: 70
                    }
                }
                """,
                difficulty="Intermediate",
                hints=[
                    "Add items using `dictionary[key] = value`.",
                    "Update quantities by modifying the value for a given key.",
                    "Retrieve values using `dictionary[key]`."
                ]
            )
        ],
        best_practices=[
            "Use `List<T>` for dynamically sized lists where order matters.",
            "Use `Dictionary<TKey, TValue>` for fast lookups with unique keys.",
            "Use `Queue<T>` for FIFO operations and `Stack<T>` for LIFO operations.",
            "Choose the right collection based on the required functionality to improve performance and code readability.",
            "Consider thread-safety if collections will be accessed by multiple threads (e.g., use `ConcurrentDictionary` for thread-safe operations)."
        ]
    )
