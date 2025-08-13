# content/content_manager.py

import json
import logging
import os
import time
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from functools import lru_cache
import hashlib
import pickle

logger = logging.getLogger('TutorialAgent.ContentManager')


@dataclass
class CacheEntry:
    """Cache entry for content data."""
    data: Any
    timestamp: float
    file_hash: str


class ContentCache:
    """Intelligent caching system for content."""

    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or Path.home() / '.tutorial_agent' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache: Dict[str, CacheEntry] = {}
        self.max_memory_items = 50

    def _get_file_hash(self, file_path: Path) -> str:
        """Get file hash for cache validation."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""

    def _get_cache_file(self, key: str) -> Path:
        """Get cache file path for a key."""
        safe_key = "".join(c for c in key if c.isalnum() or c in ('_', '-'))
        return self.cache_dir / f"{safe_key}.cache"

    def get(self, key: str, file_path: Path = None, max_age: int = 3600) -> Optional[Any]:
        """Get cached data."""
        try:
            # Check memory cache first
            if key in self.memory_cache:
                entry = self.memory_cache[key]

                # Check if file-based cache is still valid
                if file_path and self._get_file_hash(file_path) != entry.file_hash:
                    del self.memory_cache[key]
                # Check age
                elif time.time() - entry.timestamp > max_age:
                    del self.memory_cache[key]
                else:
                    return entry.data

            # Check disk cache
            cache_file = self._get_cache_file(key)
            if cache_file.exists():
                with open(cache_file, 'rb') as f:
                    entry = pickle.load(f)

                # Validate cache
                current_hash = self._get_file_hash(file_path) if file_path else entry.file_hash
                if (current_hash == entry.file_hash and
                        time.time() - entry.timestamp <= max_age):

                    # Store in memory cache
                    self.memory_cache[key] = entry
                    self._cleanup_memory_cache()
                    return entry.data
                else:
                    # Remove invalid cache
                    cache_file.unlink()

            return None

        except Exception as e:
            logger.warning(f"Error reading cache for {key}: {e}")
            return None

    def set(self, key: str, data: Any, file_path: Path = None):
        """Set cached data."""
        try:
            file_hash = self._get_file_hash(file_path) if file_path else ""
            entry = CacheEntry(data, time.time(), file_hash)

            # Store in memory
            self.memory_cache[key] = entry
            self._cleanup_memory_cache()

            # Store on disk
            cache_file = self._get_cache_file(key)
            with open(cache_file, 'wb') as f:
                pickle.dump(entry, f)

        except Exception as e:
            logger.warning(f"Error setting cache for {key}: {e}")

    def _cleanup_memory_cache(self):
        """Clean up memory cache if it's too large."""
        if len(self.memory_cache) > self.max_memory_items:
            # Remove oldest entries
            sorted_items = sorted(
                self.memory_cache.items(),
                key=lambda x: x[1].timestamp
            )
            for key, _ in sorted_items[:-self.max_memory_items]:
                del self.memory_cache[key]

    def clear(self):
        """Clear all caches."""
        self.memory_cache.clear()
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                cache_file.unlink()
            except Exception:
                pass


