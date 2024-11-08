# gui/main_window.py

import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QToolBar, QStatusBar, QSplitter, QSizePolicy,
    QLabel, QMessageBox, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer, QSize
from PyQt6.QtGui import QAction, QIcon, QPixmap

from .widgets import (
    LanguageCard,
    ContentViewer,
    CodeEditor,
    ProgressViewer,
    SearchBar
)
from .dialogs import SettingsDialog, TutorialDialog
from content.models import Topic, Language
from content import ContentManager

logger = logging.getLogger('TutorialAgent')


class WelcomeScreen(QWidget):
    """Welcome screen widget shown before language selection."""

    get_started = pyqtSignal()  # Signal to indicate user wants to start

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Initialize welcome screen UI."""
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QLabel#welcomeLabel {
                color: #2c3e50;
                font-size: 32px;
                font-weight: bold;
            }
            QLabel#instructionLabel {
                color: #7f8c8d;
                font-size: 18px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo or icon (if exists)
        try:
            logo_path = str(Path(__file__).parent.parent / 'assets' / 'icons' / 'logo.png')
            if Path(logo_path).exists():
                logo_label = QLabel()
                logo_label.setPixmap(QPixmap(logo_path).scaled(
                    100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                ))
                layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            logger.warning(f"Could not load logo: {str(e)}")

        # Welcome message
        welcome_label = QLabel("Welcome to Tutorial Agent")
        welcome_label.setObjectName("welcomeLabel")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        # Instructions
        instruction_label = QLabel(
            "Start your programming journey by selecting a language from the sidebar."
            "\nOur interactive tutorials will guide you through the learning process."
        )
        instruction_label.setObjectName("instructionLabel")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instruction_label)

        # Get started button
        self.start_button = QPushButton("Get Started")
        self.start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_button.setFixedWidth(200)
        self.start_button.clicked.connect(self.get_started.emit)
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        try:
            logger.debug("Initializing MainWindow")
            self.setWindowTitle("Programming Tutorial Agent")
            self.setMinimumSize(1200, 800)

            # Initialize member variables
            self.current_language = None
            self.language_cards = {}

            # Initialize content manager
            content_dir = Path(__file__).parent.parent / 'content'
            self.content_manager = ContentManager(content_dir)

            # Setup UI
            self.init_ui()

            self.debug_content_loading()

            # Show welcome tutorial with slight delay
            QTimer.singleShot(100, self.show_welcome_tutorial)

            logger.debug("MainWindow initialization complete")

        except Exception as e:
            logger.error(f"Error initializing MainWindow: {str(e)}", exc_info=True)
            raise

    def init_ui(self):
        """Initialize the user interface."""
        try:
            # Create central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QHBoxLayout(central_widget)
            main_layout.setSpacing(0)
            main_layout.setContentsMargins(0, 0, 0, 0)

            # Setup components
            self.setup_toolbar()
            self.setup_statusbar()

            # Create main splitter
            self.main_splitter = QSplitter(Qt.Orientation.Horizontal)

            # Add sidebar
            sidebar = self.create_sidebar()
            self.main_splitter.addWidget(sidebar)

            # Create content stack
            self.content_stack = QStackedWidget()

            # Add welcome screen
            self.welcome_screen = WelcomeScreen()
            self.welcome_screen.get_started.connect(self.on_get_started)
            self.content_stack.addWidget(self.welcome_screen)

            # Add main content area
            self.content_area = self.create_content_area()
            self.content_stack.addWidget(self.content_area)

            self.main_splitter.addWidget(self.content_stack)

            # Set splitter proportions
            self.main_splitter.setStretchFactor(0, 1)  # Sidebar
            self.main_splitter.setStretchFactor(1, 3)  # Content area

            main_layout.addWidget(self.main_splitter)

            # Show welcome screen by default
            self.content_stack.setCurrentWidget(self.welcome_screen)

            logger.debug("UI initialization complete")

        except Exception as e:
            logger.error(f"Error initializing UI: {str(e)}", exc_info=True)
            raise

    def setup_toolbar(self):
        """Setup the main toolbar."""
        try:
            toolbar = QToolBar()
            toolbar.setMovable(False)
            toolbar.setIconSize(QSize(20, 20))
            toolbar.setStyleSheet("""
                QToolBar {
                    spacing: 5px;
                    background: white;
                    border-bottom: 1px solid #dcdde1;
                    padding: 5px 10px;
                }
                QToolButton {
                    background: transparent;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                }
                QToolButton:hover {
                    background: #f5f6fa;
                }
            """)

            # Add search bar
            self.search_bar = SearchBar()
            self.search_bar.search_triggered.connect(self.on_search)
            toolbar.addWidget(self.search_bar)

            # Add spacer
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            toolbar.addWidget(spacer)

            # Add actions
            actions = [
                ("refresh", "Refresh", self.refresh_content),
                ("settings", "Settings", self.show_settings),
                ("help", "Help", self.show_help),
            ]

            for action_id, text, slot in actions:
                action = QAction(QIcon(f"assets/icons/{action_id}.png"), text, self)
                action.triggered.connect(slot)
                toolbar.addAction(action)

            self.addToolBar(toolbar)
            logger.debug("Toolbar setup complete")

        except Exception as e:
            logger.error(f"Error setting up toolbar: {str(e)}", exc_info=True)
            raise

    def setup_statusbar(self):
        """Setup the status bar."""
        try:
            status_bar = QStatusBar()
            status_bar.setStyleSheet("""
                QStatusBar {
                    background: white;
                    border-top: 1px solid #dcdde1;
                }
                QStatusBar::item {
                    border: none;
                }
                QLabel {
                    color: #2c3e50;
                }
            """)

            # Add status label
            self.status_label = QLabel("Ready")
            status_bar.addPermanentWidget(self.status_label)

            self.setStatusBar(status_bar)
            logger.debug("Status bar setup complete")

        except Exception as e:
            logger.error(f"Error setting up status bar: {str(e)}", exc_info=True)
            raise



    def create_content_area(self):
        """Create the main content area with content viewer and code editor."""
        try:
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setSpacing(0)

            # Create vertical splitter for content viewer and code editor
            content_splitter = QSplitter(Qt.Orientation.Vertical)

            # Add content viewer
            self.content_viewer = ContentViewer()
            self.content_viewer.run_example.connect(self.run_code)
            self.content_viewer.start_exercise.connect(self.start_exercise)
            content_splitter.addWidget(self.content_viewer)

            # Add code editor
            self.code_editor = CodeEditor()
            self.code_editor.code_executed.connect(self.handle_code_execution)
            content_splitter.addWidget(self.code_editor)

            # Set splitter proportions
            content_splitter.setStretchFactor(0, 2)  # Content viewer
            content_splitter.setStretchFactor(1, 1)  # Code editor

            content_layout.addWidget(content_splitter)

            # Style the content area
            content_widget.setStyleSheet("""
                QWidget {
                    background-color: white;
                }
            """)

            logger.debug("Content area creation complete")
            return content_widget

        except Exception as e:
            logger.error(f"Error creating content area: {str(e)}", exc_info=True)
            raise

    def create_sidebar(self):
        """Create the sidebar containing language cards and progress viewer."""
        try:
            logger.debug("Creating sidebar")
            sidebar = QWidget()
            sidebar.setMaximumWidth(350)
            sidebar.setMinimumWidth(250)
            sidebar_layout = QVBoxLayout(sidebar)
            sidebar_layout.setContentsMargins(10, 10, 10, 10)
            sidebar_layout.setSpacing(10)

            # Get available languages from content manager
            languages = self.content_manager.get_all_languages()
            logger.debug(f"Found {len(languages)} languages")

            if not languages:
                logger.warning("No languages found in content manager")
                # Add a message to the sidebar
                message = QLabel("No programming languages available.\nPlease check content directory.")
                message.setStyleSheet("""
                    QLabel {
                        color: #666;
                        padding: 20px;
                        text-align: center;
                    }
                """)
                message.setWordWrap(True)
                sidebar_layout.addWidget(message)
            else:
                # Create language cards
                for lang_id, language in languages.items():
                    try:
                        logger.debug(f"Creating card for language: {language.name}")
                        card = LanguageCard(
                            language=language.name,
                            description=language.description[:100] + "...",  # Truncate long descriptions
                            icon=f"assets/icons/{language.icon}",
                            color=language.color
                        )
                        card.clicked.connect(self.on_language_selected)
                        sidebar_layout.addWidget(card)
                        self.language_cards[language.name] = card
                        logger.debug(f"Created language card for {language.name}")
                    except Exception as e:
                        logger.error(f"Error creating card for {language.name}: {str(e)}", exc_info=True)

            # Add progress viewer
            self.progress_viewer = ProgressViewer()
            sidebar_layout.addWidget(self.progress_viewer)

            # Add stretcher at the bottom
            sidebar_layout.addStretch()

            # Style the sidebar
            sidebar.setStyleSheet("""
                QWidget {
                    background-color: #f5f6fa;
                }
            """)

            logger.info(f"Created sidebar with {len(self.language_cards)} language cards")
            return sidebar

        except Exception as e:
            logger.error(f"Error creating sidebar: {str(e)}", exc_info=True)
            raise

    def _load_languages(self):
        """Load languages from the content manager."""
        try:
            languages = self.content_manager.get_all_languages()
            logger.debug(f"Loading {len(languages)} languages")
            for lang_id, language in languages.items():
                logger.debug(f"Found language: {language.name}")
            return languages
        except Exception as e:
            logger.error(f"Error loading languages: {str(e)}", exc_info=True)
            return {}

    def on_get_started(self):
        """Handle Get Started button click."""
        try:
            logger.debug("Get Started clicked")
            # Show first language tutorial if available
            if self.language_cards:
                first_language = next(iter(self.language_cards.keys()))
                self.on_language_selected(first_language)
            else:
                logger.warning("No language cards available")
                QMessageBox.warning(
                    self,
                    "No Languages Available",
                    "No programming languages are currently available. Please check your content directory."
                )
        except Exception as e:
            logger.error(f"Error handling get started: {str(e)}", exc_info=True)

    @pyqtSlot(str)
    def on_language_selected(self, language):
        """Handle language selection."""
        try:
            logger.debug(f"Language selected: {language}")
            self.current_language = language

            # Update sidebar cards
            for lang, card in self.language_cards.items():
                card.setSelected(lang == language)

            # Switch to content area if on welcome screen
            if self.content_stack.currentWidget() == self.welcome_screen:
                self.content_stack.setCurrentWidget(self.content_area)

            # Get language content from content manager
            language_data = None
            for lang_id, lang_obj in self.content_manager.get_all_languages().items():
                if lang_obj.name.lower() == language.lower():
                    language_data = lang_obj
                    break

            if language_data:
                # Format the content for the content viewer
                viewer_data = {
                    'title': language_data.name,
                    'description': language_data.description,
                    'topics': [
                        {
                            'title': topic.title,
                            'description': topic.description,
                            'content': topic.content,
                            'examples': topic.examples,
                            'exercises': topic.exercises
                        } for topic in language_data.topics
                    ]
                }

                # Update content viewer with the language data
                self.content_viewer.load_content(viewer_data)

                # Update code editor
                self.code_editor.set_language(language)

                # Update progress viewer
                # Create a dictionary of topic names and their progress
                topic_progress = {
                    topic.title: 0 for topic in language_data.topics
                }
                completed_topics = self.content_manager.user_progress.get(language, {}).get('completed_topics', [])
                for topic_id in completed_topics:
                    for topic in language_data.topics:
                        if topic.id == topic_id:
                            topic_progress[topic.title] = 100
                            break

                self.progress_viewer.update_progress(language, topic_progress)

                # Calculate overall progress
                total_topics = len(language_data.topics)
                completed_count = len(completed_topics)
                overall_progress = (completed_count / total_topics * 100) if total_topics > 0 else 0

                # Update card progress
                if language in self.language_cards:
                    self.language_cards[language].set_progress(int(overall_progress))

                # Update status bar
                self.status_label.setText(f"Loaded {language} content successfully")
                logger.debug(f"Successfully loaded content for {language}")

            else:
                raise ValueError(f"No content found for language: {language}")

        except Exception as e:
            logger.error(f"Error handling language selection: {str(e)}", exc_info=True)
            # Load fallback content
            logger.debug("Loading fallback content")
            fallback_content = self._get_fallback_content(language)
            self.content_viewer.load_content(fallback_content)
            self.code_editor.set_language(language)
            self.status_label.setText(f"Loaded basic content for {language}")

    def _get_hello_world_code(self, language: str) -> str:
        """Get Hello World example for different languages."""
        examples = {
            "Python": 'print("Hello, World!")',
            "JavaScript": 'console.log("Hello, World!");',
            "Java": '''public class HelloWorld {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
        }
    }''',
            "C#": '''using System;
    class Program {
        static void Main() {
            Console.WriteLine("Hello, World!");
        }
    }''',
            "C++": '''#include <iostream>
    int main() {
        std::cout << "Hello, World!" << std::endl;
        return 0;
    }'''
        }
        return examples.get(language, 'print("Hello, World!")')

    def _get_starter_code(self, language: str) -> str:
        """Get starter code for different languages."""
        starters = {
            "Python": '''# Write a program that prints your name
    name = "Your Name"

    # Print a greeting
    print(f"Hello, {name}!")''',

            "JavaScript": '''// Write a program that prints your name
    const name = "Your Name";

    // Print a greeting
    console.log(`Hello, ${name}!`);''',

            "Java": '''public class Exercise {
        public static void main(String[] args) {
            // Write a program that prints your name
            String name = "Your Name";

            // Print a greeting
            System.out.println("Hello, " + name + "!");
        }
    }''',

            "C#": '''using System;

    class Program {
        static void Main() {
            // Write a program that prints your name
            string name = "Your Name";

            // Print a greeting
            Console.WriteLine($"Hello, {name}!");
        }
    }''',

            "C++": '''#include <iostream>
    #include <string>

    int main() {
        // Write a program that prints your name
        std::string name = "Your Name";

        // Print a greeting
        std::cout << "Hello, " << name << "!" << std::endl;
        return 0;
    }'''
        }
        return starters.get(language, '# Write your code here\n')

    def debug_content(self):
        """Print debug information about current content."""
        try:
            logger.debug("\n=== Content Debug Information ===")
            logger.debug(f"Current Language: {self.current_language}")

            # Check content manager
            logger.debug("\nContent Manager:")
            logger.debug(f"Available languages: {list(self.content_manager.get_all_languages().keys())}")

            # Check language content
            if self.current_language:
                for lang_id, lang_obj in self.content_manager.get_all_languages().items():
                    if lang_obj.name.lower() == self.current_language.lower():
                        logger.debug(f"\nLanguage Details for {lang_obj.name}:")
                        logger.debug(f"Description: {lang_obj.description}")
                        logger.debug(f"Number of topics: {len(lang_obj.topics)}")

                        for i, topic in enumerate(lang_obj.topics):
                            logger.debug(f"\nTopic {i + 1}: {topic.title}")
                            logger.debug(f"Description: {topic.description}")
                            logger.debug(f"Has content: {bool(topic.content)}")
                            logger.debug(f"Number of examples: {len(topic.examples)}")
                            logger.debug(f"Number of exercises: {len(topic.exercises)}")
                        break

            logger.debug("\n=============================")

        except Exception as e:
            logger.error(f"Error in debug_content: {str(e)}", exc_info=True)

    def _get_fallback_content(self, language: str) -> dict:
        """Get fallback content when actual content cannot be loaded."""
        return {
            'title': f'Introduction to {language}',
            'description': f'Learn the basics of {language} programming',
            'estimated_time': 30,
            'content': f"""# Welcome to {language}

    Let's start learning {language}! This tutorial will guide you through:

    ## Basic Concepts
    - Syntax and basic operations
    - Variables and data types
    - Control structures
    - Functions and modules

    ## What you'll learn
    - How to write basic {language} programs
    - Best practices and coding standards
    - Problem-solving techniques
    - Real-world applications
    """,
            'examples': [
                {
                    'title': 'Hello World',
                    'code': self._get_hello_world_code(language),
                    'explanation': 'Your first program - printing "Hello, World!" to the console.'
                }
            ],
            'exercises': [
                {
                    'title': 'Basic Syntax Practice',
                    'description': 'Write a program that prints your name and declares a variable.',
                    'difficulty': 'Beginner',
                    'starter_code': self._get_starter_code(language)
                }
            ]
        }

    def show_welcome_tutorial(self):
        """Show welcome tutorial on first launch."""
        try:
            welcome_tutorial = {
                'id': 'welcome',
                'title': 'Welcome to Tutorial Agent',
                'steps': [
                    {
                        'number': 1,
                        'title': 'Welcome',
                        'content': 'Welcome to Tutorial Agent! Let\'s take a quick tour to help you get started.',
                        'tip': 'You can skip this tutorial and access it later from the help menu.'
                    },
                    {
                        'number': 2,
                        'title': 'Choose a Language',
                        'content': 'Start by selecting a programming language from the sidebar. Each card shows the language and its description.',
                        'tip': 'Click any language card to begin learning.'
                    },
                    {
                        'number': 3,
                        'title': 'Learning Interface',
                        'content': 'The main area shows tutorials, examples, and exercises. You can write and test code in the built-in editor.',
                        'tip': 'Use the tabs to switch between different types of content.'
                    },
                    {
                        'number': 4,
                        'title': 'Track Progress',
                        'content': 'Your learning progress is tracked automatically. View your progress in the sidebar below the language cards.',
                        'tip': 'Complete exercises to earn points and track your mastery.'
                    },
                    {
                        'number': 5,
                        'title': 'Ready to Start',
                        'content': 'You\'re all set! Choose a language to begin your programming journey.',
                        'tip': 'Remember to save your code and track your progress!'
                    }
                ]
            }

            TutorialDialog.show_tutorial(self, 'welcome', welcome_tutorial)

        except Exception as e:
            logger.error(f"Error showing welcome tutorial: {str(e)}", exc_info=True)

    def show_language_tutorial(self, language: str):
        """Show tutorial for selected language."""
        try:
            # Get language info from content manager
            language_content = self.content_manager.get_language(language)

            language_tutorial = {
                'id': f'{language.lower()}-intro',
                'title': f'Getting Started with {language}',
                'steps': [
                    {
                        'number': 1,
                        'title': f'Welcome to {language}',
                        'content': language_content.description,
                    },
                    {
                        'number': 2,
                        'title': 'Learning Path',
                        'content': 'Follow our structured learning path:\n' +
                                   '\n'.join(f'- {topic}' for topic in language_content.learning_path),
                    },
                    {
                        'number': 3,
                        'title': 'Interactive Learning',
                        'content': 'Practice with interactive examples and exercises. Write and test code in the editor.',
                    },
                    {
                        'number': 4,
                        'title': 'Getting Help',
                        'content': 'Use the help menu or click the help icon for assistance.',
                    }
                ]
            }

            TutorialDialog.show_tutorial(self, f'{language.lower()}-intro', language_tutorial)

        except Exception as e:
            logger.error(f"Error showing language tutorial: {str(e)}", exc_info=True)

    def run_code(self, code: str):
        """Execute code in the editor."""
        try:
            self.code_editor.set_code(code)
            self.code_editor.run_code()
        except Exception as e:
            logger.error(f"Error running code: {str(e)}", exc_info=True)

    def handle_code_execution(self, success: bool, output: str):
        """Handle code execution results."""
        try:
            if success:
                self.status_label.setText("Code executed successfully")
            else:
                self.status_label.setText("Code execution failed")
        except Exception as e:
            logger.error(f"Error handling code execution: {str(e)}", exc_info=True)

    def start_exercise(self, exercise_data: dict):
        """Start a coding exercise."""
        try:
            self.code_editor.set_code(exercise_data.get('starter_code', ''))
            self.status_label.setText(f"Started exercise: {exercise_data['title']}")
        except Exception as e:
            logger.error(f"Error starting exercise: {str(e)}", exc_info=True)

    def on_search(self, query: str):
        """Handle search queries."""
        try:
            # Implement search functionality using content manager
            results = self.content_manager.search(query)
            # Update UI with search results
            self.status_label.setText(f"Found {len(results)} results")
        except Exception as e:
            logger.error(f"Error performing search: {str(e)}", exc_info=True)

    def refresh_content(self):
        """Refresh current content."""
        try:
            if self.current_language:
                self.on_language_selected(self.current_language)
            self.status_label.setText("Content refreshed")
        except Exception as e:
            logger.error(f"Error refreshing content: {str(e)}", exc_info=True)

    def debug_content_loading(self):
        """Debug content loading issues."""
        try:
            logger.debug("Debugging content loading...")

            # Check content manager initialization
            logger.debug(f"Content manager initialized: {self.content_manager is not None}")

            # Check available languages
            languages = self.content_manager.get_all_languages()
            logger.debug(f"Available languages: {list(languages.keys())}")

            # Check each language's content
            for lang_id, language in languages.items():
                logger.debug(f"\nChecking language: {lang_id}")
                logger.debug(f"Name: {language.name}")
                logger.debug(f"Topics count: {len(language.topics)}")

                for i, topic in enumerate(language.topics):
                    logger.debug(f"\nTopic {i + 1}: {topic.title}")
                    logger.debug(f"Has content: {bool(topic.content)}")
                    logger.debug(f"Examples count: {len(topic.examples)}")
                    logger.debug(f"Exercises count: {len(topic.exercises)}")

        except Exception as e:
            logger.error(f"Error during content debug: {str(e)}", exc_info=True)

    def show_settings(self):
        """Show settings dialog."""
        try:
            dialog = SettingsDialog(self)
            if dialog.exec():
                # Handle settings changes
                self.status_label.setText("Settings updated")
        except Exception as e:
            logger.error(f"Error showing settings: {str(e)}", exc_info=True)

    def show_help(self):
        """Show help documentation."""
        try:
            # Show help content or tutorial
            self.show_welcome_tutorial()
        except Exception as e:
            logger.error(f"Error showing help: {str(e)}", exc_info=True)

    def closeEvent(self, event):
        """Handle application close event."""
        try:
            # Save current progress and state
            if self.current_language:
                self.content_manager.save_user_progress()
            event.accept()
        except Exception as e:
            logger.error(f"Error saving progress: {str(e)}", exc_info=True)
            reply = QMessageBox.question(
                self,
                "Error Saving Progress",
                "An error occurred while saving progress. Exit anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()