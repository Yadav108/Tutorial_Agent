"""
Core components for Tutorial Agent

This package contains the core business logic and main classes
for the Tutorial Agent application.
"""

from pathlib import Path
import sys

# Add parent directories to path for imports
core_dir = Path(__file__).parent
project_root = core_dir.parent.parent
sys.path.insert(0, str(project_root))

# Import core components
from content.content_manager import ContentManager
from config.settings_manager import SettingsManager

# Main application class
class TutorialAgent:
    """Main application controller class."""
    
    def __init__(self, config_file: str = None):
        """Initialize Tutorial Agent."""
        self.settings = SettingsManager(config_file)
        self.content_manager = ContentManager()
        self._initialized = False
    
    def initialize(self):
        """Initialize the application components."""
        if self._initialized:
            return
            
        # Initialize components
        self.content_manager.initialize(self.settings)
        self._initialized = True
    
    def run(self):
        """Run the Tutorial Agent application."""
        if not self._initialized:
            self.initialize()
            
        # Import and start GUI
        from gui.main_window import MainWindow
        from PyQt6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        window = MainWindow()
        app.setStyle('Fusion')
        window.show()
        
        return app.exec()

# Progress manager class
class ProgressManager:
    """Manages user progress and achievements."""
    
    def __init__(self):
        self.user_progress = {}
        self.achievements = []
    
    def update_progress(self, user_id: str, topic_id: str, progress: float):
        """Update progress for a user on a specific topic."""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
        self.user_progress[user_id][topic_id] = progress
    
    def get_progress(self, user_id: str, topic_id: str = None):
        """Get progress for a user."""
        if user_id not in self.user_progress:
            return 0.0 if topic_id else {}
        
        if topic_id:
            return self.user_progress[user_id].get(topic_id, 0.0)
        return self.user_progress[user_id]

# Export all components
__all__ = [
    "TutorialAgent",
    "ContentManager", 
    "ProgressManager",
    "SettingsManager"
]