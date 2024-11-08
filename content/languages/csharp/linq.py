from content.models import Topic, Example, Exercise


def create_linq_content() -> Topic:
    """Create and return LINQ tutorial content."""
    return Topic(
        title="LINQ (Language Integrated Query)",
        description="Learn how to use LINQ in C# to query and manipulate data collections efficiently and concisely.",
        content="""
        <h1>LINQ (Language Integrated Query)</h1>
        <p>LINQ (Language Integrated Query) is a powerful feature in C# that allows you to query collections of data using a query syntax similar to SQL. LINQ can be used with various data sources, such as collections, XML, and databases.</p>

        <h2>Basic LINQ Syntax</h2>
        <p>LINQ offers two main syntaxes: query syntax and method syntax. The query syntax is similar to SQL, while the method syntax uses lambda expressions.</p>

        <h3>Query Syntax Example</h3>
        <pre><code>using System;
using System.Linq;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        List&lt;int&gt; numbers = new List&lt;int&gt;() { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        var evenNumbers = from number in numbers
                          where number % 2 == 0
                          select number;

        Console.WriteLine("Even Numbers: " + string.Join(", ", evenNumbers)); // Output: 2, 4, 6, 8
    }
}</code></pre>

        <h3>Method Syntax Example</h3>
        <pre><code>using System;
using System.Linq;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        List&lt;int&gt; numbers = new List&lt;int&gt;() { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        var evenNumbers = numbers.Where(number => number % 2 == 0);

        Console.WriteLine("Even Numbers: " + string.Join(", ", evenNumbers)); // Output: 2, 4, 6, 8
    }
}</code></pre>

        <h2>Common LINQ Operations</h2>
        <ul>
            <li><strong>Where:</strong> Filters elements based on a condition.</li>
            <li><strong>Select:</strong> Projects each element into a new form.</li>
            <li><strong>OrderBy:</strong> Sorts elements in ascending order.</li>
            <li><strong>OrderByDescending:</strong> Sorts elements in descending order.</li>
            <li><strong>GroupBy:</strong> Groups elements that share a common attribute.</li>
            <li><strong>Sum, Max, Min, Average:</strong> Aggregation functions.</li>
        </ul>

        <h2>Example: Filtering and Sorting with LINQ</h2>
        <p>Here’s how to filter and sort a collection with LINQ:</p>

        <pre><code>using System;
using System.Linq;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        List&lt;string&gt; names = new List&lt;string&gt;() { "John", "Anna", "Kyle", "Zara", "Emily" };
        var filteredNames = names.Where(name => name.StartsWith("A"))
                                 .OrderBy(name => name);

        Console.WriteLine("Names starting with 'A': " + string.Join(", ", filteredNames)); // Output: Anna
    }
}</code></pre>
        """,
        examples=[
            Example(
                title="Using LINQ to Find Even Numbers",
                code="""
                using System;
                using System.Linq;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
                        var evenNumbers = numbers.Where(n => n % 2 == 0);
                        Console.WriteLine("Even Numbers: " + string.Join(", ", evenNumbers)); // Output: 2, 4, 6, 8, 10
                    }
                }
                """,
                explanation="This example demonstrates filtering a list to find even numbers using LINQ's `Where` method."
            ),
            Example(
                title="Grouping Data with LINQ",
                code="""
                using System;
                using System.Linq;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        List<string> fruits = new List<string> { "Apple", "Banana", "Cherry", "Avocado", "Blueberry" };
                        var groupedFruits = fruits.GroupBy(f => f[0]);

                        foreach (var group in groupedFruits)
                        {
                            Console.WriteLine($"Fruits that start with '{group.Key}': " + string.Join(", ", group));
                        }
                    }
                }
                """,
                explanation="This example shows how to group a list of fruits by the first letter using the `GroupBy` method."
            )
        ],
        exercises=[
            Exercise(
                title="Find High Scores",
                description="Create a program that filters a list of scores to find only those greater than 80, then sorts them in descending order.",
                starter_code="""
                using System;
                using System.Linq;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        // Sample list of scores
                        List<int> scores = new List<int> { 60, 85, 90, 75, 95, 88, 70 };

                        // Filter and sort high scores using LINQ
                    }
                }
                """,
                solution="""
                using System;
                using System.Linq;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        List<int> scores = new List<int> { 60, 85, 90, 75, 95, 88, 70 };
                        var highScores = scores.Where(score => score > 80)
                                               .OrderByDescending(score => score);
                        Console.WriteLine("High Scores: " + string.Join(", ", highScores)); // Output: 95, 90, 88, 85
                    }
                }
                """,
                difficulty="Intermediate",
                hints=[
                    "Use `Where` to filter scores above 80.",
                    "Use `OrderByDescending` to sort scores in descending order."
                ]
            ),
            Exercise(
                title="Project Data with LINQ",
                description="Create a program that transforms a list of names into uppercase letters using LINQ's `Select` method.",
                starter_code="""
                using System;
                using System.Linq;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        // Sample list of names
                        List<string> names = new List<string> { "Alice", "Bob", "Charlie", "Diana" };

                        // Transform names to uppercase using LINQ
                    }
                }
                """,
                solution="""
                using System;
                using System.Linq;
                using System.Collections.Generic;

                class Program
                {
                    static void Main()
                    {
                        List<string> names = new List<string> { "Alice", "Bob", "Charlie", "Diana" };
                        var upperCaseNames = names.Select(name => name.ToUpper());
                        Console.WriteLine("Uppercase Names: " + string.Join(", ", upperCaseNames)); // Output: ALICE, BOB, CHARLIE, DIANA
                    }
                }
                """,
                difficulty="Beginner",
                hints=[
                    "Use `Select` to transform each name to uppercase.",
                    "Use `ToUpper` on each string element to convert it."
                ]
            )
        ],
        best_practices=[
            "Use LINQ for concise, readable data manipulation.",
            "Choose query or method syntax based on readability and preference.",
            "Use LINQ with collections like List, Dictionary, or arrays for streamlined data operations.",
            "Avoid complex LINQ queries that may hinder readability; consider refactoring them into multiple queries.",
            "Use `GroupBy` for grouping data, `Select` for projection, and `Where` for filtering conditions.",
            "Test LINQ queries on smaller data sets to ensure they work as expected."
        ]
    )
