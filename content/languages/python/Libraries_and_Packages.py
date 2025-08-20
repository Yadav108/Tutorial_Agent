from content.legacy_models import Topic, Exercise
from content.models import Example

def create() -> Topic:
    """Create and return Python libraries and packages tutorial content."""
    return Topic(
        title="Libraries and Packages",
        description="Learn how to use, install, and manage libraries and packages in Python to extend functionality.",
        content="""
        <h1>Libraries and Packages in Python</h1>
        <p>Python has a vast ecosystem of libraries and packages that make it easier to perform a variety of tasks, from data analysis to machine learning. Understanding how to work with libraries and packages is crucial to leveraging Python's full potential.</p>

        <h2>Installing Packages with pip</h2>
        <p>The Python package installer, pip, is used to install packages from the Python Package Index (PyPI). Use the following command to install packages:</p>
        <code>pip install package_name</code>

        <h2>Importing and Using Libraries</h2>
        <p>Once a library is installed, you can import and use it in your code. Here's a basic example using the popular math library:</p>
        """,
        examples=[
            Example(
                title="Installing and Using a Library",
                code="""
# Install the requests library
# Command (in terminal): pip install requests

import requests

response = requests.get("https://api.example.com/data")
if response.status_code == 200:
    print("Data fetched successfully!")
else:
    print("Failed to fetch data.")
                """,
                explanation="This example demonstrates installing and using the 'requests' library for making HTTP requests. The code fetches data from a URL and checks if the request was successful by examining the status code."
            ),
            Example(
                title="Using the math Library",
                code="""
import math

# Calculate square root
print("Square root of 16 is:", math.sqrt(16))

# Use pi constant
print("Value of pi:", math.pi)
                """,
                explanation="The 'math' library offers a range of mathematical functions. Here, we calculate the square root of 16 and print the value of pi."
            )
        ],
        exercises=[
            Exercise(
                title="Data Fetcher",
                description="Write a program that uses the 'requests' library to fetch JSON data from a provided API endpoint and displays specific information.",
                starter_code="""import requests

def fetch_data(api_url):
    # Use requests to get data from the API
    pass

# Test the function
url = 'https://api.example.com/data'
data = fetch_data(url)
if data:
    print(data)
else:
    print("No data retrieved.")""",
                solution="""import requests

def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()  # Return JSON data if successful
        else:
            print("Failed to retrieve data.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Test the function
url = 'https://api.example.com/data'
data = fetch_data(url)
if data:
    print(data)
else:
    print("No data retrieved.")""",
                difficulty="Intermediate",
                hints=[
                    "Use requests.get() to fetch data from the API.",
                    "Handle potential exceptions using try-except.",
                    "Check the status code to verify a successful response.",
                    "Return the JSON data using response.json()."
                ]
            ),
            Exercise(
                title="CSV Data Processor",
                description="Use the 'pandas' library to read a CSV file of product prices and calculate the average price.",
                starter_code="""import pandas as pd

def calculate_average_price(filename):
    # Use pandas to read the CSV and calculate the average price
    pass

# Test the function
filename = 'products.csv'
average_price = calculate_average_price(filename)
print("Average Price:", average_price)""",
                solution="""import pandas as pd

def calculate_average_price(filename):
    try:
        df = pd.read_csv(filename)
        average_price = df['price'].mean()
        return average_price
    except FileNotFoundError:
        print("File not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Empty data.")
        return None

# Test the function
filename = 'products.csv'
average_price = calculate_average_price(filename)
print("Average Price:", average_price)""",
                difficulty="Intermediate",
                hints=[
                    "Use pd.read_csv() to read the CSV file.",
                    "Calculate the average price using the .mean() method.",
                    "Handle any file-related exceptions properly."
                ]
            )
        ],
        best_practices=[
            "Use pip to install libraries and keep them updated.",
            "Use virtual environments to manage dependencies.",
            "Regularly check for updates to installed packages.",
            "Keep your imports organized and only import what you need.",
            "Use exception handling when working with libraries, especially for network or file I/O operations.",
            "Document the libraries and versions used in your project for reproducibility.",
            "Explore libraries on PyPI (pypi.org) for new functionalities."
        ]
    )
