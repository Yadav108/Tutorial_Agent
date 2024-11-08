# File: Tutorial_Agent/setup.py

from setuptools import setup, find_packages

setup(
    name="tutorial_agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'PyQt6>=6.0.0',
        'SQLAlchemy>=1.4.0',
        'markdown>=3.3.0',
        'pygments>=2.10.0',
    ],
    author="Aryan Yadav",
    author_email="yadavaryan2073@gmail.com",
    description="A comprehensive programming tutorial platform",
    keywords="programming, tutorials, education",
    project_urls={
        "Source": "https://github.com/yourusername/tutorial_agent",
    },
    python_requires='>=3.8',
)
