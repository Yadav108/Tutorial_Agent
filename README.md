# Tutorial Agent - Interactive Programming Learning Platform

🚀 **A comprehensive, modern learning platform for multiple programming languages**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)](https://pypi.org/project/PyQt6/)

An advanced interactive learning platform designed for programming education with support for Python, C++, C#, Java, and JavaScript. Features comprehensive tutorials, interactive code execution, progress tracking, and a modern user interface.

## ✨ Key Features

### 🎓 **Comprehensive Learning Experience**
- **Multi-Language Support**: Python, C++, C#, Java, JavaScript with extensible architecture
- **Structured Learning Paths**: Carefully designed curricula from beginner to advanced
- **Interactive Tutorials**: Step-by-step lessons with practical examples
- **Hands-on Exercises**: Coding challenges with automated validation
- **Quiz System**: Multiple choice, code completion, and interactive assessments

### 💻 **Advanced Code Editor**
- **Professional IDE Experience**: Syntax highlighting, auto-completion, error detection
- **Multi-Language Support**: Language-specific features and tools
- **Code Execution**: Run and test code directly in the application
- **Project Templates**: Quick-start templates for different languages
- **Version Control Integration**: Git support for project management

### 📊 **Progress Tracking & Analytics**
- **Detailed Progress Reports**: Track learning journey across all languages
- **Achievement System**: Unlock badges and milestones
- **Performance Analytics**: Identify strengths and areas for improvement
- **Learning Streaks**: Stay motivated with daily progress tracking
- **Custom Goals**: Set personal learning objectives

### 🎨 **Modern User Interface**
- **Dark/Light Themes**: Customizable appearance with multiple themes
- **Responsive Design**: Optimized for different screen sizes
- **Accessibility**: WCAG-compliant design for inclusive learning
- **Customizable Layout**: Personalize workspace to your preferences
- **Multi-Language UI**: Support for multiple interface languages

## 🚀 Quick Start

### Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (included with Python)
- **Git** - Version control system (optional but recommended)

### Installation Options

#### Option 1: Automated Setup (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Yadav108/tutorial-agent.git
   cd tutorial-agent
   ```

2. **Run the setup script**:
   ```bash
   python setup_project.py
   ```
   
   This will:
   - Check system requirements
   - Create necessary directories
   - Install dependencies
   - Setup default configuration
   - Create placeholder assets
   - Run basic validation tests

3. **Start the application**:
   ```bash
   python run.py
   ```

#### Option 2: Manual Setup

1. **Clone and navigate**:
   ```bash
   git clone https://github.com/Yadav108/tutorial-agent.git
   cd tutorial-agent
   ```

2. **Create virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

### 🎯 First Launch

On first launch, the application will:
- Create user configuration files
- Initialize the database
- Set up default preferences
- Show the welcome tutorial

### 📋 Command Line Options

```bash
# Standard launch
python run.py

# Debug mode with verbose logging
python run.py --debug

# Reset all settings to defaults
python run.py --reset-settings

# Use custom configuration file
python run.py --config /path/to/config.json

# Show version information
python run.py --version

# Show help
python run.py --help
```

## 📁 Enhanced Project Structure

```
Tutorial_Agent/
├── 📋 Project Configuration
│   ├── run.py                    # 🚀 Main application launcher (enhanced)
│   ├── __main__.py              # 🎯 Module entry point
│   ├── setup_project.py         # ⚙️ Automated project setup
│   ├── requirements.txt         # 📦 Dependencies
│   └── .gitignore               # 🚫 Version control exclusions
│
├── 📚 Core Application
│   ├── tutorial_agent/          # 🏗️ Main package
│   │   ├── __init__.py
│   │   ├── core/                # 🧠 Core business logic
│   │   └── services/            # 🔧 Service layer
│   │
│   ├── gui/                     # 🖥️ User Interface
│   │   ├── main_window.py       # 🏠 Main window (enhanced)
│   │   ├── widgets/             # 🧩 Custom UI components
│   │   ├── dialogs/             # 💬 Dialog windows
│   │   └── helpers/             # 🛠️ UI utilities
│   │
│   ├── content/                 # 📖 Learning Content
│   │   ├── models.py            # 🏗️ Enhanced data models
│   │   ├── content_manager.py   # 📚 Content management
│   │   ├── languages/           # 🌐 Language-specific content
│   │   │   ├── python/
│   │   │   ├── javascript/
│   │   │   ├── csharp/
│   │   │   ├── java/
│   │   │   └── cpp/
│   │   └── exercises/           # 💪 Coding exercises
│   │
│   ├── database/                # 🗄️ Data Persistence
│   │   ├── models/              # 📊 Database models
│   │   ├── migrations/          # 🔄 Schema changes
│   │   └── db_handler.py        # 🔧 Database operations
│   │
│   ├── services/                # 🔧 Business Services
│   │   ├── auth_service.py      # 🔐 Authentication
│   │   ├── content_service.py   # 📚 Content delivery
│   │   ├── progress_service.py  # 📊 Progress tracking
│   │   └── quiz_service.py      # ❓ Quiz management
│   │
│   └── utils/                   # 🛠️ Utilities
│       ├── error_handler.py     # 🚨 Enhanced error handling
│       ├── logging_setup.py     # 📝 Logging configuration
│       ├── notifications.py     # 📢 User notifications
│       └── helpers/             # 🧰 Helper functions
│
├── 🎨 Assets & Configuration
│   ├── assets/                  # 🎭 Application assets
│   │   ├── icons/               # 🎯 Language & UI icons
│   │   ├── images/              # 🖼️ Images & graphics
│   │   └── styles/              # 🎨 Themes & styling
│   │
│   ├── config/                  # ⚙️ Configuration
│   │   ├── settings.py          # 📋 Basic settings
│   │   ├── settings_manager.py  # 🔧 Advanced settings management
│   │   ├── constants.py         # 📐 Application constants
│   │   └── default_settings.json
│   │
│   ├── logs/                    # 📝 Application logs
│   ├── cache/                   # 🗄️ Cached data
│   └── data/                    # 💾 User data
│
├── 🧪 Quality Assurance
│   ├── tests/                   # 🧪 Test suite
│   │   ├── test_gui/
│   │   ├── test_services/
│   │   ├── test_utils/
│   │   └── conftest.py
│   │
│   └── docs/                    # 📚 Documentation
│       ├── user_guide/
│       ├── developer_guide/
│       └── api/
│
└── 🚀 Development
    └── venv/                    # 🐍 Python virtual environment
```

### 🏗️ Architecture Highlights

- **🧩 Modular Design**: Cleanly separated concerns with service layers
- **🎯 Type Safety**: Full type hints throughout the codebase
- **🚨 Error Handling**: Comprehensive error handling and user feedback
- **📊 Configuration Management**: Advanced settings with validation
- **🧪 Testing Ready**: Structured for comprehensive testing
- **📝 Logging**: Professional logging with rotation and levels
- **🔧 Extensible**: Easy to add new languages and features

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
