qq# Programming Tutorial Agent

An interactive learning platform for multiple programming languages with a focus on Python, C++, C#, and Java.

## Features

- 📚 Interactive tutorials for multiple programming languages
- 💻 Built-in code editor with syntax highlighting
- ✅ Interactive quizzes and assessments
- 📊 Progress tracking and analytics
- 🎯 Achievement system
- 🌙 Light/Dark theme support
- 📱 Responsive design
- 🔄 Auto-save functionality

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

### Setup

1. Clone the repository or download the source code:
```bash
git clone https://github.com/Yadav108/tutorial-agent.git
cd tutorial-agent
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the application:
```bash
python run.py
```

## Project Structure

```
tutorial_agent/
├── requirements.txt        # Project dependencies
├── main.py                # Main application entry point
├── run.py                 # Application launcher
│
├── config/                # Configuration files
│   ├── __init__.py
│   └── settings.py        # Application settings
│
├── database/              # Database handling
│   ├── __init__.py
│   └── db_handler.py      # Database operations
│
├── content/               # Tutorial content
│   ├── python/           # Python tutorials
│   ├── cpp/              # C++ tutorials
│   ├── csharp/           # C# tutorials
│   └── java/             # Java tutorials
│
├── gui/                   # GUI components
│   ├── __init__.py
│   ├── main_window.py    # Main application window
│   ├── sidebar.py        # Navigation sidebar
│   ├── content_viewer.py # Content display
│   ├── code_editor.py    # Code editor
│   └── quiz_widget.py    # Quiz interface
│
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── content_loader.py # Content management
│   └── quiz_handler.py   # Quiz management
│
└── assets/               # Application assets
    ├── images/           # Icons and images
    ├── styles/           # CSS/QSS styles
    └── themes/           # Theme files
```

## Usage

### Navigation

1. Select a programming language from the sidebar
2. Choose a topic from the available tutorials
3. Navigate through subtopics using the content viewer
4. Practice coding in the built-in editor
5. Take quizzes to test your knowledge

### Features

#### Code Editor
- Syntax highlighting
- Auto-completion
- Error detection
- Run code functionality
- Save/Load code snippets

#### Quiz System
- Multiple choice questions
- Immediate feedback
- Progress tracking
- Score history

#### Progress Tracking
- Topic completion status
- Quiz scores
- Time spent
- Achievement badges

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make changes and commit (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## Content Structure

### Tutorial Format
Tutorials are organized in JSON format:
```json
{
    "language": "Python",
    "level": "Basics",
    "topics": [
        {
            "id": "introduction",
            "title": "Introduction to Python",
            "content": "...",
            "subtopics": [...],
            "examples": [...],
            "quiz": [...]
        }
    ]
}
```

### Adding New Content
1. Create a new JSON file in the appropriate language directory
2. Follow the content structure format
3. Add necessary code examples and quiz questions
4. Update the content index

## Development

### Building from Source
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
pylint tutorial_agent/

# Format code
black tutorial_agent/
```

### Creating Custom Themes
1. Create a new QSS file in `assets/themes/`
2. Follow the existing theme structure
3. Add theme to settings

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Check Python version
   - Verify all dependencies are installed
   - Check log files in `logs/`

2. **Database errors**
   - Ensure write permissions
   - Check database connection
   - Verify schema integrity

3. **Content not loading**
   - Check content file format
   - Verify file permissions
   - Check content path in settings

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with PyQt6
- Syntax highlighting by Pygments
- Markdown support by python-markdown
- Icons from Lucide

## Contact

For support or queries:
- Email: yadavaryan2073@gmail.com
- GitHub Issues: [Create an issue](https://github.com/Yadav108/tutorial-agent/issues)