class ContentManager:
    """Content manager that works with Python content files."""

    def __init__(self, content_dir: Path):
        self.content_dir = Path(content_dir)
        self.cache = ContentCache()
        self.user_progress = self._load_user_progress()
        self._languages_cache = None
        self._search_index = None

        logger.info(f"ContentManager initialized with content_dir: {self.content_dir}")

    def _load_python_module(self, file_path: Path):
        """Load a Python module from file path."""
        try:
            spec = importlib.util.spec_from_file_location("content_module", file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                # Add the content directory to sys.path temporarily
                old_path = sys.path[:]
                sys.path.insert(0, str(self.content_dir.parent))
                try:
                    spec.loader.exec_module(module)
                    return module
                finally:
                    sys.path[:] = old_path
            return None
        except Exception as e:
            logger.error(f"Error loading Python module {file_path}: {e}")
            return None

    def _find_create_function(self, module, file_name: str):
        """Find the create function in a module."""
        # Try common function naming patterns
        possible_names = [
            f"create_{file_name}_content",
            f"create_{file_name}",
            f"get_{file_name}_content",
            f"get_{file_name}",
            "create_content",
            "get_content"
        ]

        for func_name in possible_names:
            if hasattr(module, func_name):
                func = getattr(module, func_name)
                if callable(func):
                    return func

        # If no standard function found, look for any function that returns a Topic
        for attr_name in dir(module):
            if not attr_name.startswith('_'):
                attr = getattr(module, attr_name)
                if callable(attr):
                    try:
                        # Try calling it to see if it returns a Topic
                        result = attr()
                        if hasattr(result, 'title') and hasattr(result, 'description'):
                            return attr
                    except:
                        continue

        return None

    @lru_cache(maxsize=32)
    def get_all_languages(self) -> Dict[str, 'Language']:
        """Get all available languages from Python files."""
        cache_key = "all_languages"

        # Try cache first
        cached_data = self.cache.get(cache_key, max_age=300)  # 5 minutes
        if cached_data:
            logger.debug("Loaded languages from cache")
            return cached_data

        logger.debug("Loading languages from Python files")
        languages = {}

        try:
            languages_dir = self.content_dir / 'languages'
            if not languages_dir.exists():
                logger.warning(f"Languages directory not found: {languages_dir}")
                return {}

            for lang_dir in languages_dir.iterdir():
                if not lang_dir.is_dir() or lang_dir.name.startswith('.') or lang_dir.name == '__pycache__':
                    continue

                try:
                    language = self._load_language_from_py_files(lang_dir)
                    if language:
                        languages[language.id] = language
                        logger.debug(f"Loaded language: {language.name}")
                except Exception as e:
                    logger.error(f"Error loading language from {lang_dir}: {e}")

            # Cache the result
            self.cache.set(cache_key, languages)
            logger.info(f"Loaded {len(languages)} languages")

        except Exception as e:
            logger.error(f"Error loading languages: {e}")

        return languages

    def _load_language_from_py_files(self, lang_dir: Path) -> Optional['Language']:
        """Load a language from Python files."""
        try:
            from .models import Language, DifficultyLevel  # Import here to avoid circular imports

            lang_name = lang_dir.name
            topics = []

            # Get all Python files in the language directory
            py_files = list(lang_dir.glob('*.py'))

            # Filter out __init__.py and other special files
            content_files = [f for f in py_files if not f.name.startswith('_')]

            if not content_files:
                logger.warning(f"No content files found in {lang_dir}")
                return None

            # Load topics from Python files
            for py_file in content_files:
                try:
                    topic = self._load_topic_from_py_file(py_file)
                    if topic:
                        topics.append(topic)
                        logger.debug(f"Loaded topic: {topic.title}")
                except Exception as e:
                    logger.error(f"Error loading topic from {py_file}: {e}")

            if not topics:
                logger.warning(f"No topics loaded for language {lang_name}")
                return None

            # Create language object with correct parameters
            language_info = self._get_language_info(lang_name)

            language = Language(
                name=language_info['name'],
                description=language_info['description'],
                topics=topics,
                id=lang_name,
                icon=language_info['icon'],
                color=language_info['color'],
                learning_path=[topic.title.lower().replace(' ', '_') for topic in topics],
                difficulty=DifficultyLevel.BEGINNER,
                estimated_hours=max(1, sum(getattr(topic, 'estimated_time', 30) for topic in topics) // 60)
            )

            return language

        except Exception as e:
            logger.error(f"Error creating language from {lang_dir}: {e}")
            return None

    def _get_language_info(self, lang_name: str) -> Dict[str, str]:
        """Get language-specific information."""
        language_info = {
            'python': {
                'name': 'Python',
                'description': 'A versatile, beginner-friendly programming language perfect for web development, data science, and automation.',
                'icon': 'python.svg',
                'color': '#3776ab'
            },
            'javascript': {
                'name': 'JavaScript',
                'description': 'The programming language that powers interactive websites and modern web applications.',
                'icon': 'javascript.svg',
                'color': '#f7df1e'
            },
            'java': {
                'name': 'Java',
                'description': 'A robust, object-oriented programming language used for enterprise applications and Android development.',
                'icon': 'java.svg',
                'color': '#ed8b00'
            },
            'csharp': {
                'name': 'C#',
                'description': 'A modern, object-oriented programming language developed by Microsoft for building Windows and web applications.',
                'icon': 'csharp.svg',
                'color': '#239120'
            },
            'cpp': {
                'name': 'C++',
                'description': 'A powerful, low-level programming language ideal for system programming and performance-critical applications.',
                'icon': 'cpp.svg',
                'color': '#00599c'
            }
        }

        return language_info.get(lang_name, {
            'name': lang_name.title(),
            'description': f'Learn {lang_name.title()} programming language.',
            'icon': f'{lang_name}.svg',
            'color': '#007bff'
        })

    def _load_topic_from_py_file(self, py_file: Path) -> Optional['Topic']:
        """Load a topic from a Python file."""
        try:
            cache_key = f"topic_{py_file.stem}"

            # Try cache first
            cached_topic = self.cache.get(cache_key, py_file, max_age=300)
            if cached_topic:
                return cached_topic

            # Load the Python module
            module = self._load_python_module(py_file)
            if not module:
                return None

            # Find the content creation function
            create_func = self._find_create_function(module, py_file.stem)
            if not create_func:
                logger.warning(f"No create function found in {py_file}")
                return None

            # Call the function to get the topic
            topic = create_func()

            # Validate that it's a topic-like object
            if not (hasattr(topic, 'title') and hasattr(topic, 'description')):
                logger.warning(f"Invalid topic object from {py_file}")
                return None

            # Cache the topic
            self.cache.set(cache_key, topic, py_file)

            return topic

        except Exception as e:
            logger.error(f"Error loading topic from {py_file}: {e}")
            return None

    def get_language(self, language_id: str) -> Optional['Language']:
        """Get a specific language by ID."""
        languages = self.get_all_languages()
        return languages.get(language_id)

    def search(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Enhanced search with indexing."""
        if not query.strip():
            return []

        query = query.lower().strip()
        results = []

        try:
            # Build search index if not exists
            if not self._search_index:
                self._build_search_index()

            # Search in the index
            for item in self._search_index:
                score = self._calculate_relevance_score(query, item)
                if score > 0:
                    results.append({
                        'type': item['type'],
                        'title': item['title'],
                        'description': item['description'],
                        'language': item['language'],
                        'score': score,
                        'content': item.get('content', ''),
                        'path': item.get('path', '')
                    })

            # Sort by relevance score
            results.sort(key=lambda x: x['score'], reverse=True)

            return results[:max_results]

        except Exception as e:
            logger.error(f"Error performing search: {e}")
            return []

    def _build_search_index(self):
        """Build search index for fast searching."""
        try:
            cache_key = "search_index"

            # Try cache first
            cached_index = self.cache.get(cache_key, max_age=1800)  # 30 minutes
            if cached_index:
                self._search_index = cached_index
                return

            logger.debug("Building search index...")
            self._search_index = []

            languages = self.get_all_languages()
            for lang_id, language in languages.items():
                # Index language
                self._search_index.append({
                    'type': 'language',
                    'title': language.name,
                    'description': language.description,
                    'language': language.name,
                    'content': f"{language.name} {language.description}",
                    'path': f"languages/{lang_id}"
                })

                # Index topics
                for topic in language.topics:
                    content_text = getattr(topic, 'content', '')
                    self._search_index.append({
                        'type': 'topic',
                        'title': topic.title,
                        'description': topic.description,
                        'language': language.name,
                        'content': f"{topic.title} {topic.description} {content_text}",
                        'path': f"languages/{lang_id}/topics/{topic.title.lower().replace(' ', '_')}"
                    })

                    # Index examples
                    if hasattr(topic, 'examples'):
                        for i, example in enumerate(topic.examples):
                            self._search_index.append({
                                'type': 'example',
                                'title': getattr(example, 'title', f'Example {i + 1}'),
                                'description': getattr(example, 'explanation', ''),
                                'language': language.name,
                                'content': f"{getattr(example, 'title', '')} {getattr(example, 'explanation', '')} {getattr(example, 'code', '')}",
                                'path': f"languages/{lang_id}/topics/{topic.title.lower().replace(' ', '_')}/examples/{i}"
                            })

                    # Index exercises
                    if hasattr(topic, 'exercises'):
                        for i, exercise in enumerate(topic.exercises):
                            self._search_index.append({
                                'type': 'exercise',
                                'title': getattr(exercise, 'title', f'Exercise {i + 1}'),
                                'description': getattr(exercise, 'description', ''),
                                'language': language.name,
                                'content': f"{getattr(exercise, 'title', '')} {getattr(exercise, 'description', '')}",
                                'path': f"languages/{lang_id}/topics/{topic.title.lower().replace(' ', '_')}/exercises/{i}"
                            })

            # Cache the index
            self.cache.set(cache_key, self._search_index)
            logger.info(f"Built search index with {len(self._search_index)} items")

        except Exception as e:
            logger.error(f"Error building search index: {e}")
            self._search_index = []

    def _calculate_relevance_score(self, query: str, item: Dict[str, Any]) -> float:
        """Calculate relevance score for search results."""
        score = 0.0
        content = item.get('content', '').lower()
        title = item.get('title', '').lower()
        description = item.get('description', '').lower()

        # Exact matches get highest score
        if query in title:
            score += 10.0
        if query in description:
            score += 5.0
        if query in content:
            score += 2.0

        # Word matches
        query_words = query.split()
        for word in query_words:
            if word in title:
                score += 3.0
            if word in description:
                score += 1.5
            if word in content:
                score += 0.5

        # Type-based scoring
        type_scores = {
            'language': 1.2,
            'topic': 1.0,
            'example': 0.8,
            'exercise': 0.9
        }
        score *= type_scores.get(item.get('type', ''), 1.0)

        return score

    def _load_user_progress(self) -> Dict[str, Any]:
        """Load user progress from file."""
        try:
            progress_file = self.content_dir.parent / 'user_progress.json'
            if progress_file.exists():
                with open(progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load user progress: {e}")

        return {}

    def save_user_progress(self):
        """Save user progress to file."""
        try:
            progress_file = self.content_dir.parent / 'user_progress.json'
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_progress, f, indent=2)
            logger.debug("User progress saved")
        except Exception as e:
            logger.error(f"Error saving user progress: {e}")

    def mark_topic_completed(self, language: str, topic_id: str):
        """Mark a topic as completed."""
        if language not in self.user_progress:
            self.user_progress[language] = {'completed_topics': [], 'scores': {}}

        if topic_id not in self.user_progress[language]['completed_topics']:
            self.user_progress[language]['completed_topics'].append(topic_id)
            self.save_user_progress()
            logger.info(f"Marked topic {topic_id} as completed for {language}")

    def get_progress_stats(self, language: str) -> Dict[str, Any]:
        """Get progress statistics for a language."""
        lang_obj = self.get_language(language)
        if not lang_obj:
            return {}

        total_topics = len(lang_obj.topics)
        completed_topics = len(self.user_progress.get(language, {}).get('completed_topics', []))

        return {
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'completion_percentage': (completed_topics / total_topics * 100) if total_topics > 0 else 0,
            'estimated_time_remaining': sum(
                getattr(topic, 'estimated_time', 30) for topic in lang_obj.topics
                if topic.title not in self.user_progress.get(language, {}).get('completed_topics', [])
            )
        }

    def invalidate_cache(self, language_id: str = None):
        """Invalidate cache for a specific language or all content."""
        if language_id:
            # Clear specific language cache
            cache_keys = [f"language_{language_id}", f"topic_{language_id}"]
            for key in cache_keys:
                if key in self.cache.memory_cache:
                    del self.cache.memory_cache[key]
        else:
            # Clear all cache
            self.cache.clear()
            self._search_index = None

        # Clear function cache
        self.get_all_languages.cache_clear()

        logger.info(f"Cache invalidated for {language_id or 'all content'}")

    def get_recommendations(self, language: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get personalized content recommendations."""
        try:
            lang_obj = self.get_language(language)
            if not lang_obj:
                return []

            completed_topics = set(self.user_progress.get(language, {}).get('completed_topics', []))
            recommendations = []

            for topic in lang_obj.topics:
                if topic.title not in completed_topics:
                    # Check prerequisites if they exist
                    prerequisites = getattr(topic, 'prerequisites', [])
                    prerequisites_met = all(
                        prereq in completed_topics
                        for prereq in prerequisites
                    )

                    if prerequisites_met:
                        recommendations.append({
                            'type': 'topic',
                            'id': topic.title.lower().replace(' ', '_'),
                            'title': topic.title,
                            'description': topic.description,
                            'difficulty': getattr(topic, 'difficulty', 'beginner'),
                            'estimated_time': getattr(topic, 'estimated_time', 30),
                            'reason': 'Next in learning path'
                        })

            return recommendations[:limit]

        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return []