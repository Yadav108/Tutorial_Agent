from pathlib import Path
from typing import Dict, List, Optional
import json
import importlib
import logging
from dataclasses import asdict
from content.models import Language, Topic, Example, Exercise


class ContentManager:
    """Manages loading and organizing tutorial content."""

    def __init__(self):
        self.content_path = Path("content/languages")
        self.languages: Dict[str, Language] = {}
        self.logger = logging.getLogger(__name__)

    def load_all_content(self):
        """Load content for all supported programming languages."""
        for lang_dir in self.content_path.iterdir():
            if lang_dir.is_dir():
                try:
                    self._load_language_content(lang_dir.name)
                except Exception as e:
                    self.logger.error(f"Error loading content for {lang_dir.name}: {str(e)}")

    def _load_language_content(self, language: str):
        """Load content for a specific programming language."""
        try:
            # Import language module dynamically
            module_path = f"content.languages.{language}"
            lang_module = importlib.import_module(module_path)

            # Each language module should have a create_content function
            if hasattr(lang_module, 'create_content'):
                language_content = lang_module.create_content()
                self.languages[language] = language_content

                # Save content to JSON for caching
                self._cache_content(language, language_content)
            else:
                raise AttributeError(f"No create_content function found in {module_path}")

        except ImportError as e:
            self.logger.error(f"Could not import content for {language}: {str(e)}")
            # Try loading from cache
            cached_content = self._load_cached_content(language)
            if cached_content:
                self.languages[language] = cached_content

    def _cache_content(self, language: str, content: Language):
        """Cache language content to JSON file."""
        cache_dir = Path("content/cache")
        cache_dir.mkdir(parents=True, exist_ok=True)

        cache_file = cache_dir / f"{language}.json"
        try:
            with cache_file.open('w') as f:
                json.dump(asdict(content), f, indent=2)
        except Exception as e:
            self.logger.error(f"Error caching content for {language}: {str(e)}")

    def _load_cached_content(self, language: str) -> Optional[Language]:
        """Load language content from cache."""
        cache_file = Path("content/cache") / f"{language}.json"
        if cache_file.exists():
            try:
                with cache_file.open('r') as f:
                    data = json.load(f)
                    return self._deserialize_language(data)
            except Exception as e:
                self.logger.error(f"Error loading cached content for {language}: {str(e)}")
        return None

    def _deserialize_language(self, data: dict) -> Language:
        """Convert JSON data back to Language object."""
        return Language(
            name=data['name'],
            description=data['description'],
            topics=[self._deserialize_topic(t) for t in data['topics']],
            prerequisites=data['prerequisites'],
            learning_path=data['learning_path'],
            resources=data['resources']
        )

    def _deserialize_topic(self, data: dict) -> Topic:
        """Convert JSON data back to Topic object."""
        return Topic(
            title=data['title'],
            description=data['description'],
            content=data['content'],
            examples=[self._deserialize_example(e) for e in data['examples']],
            best_practices=data['best_practices'],
            exercises=[self._deserialize_exercise(e) for e in data['exercises']],
            subtopics=[self._deserialize_topic(st) for st in data['subtopics']]
        )

    def _deserialize_example(self, data: dict) -> Example:
        """Convert JSON data back to Example object."""
        return Example(
            title=data['title'],
            description=data['description'],
            code=data['code'],
            output=data.get('output'),
            explanation=data.get('explanation')
        )

    def _deserialize_exercise(self, data: dict) -> Exercise:
        """Convert JSON data back to Exercise object."""
        return Exercise(
            title=data['title'],
            description=data['description'],
            starter_code=data['starter_code'],
            solution=data['solution'],
            hints=data['hints'],
            test_cases=data['test_cases'],
            difficulty=data['difficulty']
        )

    def get_language_content(self, language: str) -> Optional[Language]:
        """Get content for a specific language."""
        return self.languages.get(language)

    def get_topic_content(self, language: str, topic_path: List[str]) -> Optional[Topic]:
        """Get content for a specific topic within a language."""
        language_content = self.get_language_content(language)
        if not language_content:
            return None

        current_topic = None
        current_topics = language_content.topics

        for topic_name in topic_path:
            for topic in current_topics:
                if topic.title == topic_name:
                    current_topic = topic
                    current_topics = topic.subtopics
                    break
            else:
                return None

        return current_topic

    def search_content(self, query: str) -> List[Dict]:
        """Search through all content."""
        results = []

        for language in self.languages.values():
            for topic in language.topics:
                self._search_topic(query, language.name, topic, results)

        return results

    def _search_topic(self, query: str, language: str, topic: Topic, results: List[Dict]):
        """Recursively search through topics."""
        query = query.lower()

        # Search in topic title and content
        if query in topic.title.lower() or query in topic.content.lower():
            results.append({
                'language': language,
                'topic': topic.title,
                'type': 'topic',
                'description': topic.description
            })

        # Search in examples
        for example in topic.examples:
            if query in example.title.lower() or query in example.description.lower():
                results.append({
                    'language': language,
                    'topic': topic.title,
                    'type': 'example',
                    'description': example.title
                })

        # Search in exercises
        for exercise in topic.exercises:
            if query in exercise.title.lower() or query in exercise.description.lower():
                results.append({
                    'language': language,
                    'topic': topic.title,
                    'type': 'exercise',
                    'description': exercise.title
                })

        # Search in subtopics
        for subtopic in topic.subtopics:
            self._search_topic(query, language, subtopic, results)

    def get_learning_path(self, language: str) -> List[str]:
        """Get the recommended learning path for a language."""
        language_content = self.get_language_content(language)
        return language_content.learning_path if language_content else []

    def get_prerequisites(self, language: str) -> List[str]:
        """Get prerequisites for a language."""
        language_content = self.get_language_content(language)
        return language_content.prerequisites if language_content else []

    def get_resources(self, language: str) -> List[Dict[str, str]]:
        """Get additional resources for a language."""
        language_content = self.get_language_content(language)
        return language_content.resources if language_content else []


# Usage Example:
if __name__ == "__main__":
    content_manager = ContentManager()
    content_manager.load_all_content()

    # Get Python content
    python_content = content_manager.get_language_content("python")
    if python_content:
        print(f"Loaded {len(python_content.topics)} topics for Python")

        # Search for specific content
        results = content_manager.search_content("variables")
        print(f"Found {len(results)} results for 'variables'")