from content.models import Topic, Example, Exercise


def create_async_programming_content() -> Topic:
    """Create and return Async Programming tutorial content."""
    return Topic(
        title="Async Programming",
        description="Learn asynchronous programming in C#, using async and await to write non-blocking code.",
        content="""
        <h1>Async Programming in C#</h1>
        <p>Asynchronous programming allows C# applications to perform tasks without blocking the main thread. This is especially useful for I/O-bound operations like reading from or writing to files, network requests, and database operations, where waiting on responses can slow down the program.</p>

        <h2>Introduction to async and await</h2>
        <p>The <code>async</code> and <code>await</code> keywords make asynchronous programming simpler and more readable in C#. When a method is marked as <code>async</code>, it can use <code>await</code> to pause its execution until an asynchronous operation completes.</p>

        <h3>Key Points:</h3>
        <ul>
            <li><strong>async</strong>: Marks a method as asynchronous.</li>
            <li><strong>await</strong>: Pauses the execution of the method until the awaited task completes.</li>
            <li><strong>Task</strong>: Represents an asynchronous operation that can return a result (via <code>Task&lt;T&gt;</code>) or be void (via <code>Task</code>).</li>
        </ul>

        <h2>Example: Asynchronous Task</h2>
        <p>Here’s an example of a method performing a simulated asynchronous operation:</p>

        <pre><code>using System;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        Console.WriteLine("Starting async operation...");
        await DoSomethingAsync();
        Console.WriteLine("Async operation complete.");
    }

    static async Task DoSomethingAsync()
    {
        await Task.Delay(2000); // Simulate a 2-second delay
        Console.WriteLine("Operation in progress...");
    }
}</code></pre>

        <p>In this example, <code>await Task.Delay(2000)</code> simulates a delay, mimicking an I/O operation. The <code>Main</code> method waits for <code>DoSomethingAsync</code> to complete before continuing.</p>
        """,
        examples=[
            Example(
                title="Basic Async File Read",
                code="""
                using System;
                using System.IO;
                using System.Threading.Tasks;

                class Program
                {
                    static async Task Main()
                    {
                        string content = await ReadFileAsync("sample.txt");
                        Console.WriteLine("File content:\\n" + content);
                    }

                    static async Task<string> ReadFileAsync(string filePath)
                    {
                        using (StreamReader reader = new StreamReader(filePath))
                        {
                            return await reader.ReadToEndAsync();
                        }
                    }
                }
                """,
                explanation="This example demonstrates reading a file asynchronously using `StreamReader.ReadToEndAsync`."
            ),
            Example(
                title="Asynchronous Web Request",
                code="""
                using System;
                using System.Net.Http;
                using System.Threading.Tasks;

                class Program
                {
                    static async Task Main()
                    {
                        string url = "https://example.com";
                        string content = await FetchContentAsync(url);
                        Console.WriteLine("Web content:\\n" + content);
                    }

                    static async Task<string> FetchContentAsync(string url)
                    {
                        using (HttpClient client = new HttpClient())
                        {
                            return await client.GetStringAsync(url);
                        }
                    }
                }
                """,
                explanation="This example shows an asynchronous web request using `HttpClient.GetStringAsync`, allowing the program to fetch data from a URL without blocking."
            )
        ],
        exercises=[
            Exercise(
                title="Create an Async File Write",
                description="Write a program that writes user input to a file asynchronously, then confirms completion.",
                starter_code="""
                using System;
                using System.IO;
                using System.Threading.Tasks;

                class Program
                {
                    static async Task Main()
                    {
                        // Get input from the user
                        Console.Write("Enter text to save to file: ");
                        string userInput = Console.ReadLine();

                        // Call the asynchronous file write method

                        Console.WriteLine("Text has been written to file.");
                    }

                    static async Task WriteToFileAsync(string text)
                    {
                        // Implement asynchronous file write here
                    }
                }
                """,
                solution="""
                using System;
                using System.IO;
                using System.Threading.Tasks;

                class Program
                {
                    static async Task Main()
                    {
                        Console.Write("Enter text to save to file: ");
                        string userInput = Console.ReadLine();

                        await WriteToFileAsync(userInput);

                        Console.WriteLine("Text has been written to file.");
                    }

                    static async Task WriteToFileAsync(string text)
                    {
                        using (StreamWriter writer = new StreamWriter("output.txt"))
                        {
                            await writer.WriteLineAsync(text);
                        }
                    }
                }
                """,
                difficulty="Intermediate",
                hints=[
                    "Use `StreamWriter` to write to a file asynchronously.",
                    "Use `await` to call asynchronous methods."
                ]
            ),
            Exercise(
                title="Implement an Async Counter",
                description="Create an async method that counts down from a specified number, pausing one second between each count.",
                starter_code="""
                using System;
                using System.Threading.Tasks;

                class Program
                {
                    static async Task Main()
                    {
                        Console.Write("Enter countdown start number: ");
                        int startNumber = Convert.ToInt32(Console.ReadLine());

                        // Call the asynchronous countdown method
                    }

                    static async Task CountdownAsync(int start)
                    {
                        // Implement countdown logic here
                    }
                }
                """,
                solution="""
                using System;
                using System.Threading.Tasks;

                class Program
                {
                    static async Task Main()
                    {
                        Console.Write("Enter countdown start number: ");
                        int startNumber = Convert.ToInt32(Console.ReadLine());

                        await CountdownAsync(startNumber);

                        Console.WriteLine("Countdown complete!");
                    }

                    static async Task CountdownAsync(int start)
                    {
                        for (int i = start; i >= 0; i--)
                        {
                            Console.WriteLine(i);
                            await Task.Delay(1000); // Wait for 1 second
                        }
                    }
                }
                """,
                difficulty="Beginner",
                hints=[
                    "Use `for` loop to count down from start to zero.",
                    "Use `Task.Delay(1000)` to wait for one second between counts."
                ]
            )
        ],
        best_practices=[
            "Use async methods for I/O-bound operations like file reads/writes, network requests, or database queries.",
            "Avoid using async void; prefer async Task to allow proper error handling.",
            "Always use await for async operations to ensure they complete before continuing.",
            "Use try-catch to handle exceptions in async methods.",
            "Keep async methods concise; avoid doing CPU-bound work within them."
        ]
    )
