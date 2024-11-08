from content.models import Topic, Example, Exercise


def create_file_io_content() -> Topic:
    """Create and return File I/O tutorial content."""
    return Topic(
        title="File I/O (Input/Output)",
        description="Learn how to work with files in C#, including reading from and writing to files using the System.IO namespace.",
        content="""
        <h1>File I/O in C#</h1>
        <p>File I/O (Input/Output) operations allow you to read from and write data to files. C# provides various classes for handling files through the <code>System.IO</code> namespace, including <code>File</code>, <code>StreamReader</code>, and <code>StreamWriter</code>.</p>

        <h2>Basic File I/O Operations</h2>
        <ul>
            <li><strong>Reading a file:</strong> Use <code>File.ReadAllText</code> or <code>StreamReader</code> to read text from a file.</li>
            <li><strong>Writing to a file:</strong> Use <code>File.WriteAllText</code> or <code>StreamWriter</code> to write text to a file.</li>
            <li><strong>Appending to a file:</strong> Use <code>File.AppendAllText</code> or <code>StreamWriter</code> in append mode.</li>
        </ul>

        <h2>Example: Reading and Writing Files</h2>
        <p>Here's a basic example of reading from and writing to a file using <code>File</code> class methods:</p>

        <pre><code>using System;
using System.IO;

class Program
{
    static void Main()
    {
        // Writing to a file
        string text = "Hello, this is a sample text.";
        File.WriteAllText("example.txt", text);

        // Reading from a file
        string readText = File.ReadAllText("example.txt");
        Console.WriteLine("File content: " + readText);
    }
}</code></pre>

        <h2>Using StreamReader and StreamWriter</h2>
        <p>The <code>StreamReader</code> and <code>StreamWriter</code> classes offer more control over file reading and writing, particularly for larger files or line-by-line reading.</p>

        <pre><code>using System;
using System.IO;

class Program
{
    static void Main()
    {
        // Writing to a file using StreamWriter
        using (StreamWriter writer = new StreamWriter("example.txt"))
        {
            writer.WriteLine("This is line 1.");
            writer.WriteLine("This is line 2.");
        }

        // Reading from a file using StreamReader
        using (StreamReader reader = new StreamReader("example.txt"))
        {
            string line;
            while ((line = reader.ReadLine()) != null)
            {
                Console.WriteLine(line);
            }
        }
    }
}</code></pre>
        """,
        examples=[
            Example(
                title="Reading All Text from a File",
                code="""
                using System;
                using System.IO;

                class Program
                {
                    static void Main()
                    {
                        // Read the entire content of a file
                        string content = File.ReadAllText("sample.txt");
                        Console.WriteLine("File content: " + content);
                    }
                }
                """,
                explanation="This example shows how to read all text from a file using `File.ReadAllText`."
            ),
            Example(
                title="Writing and Appending Text to a File",
                code="""
                using System;
                using System.IO;

                class Program
                {
                    static void Main()
                    {
                        // Writing to a file
                        File.WriteAllText("sample.txt", "This is the first line.");

                        // Appending to a file
                        File.AppendAllText("sample.txt", "\\nThis is an appended line.");
                    }
                }
                """,
                explanation="This example demonstrates how to write to a file with `File.WriteAllText` and then append more text with `File.AppendAllText`."
            )
        ],
        exercises=[
            Exercise(
                title="Create and Read a Log File",
                description="Create a program that writes log messages to a file and reads them back. Each log entry should include a timestamp.",
                starter_code="""
                using System;
                using System.IO;

                class Program
                {
                    static void Main()
                    {
                        // File path for the log file
                        string filePath = "log.txt";

                        // Add a log entry with timestamp

                        // Read all log entries from the file

                    }
                }
                """,
                solution="""
                using System;
                using System.IO;

                class Program
                {
                    static void Main()
                    {
                        string filePath = "log.txt";

                        // Write a log entry
                        string logEntry = DateTime.Now + " - Log entry created.";
                        File.AppendAllText(filePath, logEntry + "\\n");

                        // Read all log entries
                        string logContent = File.ReadAllText(filePath);
                        Console.WriteLine("Log File Content:\\n" + logContent);
                    }
                }
                """,
                difficulty="Intermediate",
                hints=[
                    "Use `DateTime.Now` for the timestamp.",
                    "Use `File.AppendAllText` to add each log entry.",
                    "Read the log content with `File.ReadAllText`."
                ]
            ),
            Exercise(
                title="Count Lines in a File",
                description="Create a program that counts and displays the number of lines in a given text file.",
                starter_code="""
                using System;
                using System.IO;

                class Program
                {
                    static void Main()
                    {
                        // Path to the file to be read
                        string filePath = "sample.txt";

                        // Count lines in the file

                        // Display line count

                    }
                }
                """,
                solution="""
                using System;
                using System.IO;

                class Program
                {
                    static void Main()
                    {
                        string filePath = "sample.txt";
                        int lineCount = 0;

                        // Count lines using StreamReader
                        using (StreamReader reader = new StreamReader(filePath))
                        {
                            while (reader.ReadLine() != null)
                            {
                                lineCount++;
                            }
                        }

                        Console.WriteLine("Total lines: " + lineCount);
                    }
                }
                """,
                difficulty="Intermediate",
                hints=[
                    "Use `StreamReader` to read each line one at a time.",
                    "Increment a counter for each line read."
                ]
            )
        ],
        best_practices=[
            "Use `using` statements to ensure proper disposal of file streams.",
            "Always check if a file exists before attempting to read it.",
            "Consider using `File.AppendAllText` for log files to avoid overwriting existing data.",
            "Use `try-catch` blocks for exception handling, especially when dealing with file paths and permissions.",
            "Use `StreamReader` and `StreamWriter` for reading/writing large files or when needing line-by-line processing."
        ]
    )
