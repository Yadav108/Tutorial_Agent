# gui/main_window.py - Fixed version

import logging
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QToolBar, QStatusBar, QSplitter, QSizePolicy,
    QLabel, QMessageBox, QPushButton, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer, QSize, QThread, QMutex, QMutexLocker
from PyQt6.QtGui import QAction, QIcon, QPixmap

from .widgets import (
    LanguageCard, ContentViewer, ProgressViewer, SearchBar
)
from .widgets.enhanced_code_editor import ProfessionalCodeEditor
from .dialogs import SettingsDialog, TutorialDialog
from content.models import Topic, Language
from utils.enhanced_notifications import show_success, show_error, show_warning, show_info
from content.content_manager import ContentManager

logger = logging.getLogger('TutorialAgent')


@dataclass
class AppState:
    """Centralized application state management."""
    current_language: Optional[str] = None
    is_welcome_shown: bool = False
    loading_in_progress: bool = False
    last_selected_topic: Optional[str] = None
    auto_save_enabled: bool = True
    theme: str = "light"


class ContentLoadingThread(QThread):
    """Background thread for loading content without blocking UI."""

    content_loaded = pyqtSignal(dict)
    progress_updated = pyqtSignal(int, str)
    error_occurred = pyqtSignal(str)

    def __init__(self, content_manager, language: str):
        super().__init__()
        self.content_manager = content_manager
        self.language = language
        self.mutex = QMutex()
        self._stop_requested = False

    def run(self):
        """Load content in background thread."""
        try:
            # Use QMutexLocker for proper mutex handling
            locker = QMutexLocker(self.mutex)

            if self._stop_requested:
                return

            self.progress_updated.emit(10, f"Loading {self.language}...")

            # Find language data
            language_data = None
            all_languages = self.content_manager.get_all_languages()

            for lang_id, lang_obj in all_languages.items():
                if lang_obj.name.lower() == self.language.lower():
                    language_data = lang_obj
                    break

            if not language_data:
                raise ValueError(f"No content found for {self.language}")

            self.progress_updated.emit(30, "Processing topics...")

            # Process content in chunks to show progress
            total_topics = len(language_data.topics)
            processed_topics = []

            for i, topic in enumerate(language_data.topics):
                if self._stop_requested:
                    return

                progress = 30 + (60 * i // total_topics) if total_topics > 0 else 90
                self.progress_updated.emit(progress, f"Loading {topic.title}...")

                # Safely access topic attributes with fallbacks
                topic_data = {
                    'title': getattr(topic, 'title', f'Topic {i + 1}'),
                    'description': getattr(topic, 'description', 'No description available'),
                    'content': getattr(topic, 'content', ''),
                    'examples': getattr(topic, 'examples', [])[:3],  # Limit examples for performance
                    'exercises': getattr(topic, 'exercises', [])[:2]  # Limit exercises for performance
                }
                processed_topics.append(topic_data)

                # Small delay to prevent UI freezing
                self.msleep(10)

            content_data = {
                'title': language_data.name,
                'description': language_data.description,
                'topics': processed_topics,
                'total_topics': total_topics,
                'language_id': self.language.lower()
            }

            self.progress_updated.emit(100, "Content loaded!")
            self.content_loaded.emit(content_data)

        except Exception as e:
            logger.error(f"Error loading content: {e}")
            self.error_occurred.emit(str(e))

    def stop(self):
        """Stop the loading thread."""
        locker = QMutexLocker(self.mutex)
        self._stop_requested = True


class WelcomeScreen(QWidget):
    """Enhanced welcome screen with animations."""

    get_started = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup welcome screen UI with better styling."""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #667eea, stop: 1 #764ba2);
            }
            QLabel#welcomeTitle {
                color: white;
                font-size: 42px;
                font-weight: bold;
                margin: 20px 0;
            }
            QLabel#welcomeSubtitle {
                color: rgba(255, 255, 255, 0.9);
                font-size: 20px;
                margin: 20px 0;
            }
            QLabel#featuresLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                margin: 15px 0;
            }
            QPushButton#getStartedBtn {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff6b6b, stop: 1 #ee5a52);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 18px 36px;
                font-size: 18px;
                font-weight: bold;
                min-width: 220px;
            }
            QPushButton#getStartedBtn:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff5252, stop: 1 #e53935);
                transform: translateY(-2px);
            }
            QPushButton#getStartedBtn:pressed {
                background: #e53935;
                transform: translateY(0px);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(25)
        layout.setContentsMargins(50, 50, 50, 50)

        # Logo/Icon section
        try:
            logo_path = Path(__file__).parent.parent / 'assets' / 'icons' / 'logo.png'
            if logo_path.exists():
                logo_label = QLabel()
                logo_pixmap = QPixmap(str(logo_path)).scaled(
                    80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                logo_label.setPixmap(logo_pixmap)
                logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(logo_label)
        except Exception as e:
            logger.debug(f"Logo not loaded: {e}")

        # Welcome content
        title = QLabel("Welcome to Tutorial Agent")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Master programming languages with interactive tutorials")
        subtitle.setObjectName("welcomeSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Features list
        features = QLabel(
            "• Interactive coding exercises\n• Real-time code execution\n• Progress tracking\n• Multiple programming languages")
        features.setObjectName("featuresLabel")
        features.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(features)

        # Get started button
        start_btn = QPushButton("🚀 Start Learning")
        start_btn.setObjectName("getStartedBtn")
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        start_btn.clicked.connect(self.get_started.emit)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)


class LoadingOverlay(QWidget):
    """Loading overlay widget for better UX during content loading."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.hide()

    def setup_ui(self):
        """Setup loading overlay UI."""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.7);
            }
            QFrame#loadingFrame {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
            }
            QLabel#loadingTitle {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
            }
            QLabel#loadingStatus {
                color: #7f8c8d;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Loading frame
        loading_frame = QFrame()
        loading_frame.setObjectName("loadingFrame")
        loading_frame.setFixedSize(300, 150)

        frame_layout = QVBoxLayout(loading_frame)
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.setSpacing(15)

        # Loading title
        self.loading_title = QLabel("Loading Content")
        self.loading_title.setObjectName("loadingTitle")
        self.loading_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(self.loading_title)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #ecf0f1;
                border-radius: 8px;
                text-align: center;
                height: 16px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 8px;
            }
        """)
        self.progress_bar.setRange(0, 100)
        frame_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Initializing...")
        self.status_label.setObjectName("loadingStatus")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(self.status_label)

        layout.addWidget(loading_frame)

    def show_loading(self, title: str = "Loading Content"):
        """Show loading overlay."""
        self.loading_title.setText(title)
        self.progress_bar.setValue(0)
        self.status_label.setText("Initializing...")
        self.show()
        self.raise_()

    def update_progress(self, value: int, status: str):
        """Update loading progress."""
        self.progress_bar.setValue(value)
        self.status_label.setText(status)

    def hide_loading(self):
        """Hide loading overlay."""
        self.hide()


class MainWindow(QMainWindow):
    """Enhanced main window with performance optimizations."""

    # Enhanced signals
    language_changed = pyqtSignal(str)
    content_loading_started = pyqtSignal(str)
    content_loading_finished = pyqtSignal(bool, str)
    theme_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Initialize state and components
        self.app_state = AppState()
        self.language_cards: Dict[str, LanguageCard] = {}
        self.content_loading_thread: Optional[ContentLoadingThread] = None

        # Performance monitoring
        self.startup_timer = QTimer()
        self.startup_timer.singleShot(0, self._measure_startup_time)

        try:
            self._init_content_manager()
            self._init_ui()
            self._setup_connections()
            self._setup_keyboard_shortcuts()

            # Delayed initialization for better startup performance
            QTimer.singleShot(100, self._post_init_setup)

            logger.info("MainWindow initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing MainWindow: {e}", exc_info=True)
            self._handle_critical_error(e)

    def _measure_startup_time(self):
        """Measure application startup time."""
        import time
        self.startup_time = time.time()

    def _init_content_manager(self):
        """Initialize content manager with enhanced error handling."""
        try:
            content_dir = Path(__file__).parent.parent / 'content'
            self.content_manager = ContentManager(content_dir)
            logger.debug("Content manager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize content manager: {e}")
            raise

    def _init_ui(self):
        """Initialize UI with optimized widget creation."""
        self.setWindowTitle("Programming Tutorial Agent")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)  # Better default size

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Setup components
        self._setup_toolbar()
        self._setup_statusbar()

        # Create main splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Create sidebar (optimized loading)
        sidebar = self._create_sidebar()
        self.main_splitter.addWidget(sidebar)

        # Create content stack
        self._create_content_stack()
        self.main_splitter.addWidget(self.content_stack)

        # Create loading overlay
        self.loading_overlay = LoadingOverlay(self.content_stack)

        # Configure splitter
        self.main_splitter.setStretchFactor(0, 1)  # Sidebar
        self.main_splitter.setStretchFactor(1, 3)  # Content area
        self.main_splitter.setSizes([350, 1050])

        main_layout.addWidget(self.main_splitter)

        logger.debug("UI initialization complete")

    def _setup_toolbar(self):
        """Setup enhanced toolbar with better organization."""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setStyleSheet("""
            QToolBar {
                spacing: 8px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffffff, stop: 1 #f8f9fa);
                border-bottom: 1px solid #dee2e6;
                padding: 8px 15px;
            }
            QToolButton {
                background: transparent;
                border: none;
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
            }
            QToolButton:hover {
                background: #e3f2fd;
                border: 1px solid #bbdefb;
            }
            QToolButton:pressed {
                background: #bbdefb;
            }
        """)

        # Add search bar
        self.search_bar = SearchBar()
        self.search_bar.search_triggered.connect(self._on_search)
        toolbar.addWidget(self.search_bar)

        # Add spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        # Add enhanced actions
        actions = [
            ("refresh", "Refresh Content", "Ctrl+R", self._refresh_content),
            ("settings", "Settings", "Ctrl+,", self._show_settings),
            ("help", "Help & Tutorials", "F1", self._show_help),
        ]

        for icon_name, text, shortcut, slot in actions:
            action = QAction(QIcon(f"assets/icons/{icon_name}.png"), text, self)
            action.setShortcut(shortcut)
            action.setToolTip(f"{text} ({shortcut})")
            action.triggered.connect(slot)
            toolbar.addAction(action)

        self.addToolBar(toolbar)
        logger.debug("Enhanced toolbar setup complete")

    def _setup_statusbar(self):
        """Setup enhanced status bar with more information."""
        status_bar = QStatusBar()
        status_bar.setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffffff, stop: 1 #f8f9fa);
                border-top: 1px solid #dee2e6;
                padding: 4px 15px;
            }
            QStatusBar::item {
                border: none;
            }
            QLabel {
                color: #495057;
                font-size: 13px;
            }
        """)

        # Main status label
        self.status_label = QLabel("Ready")
        status_bar.addWidget(self.status_label)

        # Add separators and additional info
        status_bar.addPermanentWidget(QLabel("•"))

        # Language indicator
        self.language_indicator = QLabel("No language selected")
        status_bar.addPermanentWidget(self.language_indicator)

        status_bar.addPermanentWidget(QLabel("•"))

        # Progress indicator (hidden by default)
        self.status_progress = QProgressBar()
        self.status_progress.setVisible(False)
        self.status_progress.setMaximumWidth(150)
        status_bar.addPermanentWidget(self.status_progress)

        self.setStatusBar(status_bar)
        logger.debug("Enhanced status bar setup complete")

    def _create_sidebar(self):
        """Create optimized sidebar with lazy loading."""
        sidebar = QWidget()
        sidebar.setMaximumWidth(350)
        sidebar.setMinimumWidth(280)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 15, 15, 15)
        sidebar_layout.setSpacing(15)

        # Sidebar header
        header = QLabel("Choose a Language")
        header.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        sidebar_layout.addWidget(header)

        # Load languages with error handling
        try:
            languages = self.content_manager.get_all_languages()
            logger.debug(f"Found {len(languages)} languages")

            if not languages:
                self._add_no_languages_message(sidebar_layout)
            else:
                self._create_language_cards(sidebar_layout, languages)
        except Exception as e:
            logger.error(f"Error loading languages: {e}")
            self._add_error_message(sidebar_layout, str(e))

        # Add progress viewer
        self.progress_viewer = ProgressViewer()
        sidebar_layout.addWidget(self.progress_viewer)

        # Add stretch
        sidebar_layout.addStretch()

        # Apply sidebar styling
        sidebar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #f8f9fa, stop: 1 #ffffff);
                border-right: 1px solid #dee2e6;
            }
        """)

        logger.info(f"Created sidebar with {len(self.language_cards)} language cards")
        return sidebar

    def _create_language_cards(self, layout: QVBoxLayout, languages: Dict):
        """Create language cards with optimized rendering."""
        for lang_id, language in languages.items():
            try:
                card = LanguageCard(
                    language=language.name,
                    description=self._truncate_description(language.description),
                    icon=f"assets/icons/{getattr(language, 'icon', 'default.png')}",
                    color=getattr(language, 'color', '#3498db')
                )
                card.clicked.connect(self._on_language_selected)
                layout.addWidget(card)
                self.language_cards[language.name] = card

                logger.debug(f"Created language card for {language.name}")

            except Exception as e:
                logger.error(f"Error creating card for {language.name}: {e}")
                continue

    def _truncate_description(self, description: str, max_length: int = 100) -> str:
        """Truncate description for better UI."""
        return description[:max_length] + "..." if len(description) > max_length else description

    def _add_no_languages_message(self, layout: QVBoxLayout):
        """Add message when no languages are available."""
        message = QLabel(
            "No programming languages available.\n\n"
            "Please check your content directory\n"
            "and restart the application."
        )
        message.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 14px;
                padding: 20px;
                text-align: center;
                background-color: #f8f9fa;
                border: 1px dashed #dee2e6;
                border-radius: 8px;
            }
        """)
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)

    def _add_error_message(self, layout: QVBoxLayout, error: str):
        """Add error message to sidebar."""
        message = QLabel(f"Error loading languages:\n{error}")
        message.setStyleSheet("""
            QLabel {
                color: #dc3545;
                font-size: 14px;
                padding: 15px;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 6px;
            }
        """)
        message.setWordWrap(True)
        layout.addWidget(message)

    def _create_content_stack(self):
        """Create content stack with welcome and main content."""
        self.content_stack = QStackedWidget()

        # Welcome screen
        self.welcome_screen = WelcomeScreen()
        self.welcome_screen.get_started.connect(self._on_get_started)
        self.content_stack.addWidget(self.welcome_screen)

        # Main content area
        self.content_area = self._create_content_area()
        self.content_stack.addWidget(self.content_area)

        # Start with welcome screen
        self.content_stack.setCurrentWidget(self.welcome_screen)

    def _create_content_area(self):
        """Create optimized content area."""
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create vertical splitter
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Content viewer
        self.content_viewer = ContentViewer()
        self.content_viewer.run_example.connect(self._run_code)
        self.content_viewer.start_exercise.connect(self._start_exercise)
        splitter.addWidget(self.content_viewer)

        # Code editor
        try:
            self.code_editor = ProfessionalCodeEditor()
            self.code_editor.code_executed.connect(self._handle_code_execution)
            logger.debug("Professional code editor loaded")
        except Exception as e:
            logger.warning(f"Could not load professional code editor: {e}")
            self.code_editor = self._create_fallback_editor()

        splitter.addWidget(self.code_editor)

        # Configure splitter
        splitter.setStretchFactor(0, 2)  # Content viewer
        splitter.setStretchFactor(1, 1)  # Code editor
        splitter.setSizes([500, 250])

        layout.addWidget(splitter)

        # Apply styling
        content_widget.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QSplitter::handle {
                background-color: #dee2e6;
                height: 3px;
            }
            QSplitter::handle:hover {
                background-color: #adb5bd;
            }
        """)

        logger.debug("Content area created successfully")
        return content_widget

    def _create_fallback_editor(self):
        """Create fallback code editor."""
        from PyQt6.QtWidgets import QTextEdit

        editor = QTextEdit()
        editor.setPlainText("# Your code here...\nprint('Hello, World!')")
        editor.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12pt;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 10px;
            }
        """)

        # Add basic methods for compatibility
        editor.set_language = lambda lang: None
        editor.set_code = lambda code: editor.setPlainText(code)
        editor.run_code = lambda: None

        return editor

    def _setup_connections(self):
        """Setup signal-slot connections."""
        # Language change signals
        self.language_changed.connect(self._update_language_indicator)
        self.language_changed.connect(self._update_code_editor_language)

        # Content loading signals
        self.content_loading_started.connect(self._show_loading)
        self.content_loading_finished.connect(self._hide_loading)

    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for better UX."""
        from PyQt6.QtGui import QShortcut, QKeySequence

        # Quick language switching (Ctrl+1, Ctrl+2, etc.)
        for i, lang_name in enumerate(self.language_cards.keys(), 1):
            if i <= 9:  # Support up to 9 languages
                shortcut = QShortcut(QKeySequence(f"Ctrl+{i}"), self)
                shortcut.activated.connect(lambda l=lang_name: self._on_language_selected(l))

        # Code execution shortcut
        run_shortcut = QShortcut(QKeySequence("Ctrl+Enter"), self)
        run_shortcut.activated.connect(self._run_current_code)

        # Clear editor shortcut
        clear_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        clear_shortcut.activated.connect(self._clear_editor)

    def _post_init_setup(self):
        """Post-initialization setup for better startup performance."""
        import time
        startup_time = time.time() - self.startup_time
        logger.info(f"Application startup completed in {startup_time:.2f} seconds")

        # Show welcome tutorial if first time
        if not self.app_state.is_welcome_shown:
            QTimer.singleShot(500, self._show_welcome_tutorial)
            self.app_state.is_welcome_shown = True

    @pyqtSlot()
    def _on_get_started(self):
        """Handle get started button click."""
        try:
            if self.language_cards:
                first_language = next(iter(self.language_cards.keys()))
                self._on_language_selected(first_language)
            else:
                show_error("No programming languages available", self)
        except Exception as e:
            logger.error(f"Error in get started: {e}")
            show_error(f"Error: {e}", self)

    @pyqtSlot(str)
    def _on_language_selected(self, language: str):
        """Handle language selection with optimized loading."""
        if self.app_state.loading_in_progress:
            show_warning("Please wait for current content to load", self)
            return

        try:
            logger.info(f"Language selected: {language}")

            # Update state
            self.app_state.current_language = language
            self.app_state.loading_in_progress = True

            # Update UI selection
            self._update_language_selection(language)

            # Switch to content area
            if self.content_stack.currentWidget() == self.welcome_screen:
                self.content_stack.setCurrentWidget(self.content_area)

            # Start background loading
            self._start_content_loading(language)

            # Emit signal
            self.language_changed.emit(language)

        except Exception as e:
            self.app_state.loading_in_progress = False
            logger.error(f"Error selecting language {language}: {e}")
            show_error(f"Error loading {language}: {e}", self)

    def _update_language_selection(self, selected_language: str):
        """Update visual selection state of language cards."""
        for language, card in self.language_cards.items():
            card.setSelected(language == selected_language)

    def _start_content_loading(self, language: str):
        """Start background content loading."""
        # Stop any existing loading
        if self.content_loading_thread and self.content_loading_thread.isRunning():
            self.content_loading_thread.stop()
            self.content_loading_thread.wait(1000)

        # Start new loading thread
        self.content_loading_thread = ContentLoadingThread(self.content_manager, language)
        self.content_loading_thread.content_loaded.connect(self._on_content_loaded)
        self.content_loading_thread.progress_updated.connect(self._on_loading_progress)
        self.content_loading_thread.error_occurred.connect(self._on_loading_error)

        self.content_loading_started.emit(language)
        self.content_loading_thread.start()

    @pyqtSlot(dict)
    def _on_content_loaded(self, content_data: dict):
        """Handle successful content loading."""
        try:
            language = content_data.get('title', 'Unknown')

            # Load content into viewer
            self.content_viewer.load_content(content_data)

            # Update progress viewer
            self._update_progress_display(language, content_data)

            # Update status
            self.status_label.setText(f"Loaded {language} content successfully")

            # Show success notification
            show_success(f"Loaded {language} successfully!", self)

            # Update state
            self.app_state.loading_in_progress = False
            self.content_loading_finished.emit(True, language)

            logger.info(f"Successfully loaded content for {language}")

        except Exception as e:
            logger.error(f"Error handling loaded content: {e}")
            self._on_loading_error(str(e))

    @pyqtSlot(int, str)
    def _on_loading_progress(self, value: int, status: str):
        """Handle loading progress updates."""
        self.loading_overlay.update_progress(value, status)
        self.status_progress.setValue(value)

    @pyqtSlot(str)
    def _on_loading_error(self, error: str):
        """Handle content loading errors."""
        self.app_state.loading_in_progress = False
        self.content_loading_finished.emit(False, error)

        logger.error(f"Content loading error: {error}")
        show_error(f"Error loading content: {error}", self)

        # Load fallback content
        if self.app_state.current_language:
            self._load_fallback_content(self.app_state.current_language)

    def _update_progress_display(self, language: str, content_data: dict):
        """Update progress display with loaded content."""
        try:
            # Get user progress from content manager
            user_progress = getattr(self.content_manager, 'user_progress', {})
            language_progress = user_progress.get(language, {})
            completed_topics = language_progress.get('completed_topics', [])

            # Create topic progress dictionary
            topic_progress = {}
            for topic_data in content_data.get('topics', []):
                topic_title = topic_data.get('title', '')
                # Check if topic is completed (you may need to adjust this logic)
                is_completed = topic_title.lower().replace(' ', '_') in completed_topics
                topic_progress[topic_title] = 100 if is_completed else 0

            # Update progress viewer
            self.progress_viewer.update_progress(language, topic_progress)

            # Update language card progress
            if language in self.language_cards:
                overall_progress = sum(topic_progress.values()) / len(topic_progress) if topic_progress else 0
                self.language_cards[language].set_progress(int(overall_progress))

        except Exception as e:
            logger.error(f"Error updating progress display: {e}")

    def _show_loading(self, language: str):
        """Show loading overlay."""
        self.loading_overlay.show_loading(f"Loading {language}")
        self.status_progress.setVisible(True)
        self.status_progress.setRange(0, 100)
        self.status_progress.setValue(0)

    def _hide_loading(self, success: bool, message: str):
        """Hide loading overlay."""
        self.loading_overlay.hide_loading()
        self.status_progress.setVisible(False)

        if success:
            self.status_label.setText(f"✓ {message}")
        else:
            self.status_label.setText(f"✗ Error: {message}")

    def _update_language_indicator(self, language: str):
        """Update language indicator in status bar."""
        self.language_indicator.setText(f"Language: {language}")

    def _update_code_editor_language(self, language: str):
        """Update code editor language setting."""
        if hasattr(self.code_editor, 'set_language'):
            self.code_editor.set_language(language.lower())

    def _load_fallback_content(self, language: str):
        """Load minimal fallback content on error."""
        fallback_content = {
            'title': f'{language} - Basic Content',
            'description': f'Basic tutorial content for {language}. Some features may not be available.',
            'topics': [
                {
                    'title': 'Getting Started',
                    'description': f'Introduction to {language} programming',
                    'content': f'# Welcome to {language}\n\nThis is basic fallback content.',
                    'examples': [],
                    'exercises': []
                }
            ]
        }

        try:
            self.content_viewer.load_content(fallback_content)
            show_warning(f"Loaded basic content for {language}", self)
        except Exception as e:
            logger.error(f"Error loading fallback content: {e}")

    def _run_code(self, code: str):
        """Execute code in editor."""
        try:
            if hasattr(self.code_editor, 'set_code'):
                self.code_editor.set_code(code)
            if hasattr(self.code_editor, 'run_code'):
                self.code_editor.run_code()
        except Exception as e:
            logger.error(f"Error running code: {e}")
            show_error(f"Error running code: {e}", self)

    def _run_current_code(self):
        """Run currently loaded code (keyboard shortcut)."""
        try:
            if hasattr(self.code_editor, 'run_code'):
                self.code_editor.run_code()
        except Exception as e:
            logger.error(f"Error running current code: {e}")

    def _clear_editor(self):
        """Clear code editor (keyboard shortcut)."""
        try:
            if hasattr(self.code_editor, 'clear_editor'):
                self.code_editor.clear_editor()
            elif hasattr(self.code_editor, 'clear'):
                self.code_editor.clear()
        except Exception as e:
            logger.error(f"Error clearing editor: {e}")

    def _start_exercise(self, exercise_data: dict):
        """Start a coding exercise."""
        try:
            starter_code = exercise_data.get('starter_code', '')
            if hasattr(self.code_editor, 'set_code'):
                self.code_editor.set_code(starter_code)

            exercise_title = exercise_data.get('title', 'Exercise')
            self.status_label.setText(f"Started exercise: {exercise_title}")
            show_info(f"Exercise loaded: {exercise_title}", self)

        except Exception as e:
            logger.error(f"Error starting exercise: {e}")
            show_error(f"Error starting exercise: {e}", self)

    def _handle_code_execution(self, success: bool, output: str):
        """Handle code execution results."""
        try:
            if success:
                self.status_label.setText("✓ Code executed successfully")
                show_success("Code executed successfully!", self)
            else:
                self.status_label.setText("✗ Code execution failed")
                show_error("Code execution failed", self)
        except Exception as e:
            logger.error(f"Error handling code execution: {e}")

    def _on_search(self, query: str):
        """Handle search queries."""
        try:
            # Implement search functionality
            if hasattr(self.content_manager, 'search'):
                results = self.content_manager.search(query)
                result_count = len(results) if results else 0
                self.status_label.setText(f"Found {result_count} results for '{query}'")
                show_info(f"Found {result_count} results", self)
            else:
                show_info(f"Searching for: {query}", self)
        except Exception as e:
            logger.error(f"Error performing search: {e}")
            show_error(f"Search error: {e}", self)

    def _refresh_content(self):
        """Refresh current content."""
        try:
            if self.app_state.current_language:
                self._on_language_selected(self.app_state.current_language)
            else:
                show_info("No language selected to refresh", self)
        except Exception as e:
            logger.error(f"Error refreshing content: {e}")
            show_error(f"Refresh error: {e}", self)

    def _show_settings(self):
        """Show settings dialog."""
        try:
            dialog = SettingsDialog(self)
            if dialog.exec():
                self.status_label.setText("Settings updated")
                show_success("Settings saved successfully!", self)
        except Exception as e:
            logger.error(f"Error showing settings: {e}")
            show_error(f"Settings error: {e}", self)

    def _show_help(self):
        """Show help and tutorials."""
        try:
            self._show_welcome_tutorial()
        except Exception as e:
            logger.error(f"Error showing help: {e}")

    def _show_welcome_tutorial(self):
        """Show welcome tutorial."""
        try:
            welcome_tutorial = {
                'id': 'welcome',
                'title': 'Welcome to Tutorial Agent',
                'steps': [
                    {
                        'number': 1,
                        'title': 'Welcome! 🎉',
                        'content': 'Welcome to Tutorial Agent! Let\'s take a quick tour to get you started with interactive programming tutorials.',
                        'tip': 'You can access this tutorial anytime from the Help menu.'
                    },
                    {
                        'number': 2,
                        'title': 'Choose Your Language 🚀',
                        'content': 'Start by selecting a programming language from the sidebar. Each language has structured lessons and interactive exercises.',
                        'tip': 'Use Ctrl+1, Ctrl+2, etc. to quickly switch between languages.'
                    },
                    {
                        'number': 3,
                        'title': 'Interactive Learning 💻',
                        'content': 'Read tutorials, try examples, and complete exercises. The code editor lets you run code instantly and see results.',
                        'tip': 'Press Ctrl+Enter to run code and Ctrl+K to clear the editor.'
                    },
                    {
                        'number': 4,
                        'title': 'Track Your Progress 📈',
                        'content': 'Your learning progress is automatically tracked. Watch your progress bars fill up as you complete topics and exercises.',
                        'tip': 'Complete exercises to earn progress points and unlock advanced topics.'
                    },
                    {
                        'number': 5,
                        'title': 'Ready to Learn! ✨',
                        'content': 'You\'re all set! Choose a language to begin your programming journey. Happy coding!',
                        'tip': 'Use the search bar to quickly find specific topics or concepts.'
                    }
                ]
            }

            TutorialDialog.show_tutorial(self, 'welcome', welcome_tutorial)

        except Exception as e:
            logger.error(f"Error showing welcome tutorial: {e}")

    def _handle_critical_error(self, error: Exception):
        """Handle critical errors during initialization."""
        error_msg = f"Critical error during initialization: {error}"
        logger.critical(error_msg, exc_info=True)

        reply = QMessageBox.critical(
            self,
            "Critical Error",
            f"The application encountered a critical error and cannot continue:\n\n{error}\n\n"
            "Please check the logs and restart the application.",
            QMessageBox.StandardButton.Ok
        )

        # Force exit
        import sys
        sys.exit(1)

    def resizeEvent(self, event):
        """Handle window resize to reposition loading overlay."""
        super().resizeEvent(event)
        if hasattr(self, 'loading_overlay'):
            self.loading_overlay.resize(self.content_stack.size())

    def closeEvent(self, event):
        """Handle application close with cleanup."""
        try:
            # Stop loading threads
            if self.content_loading_thread and self.content_loading_thread.isRunning():
                self.content_loading_thread.stop()
                self.content_loading_thread.wait(2000)

            # Save progress
            if self.app_state.current_language and hasattr(self.content_manager, 'save_user_progress'):
                self.content_manager.save_user_progress()

            # Cleanup code editor
            if hasattr(self.code_editor, 'cleanup'):
                self.code_editor.cleanup()

            event.accept()
            logger.info("Application closed successfully")

        except Exception as e:
            logger.error(f"Error during application close: {e}")
            reply = QMessageBox.question(
                self,
                "Error Saving",
                f"An error occurred while saving: {e}\n\nExit anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()