# content/content_manager.py

import logging
from pathlib import Path
import json
from typing import Dict, Optional
from .models import Language, Topic

logger = logging.getLogger('TutorialAgent')


class ContentManager:
    """Manages tutorial content and user progress."""

    def __init__(self, content_dir: Path):
        """Initialize the content manager."""
        try:
            logger.debug(f"Initializing ContentManager with directory: {content_dir}")
            self.content_dir = content_dir
            self.languages = {}
            self.user_progress = {}

            # Ensure directory structure exists
            self.ensure_content_directory()

            # Load content
            self.load_content()

            # Load user progress
            self.load_user_progress()

            logger.debug("ContentManager initialization complete")

        except Exception as e:
            logger.error(f"Error initializing ContentManager: {str(e)}", exc_info=True)
            raise

    def ensure_content_directory(self):
        """Ensure content directory structure exists."""
        try:
            logger.debug("Ensuring content directory structure...")

            # Create main directories
            self.content_dir.mkdir(parents=True, exist_ok=True)
            languages_dir = self.content_dir / 'languages'
            languages_dir.mkdir(exist_ok=True)

            # Create language directories
            for lang in ['python', 'javascript']:
                lang_dir = languages_dir / lang
                lang_dir.mkdir(exist_ok=True)

            logger.debug("Content directory structure verified")

        except Exception as e:
            logger.error(f"Error ensuring content directory: {str(e)}", exc_info=True)
            raise

    def load_content(self):
        """Load all language content."""
        try:
            logger.debug("Loading tutorial content")

            # Load Python content
            try:
                from .languages.python import get_python_content
                python = get_python_content()
                self.languages[python.id] = python
                logger.debug(f"Loaded Python content with {len(python.topics)} topics")
            except Exception as e:
                logger.error(f"Error loading Python content: {str(e)}", exc_info=True)

            # Load JavaScript content
            try:
                from .languages.javascript import get_javascript_content
                javascript = get_javascript_content()
                self.languages[javascript.id] = javascript
                logger.debug(f"Loaded JavaScript content with {len(javascript.topics)} topics")
            except Exception as e:
                logger.error(f"Error loading JavaScript content: {str(e)}", exc_info=True)

            # Print debug information
            self.debug_status()

            logger.info(f"Loaded content for {len(self.languages)} languages")

        except Exception as e:
            logger.error(f"Error loading content: {str(e)}", exc_info=True)
            raise

    def load_user_progress(self):
        """Load user progress from file."""
        try:
            progress_file = self.content_dir / 'user_progress.json'
            if progress_file.exists():
                with open(progress_file, 'r', encoding='utf-8') as f:
                    self.user_progress = json.load(f)
                logger.debug("Loaded user progress")
            else:
                logger.debug("No existing user progress found")
        except Exception as e:
            logger.error(f"Error loading user progress: {str(e)}", exc_info=True)

    def save_user_progress(self):
        """Save user progress to file."""
        try:
            progress_file = self.content_dir / 'user_progress.json'
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_progress, f, indent=2)
            logger.debug("Saved user progress")
        except Exception as e:
            logger.error(f"Error saving user progress: {str(e)}", exc_info=True)

    def get_language(self, language_name: str) -> Optional[Language]:
        """Get language by name."""
        try:
            for lang in self.languages.values():
                if lang.name.lower() == language_name.lower():
                    return lang
            return None
        except Exception as e:
            logger.error(f"Error getting language {language_name}: {str(e)}", exc_info=True)
            return None

    def get_all_languages(self) -> Dict[str, Language]:
        """Get all available languages."""
        return self.languages

    def get_language_progress(self, language: str) -> float:
        """Get overall progress for a language."""
        try:
            if language not in self.user_progress:
                return 0.0

            language_obj = self.get_language(language)
            if not language_obj or not language_obj.topics:
                return 0.0

            total_topics = len(language_obj.topics)
            completed_topics = len(self.user_progress[language].get('completed_topics', []))

            return (completed_topics / total_topics) * 100

        except Exception as e:
            logger.error(f"Error calculating progress for {language}: {str(e)}", exc_info=True)
            return 0.0

    def debug_status(self):
        """Print debug information about loaded content."""
        logger.debug("\n=== Content Manager Debug Information ===")
        logger.debug(f"Content directory: {self.content_dir}")
        logger.debug(f"Number of languages loaded: {len(self.languages)}")

        for lang_id, language in self.languages.items():
            logger.debug(f"\nLanguage: {language.name} (ID: {lang_id})")
            logger.debug(f"Icon: {language.icon}")
            logger.debug(f"Color: {language.color}")
            logger.debug(f"Number of topics: {len(language.topics)}")

            if language.topics:
                logger.debug("\nTopics:")
                for topic in language.topics:
                    logger.debug(f"- {topic.title}")
                    logger.debug(f"  Examples: {len(topic.examples)}")
                    logger.debug(f"  Exercises: {len(topic.exercises)}")

        logger.debug("\n=======================================")

    def has_started_language(self, language: str) -> bool:
        """Check if user has started a language."""
        return (language in self.user_progress and
                bool(self.user_progress[language].get('completed_topics', [])))

    def mark_topic_completed(self, language: str, topic_title: str):
        """Mark a topic as completed."""
        try:
            if language not in self.user_progress:
                self.user_progress[language] = {'completed_topics': []}

            completed_topics = self.user_progress[language]['completed_topics']
            if topic_title not in completed_topics:
                completed_topics.append(topic_title)
                self.save_user_progress()
                logger.debug(f"Marked topic '{topic_title}' as completed for {language}")
        except Exception as e:
            logger.error(f"Error marking topic as completed: {str(e)}", exc_info=True)