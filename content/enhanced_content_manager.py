# content/enhanced_content_manager.py

import logging
import json
import pickle
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from functools import lru_cache, wraps
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import Language, Topic, Example, Exercise

logger = logging.getLogger('TutorialAgent.ContentManager')


@dataclass
class CacheEntry:
    """Cache entry with timestamp and metadata."""
    data: Any
    timestamp: float
    hash_key: str
    access_count: int = 0
    size_bytes: int = 0


class ContentCache:
    """Advanced content caching system with LRU eviction."""

    def __init__(self, max_size_mb: int = 50, ttl_seconds: int = 3600):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, CacheEntry] = {}
        self.current_size_bytes = 0
        self.lock = threading.RLock()

        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def get(self, key: str) -> Optional[Any]:
        """Get item from cache."""
        with self.lock:
            entry = self.cache.get(key)
            if entry is None:
                self.misses += 1
                return None

            # Check TTL
            if time.time() - entry.timestamp > self.ttl_seconds:
                self._remove_entry(key)
                self.misses += 1
                return None

            # Update access statistics
            entry.access_count += 1
            self.hits += 1
            return entry.data

    def put(self, key: str, data: Any) -> None:
        """Put item in cache with size management."""
        with self.lock:
            # Calculate size
            try:
                size_bytes = len(pickle.dumps(data))
            except:
                size_bytes = 1024  # Fallback size estimate

            # Remove if already exists
            if key in self.cache:
                self._remove_entry(key)

            # Check if we need to evict
            while (self.current_size_bytes + size_bytes > self.max_size_bytes and
                   len(self.cache) > 0):
                self._evict_lru()

            # Add new entry
            hash_key = hashlib.md5(str(data).encode()).hexdigest()
            entry = CacheEntry(
                data=data,
                timestamp=time.time(),
                hash_key=hash_key,
                size_bytes=size_bytes
            )

            self.cache[key] = entry
            self.current_size_bytes += size_bytes

    def _remove_entry(self, key: str) -> None:
        """Remove entry from cache."""
        if key in self.cache:
            entry = self.cache.pop(key)
            self.current_size_bytes -= entry.size_bytes

    def _evict_lru(self) -> None:
        """Evict least recently used item."""
        if not self.cache:
            return

        # Find LRU item (lowest access_count and oldest timestamp)
        lru_key = min(self.cache.keys(),
                      key=lambda k: (self.cache[k].access_count, self.cache[k].timestamp))

        self._remove_entry(lru_key)
        self.evictions += 1
        logger.debug(f"Evicted cache entry: {lru_key}")

    def clear(self) -> None:
        """Clear all cache entries."""
        with self.lock:
            self.cache.clear()
            self.current_size_bytes = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

        return {
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'hit_rate': hit_rate,
            'cache_size': len(self.cache),
            'memory_usage_mb': self.current_size_bytes / (1024 * 1024),
            'max_memory_mb': self.max_size_bytes / (1024 * 1024)
        }


def timed_cache(ttl_seconds: int = 300):
    """Decorator for timed caching of method results."""

    def decorator(func):
        func._cache = {}
        func._cache_times = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = str(args[1:]) + str(sorted(kwargs.items()))  # Skip 'self'
            current_time = time.time()

            # Check if cached result is still valid
            if (key in func._cache and
                    current_time - func._cache_times.get(key, 0) < ttl_seconds):
                return func._cache[key]

            # Call function and cache result
            result = func(*args, **kwargs)
            func._cache[key] = result
            func._cache_times[key] = current_time

            return result

        return wrapper

    return decorator


class PerformanceMonitor:
    """Monitor and log performance metrics."""

    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()

    def record_operation(self, operation: str, duration: float, success: bool = True):
        """Record operation performance."""
        with self.lock:
            if operation not in self.metrics:
                self.metrics[operation] = {
                    'count': 0,
                    'total_time': 0.0,
                    'success_count': 0,
                    'min_time': float('inf'),
                    'max_time': 0.0
                }

            stats = self.metrics[operation]
            stats['count'] += 1
            stats['total_time'] += duration
            stats['min_time'] = min(stats['min_time'], duration)
            stats['max_time'] = max(stats['max_time'], duration)

            if success:
                stats['success_count'] += 1

    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """Get performance statistics."""
        with self.lock:
            result = {}
            for operation, stats in self.metrics.items():
                result[operation] = {
                    'count': stats['count'],
                    'avg_time': stats['total_time'] / stats['count'] if stats['count'] > 0 else 0,
                    'min_time': stats['min_time'] if stats['min_time'] != float('inf') else 0,
                    'max_time': stats['max_time'],
                    'success_rate': stats['success_count'] / stats['count'] * 100 if stats['count'] > 0 else 0
                }
            return result


def performance_tracked(operation_name: str):
    """Decorator to track method performance."""

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            success = True
            try:
                result = func(self, *args, **kwargs)
                return result
            except Exception as e:
                success = False
                raise
            finally:
                duration = time.time() - start_time
                if hasattr(self, 'performance_monitor'):
                    self.performance_monitor.record_operation(operation_name, duration, success)

                # Log slow operations
                if duration > 1.0:
                    logger.warning(f"Slow operation {operation_name}: {duration:.2f}s")

        return wrapper

    return decorator


class EnhancedContentManager:
    """Enhanced content manager with caching, performance monitoring, and parallel loading."""

    def __init__(self, content_dir: Path, cache_size_mb: int = 50):
        self.content_dir = Path(content_dir)
        self.cache = ContentCache(max_size_mb=cache_size_mb)
        self.performance_monitor = PerformanceMonitor()

        # Thread pool for parallel operations
        self.executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="ContentLoader")

        # Content storage
        self._languages: Dict[str, Language] = {}
        self._content_loaded = False
        self._loading_lock = threading.Lock()

        # User progress
        self.user_progress: Dict[str, Any] = {}
        self.progress_file = self.content_dir / 'user_progress.json'

        # Configuration
        self.config = {
            'lazy_loading': True,
            'parallel_loading': True,
            'cache_enabled': True,
            'auto_save_progress': True
        }

        logger.info(f"Enhanced ContentManager initialized with content_dir: {content_dir}")

        # Load configuration and user progress
        self._load_user_progress()

        # Pre-load essential content
        if not self.config['lazy_loading']:
            self._load_all_content()

    @performance_tracked("load_all_languages")
    def get_all_languages(self) -> Dict[str, Language]:
        """Get all available languages with caching."""
        cache_key = "all_languages"
        cached_result = self.cache.get(cache_key)

        if cached_result is not None and self.config['cache_enabled']:
            logger.debug("Returning cached languages")
            return cached_result

        # Load if not already loaded
        if not self._content_loaded:
            self._load_all_content()

        # Cache the result
        if self.config['cache_enabled']:
            self.cache.put(cache_key, self._languages)

        return self._languages

    @performance_tracked("load_all_content")
    def _load_all_content(self):
        """Load all content with parallel processing."""
        with self._loading_lock:
            if self._content_loaded:
                return

            start_time = time.time()
            logger.info("Loading all content...")

            try:
                languages_dir = self.content_dir / 'languages'
                if not languages_dir.exists():
                    logger.warning(f"Languages directory not found: {languages_dir}")
                    self._content_loaded = True
                    return

                # Get all language directories
                language_dirs = [d for d in languages_dir.iterdir() if d.is_dir()]

                if self.config['parallel_loading'] and len(language_dirs) > 1:
                    self._load_languages_parallel(language_dirs)
                else:
                    self._load_languages_sequential(language_dirs)

                self._content_loaded = True
                load_time = time.time() - start_time
                logger.info(f"Content loading completed in {load_time:.2f}s. Loaded {len(self._languages)} languages")

            except Exception as e:
                logger.error(f"Error loading content: {e}", exc_info=True)
                raise

    def _load_languages_parallel(self, language_dirs: List[Path]):
        """Load languages in parallel using thread pool."""
        futures = {}

        # Submit loading tasks
        for lang_dir in language_dirs:
            future = self.executor.submit(self._load_single_language, lang_dir)
            futures[future] = lang_dir.name

        # Collect results
        for future in as_completed(futures):
            lang_name = futures[future]
            try:
                language = future.result(timeout=30)  # 30 second timeout
                if language:
                    self._languages[lang_name] = language
                    logger.debug(f"Loaded language: {lang_name}")
            except Exception as e:
                logger.error(f"Error loading language {lang_name}: {e}")

    def _load_languages_sequential(self, language_dirs: List[Path]):
        """Load languages sequentially."""
        for lang_dir in language_dirs:
            try:
                language = self._load_single_language(lang_dir)
                if language:
                    self._languages[lang_dir.name] = language
                    logger.debug(f"Loaded language: {lang_dir.name}")
            except Exception as e:
                logger.error(f"Error loading language {lang_dir.name}: {e}")

    @performance_tracked("load_single_language")
    def _load_single_language(self, lang_dir: Path) -> Optional[Language]:
        """Load a single language with all its topics."""
        try:
            lang_name = lang_dir.name

            # Check cache first
            cache_key = f"language_{lang_name}"
            if self.config['cache_enabled']:
                cached_language = self.cache.get(cache_key)
                if cached_language:
                    return cached_language

            # Load language metadata
            metadata_file = lang_dir / 'metadata.json'
            metadata = self._load_language_metadata(metadata_file, lang_name)

            # Load topics
            topics = self._load_language_topics(lang_dir)

            # Create language object
            language = Language(
                name=metadata['name'],
                description=metadata['description'],
                icon=metadata.get('icon', 'default.png'),
                color=metadata.get('color', '#3498db'),
                topics=topics,
                learning_path=metadata.get('learning_path', []),
                difficulty=metadata.get('difficulty', 'Medium'),
                estimated_hours=metadata.get('estimated_hours', 10)
            )

            # Cache the language
            if self.config['cache_enabled']:
                self.cache.put(cache_key, language)

            return language

        except Exception as e:
            logger.error(f"Error loading language from {lang_dir}: {e}")
            return None

    def _load_language_metadata(self, metadata_file: Path, lang_name: str) -> Dict[str, Any]:
        """Load language metadata with fallbacks."""
        default_metadata = {
            'name': lang_name.title(),
            'description': f'Learn {lang_name.title()} programming language',
            'icon': 'default.png',
            'color': '#3498db',
            'learning_path': [],
            'difficulty': 'Medium',
            'estimated_hours': 10
        }

        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    # Merge with defaults
                    default_metadata.update(metadata)
            except Exception as e:
                logger.warning(f"Error loading metadata from {metadata_file}: {e}")

        return default_metadata

    @timed_cache(ttl_seconds=600)  # Cache for 10 minutes
    def _load_language_topics(self, lang_dir: Path) -> List[Topic]:
        """Load all topics for a language."""
        topics = []

        # Look for Python files in the language directory
        for topic_file in lang_dir.glob('*.py'):
            if topic_file.name.startswith('_'):
                continue  # Skip private files

            try:
                topic = self._load_topic_from_file(topic_file)
                if topic:
                    topics.append(topic)
            except Exception as e:
                logger.error(f"Error loading topic from {topic_file}: {e}")

        # Sort topics by name for consistent ordering
        topics.sort(key=lambda t: t.title)
        return topics

    @performance_tracked("load_topic_from_file")
    def _load_topic_from_file(self, topic_file: Path) -> Optional[Topic]:
        """Load a topic from a Python file."""
        try:
            # Import the module dynamically
            import importlib.util
            import sys

            spec = importlib.util.spec_from_file_location("topic_module", topic_file)
            if spec is None or spec.loader is None:
                logger.warning(f"Could not load spec for {topic_file}")
                return None

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Look for content creation function
            content_functions = [
                'create_content',
                f'create_{topic_file.stem}_content',
                'get_content',
                'main'
            ]

            for func_name in content_functions:
                if hasattr(module, func_name):
                    content_func = getattr(module, func_name)
                    return content_func()

            logger.warning(f"No content function found in {topic_file}")
            return None

        except Exception as e:
            logger.error(f"Error loading topic from {topic_file}: {e}")
            return None

    @performance_tracked("search_content")
    def search(self, query: str, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search content with advanced filtering and ranking."""
        if not query.strip():
            return []

        query_lower = query.lower()
        results = []

        # Search in all languages or specific language
        languages_to_search = (
            {language: self._languages[language]} if language and language in self._languages
            else self._languages
        )

        for lang_name, language in languages_to_search.items():
            for topic in language.topics:
                relevance_score = 0

                # Search in topic title (highest weight)
                if query_lower in topic.title.lower():
                    relevance_score += 10

                # Search in topic description
                if query_lower in topic.description.lower():
                    relevance_score += 5

                # Search in content
                if query_lower in topic.content.lower():
                    relevance_score += 3

                # Search in examples
                for example in topic.examples:
                    if (query_lower in example.title.lower() or
                            query_lower in example.code.lower() or
                            query_lower in example.explanation.lower()):
                        relevance_score += 2

                # Search in exercises
                for exercise in topic.exercises:
                    if (query_lower in exercise.title.lower() or
                            query_lower in exercise.description.lower()):
                        relevance_score += 2

                if relevance_score > 0:
                    results.append({
                        'language': lang_name,
                        'topic': topic.title,
                        'relevance': relevance_score,
                        'type': 'topic',
                        'content': topic
                    })

        # Sort by relevance score (descending)
        results.sort(key=lambda x: x['relevance'], reverse=True)

        # Limit results
        return results[:20]

    def get_language(self, language_name: str) -> Optional[Language]:
        """Get a specific language by name."""
        languages = self.get_all_languages()

        # Try exact match first
        for lang_id, language in languages.items():
            if language.name.lower() == language_name.lower():
                return language

        # Try partial match
        for lang_id, language in languages.items():
            if language_name.lower() in language.name.lower():
                return language

        return None

    def get_topic(self, language_name: str, topic_title: str) -> Optional[Topic]:
        """Get a specific topic from a language."""
        language = self.get_language(language_name)
        if not language:
            return None

        for topic in language.topics:
            if topic.title.lower() == topic_title.lower():
                return topic

        return None

    def _load_user_progress(self):
        """Load user progress from file."""
        try:
            if self.progress_file.exists():
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    self.user_progress = json.load(f)
                logger.debug("User progress loaded")
            else:
                self.user_progress = {}
        except Exception as e:
            logger.error(f"Error loading user progress: {e}")
            self.user_progress = {}

    @performance_tracked("save_user_progress")
    def save_user_progress(self):
        """Save user progress to file."""
        try:
            self.progress_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_progress, f, indent=2, ensure_ascii=False)
            logger.debug("User progress saved")
        except Exception as e:
            logger.error(f"Error saving user progress: {e}")

    def update_topic_progress(self, language: str, topic: str, progress: int):
        """Update progress for a specific topic."""
        if language not in self.user_progress:
            self.user_progress[language] = {
                'completed_topics': [],
                'topic_progress': {},
                'last_accessed': time.time()
            }

        self.user_progress[language]['topic_progress'][topic] = progress
        self.user_progress[language]['last_accessed'] = time.time()

        # Mark as completed if 100%
        if progress >= 100 and topic not in self.user_progress[language]['completed_topics']:
            self.user_progress[language]['completed_topics'].append(topic)

        # Auto-save if enabled
        if self.config['auto_save_progress']:
            self.save_user_progress()

    def get_user_statistics(self) -> Dict[str, Any]:
        """Get comprehensive user statistics."""
        stats = {
            'total_languages': len(self._languages),
            'languages_started': len(self.user_progress),
            'total_topics_completed': 0,
            'total_progress_percentage': 0,
            'most_recent_language': None,
            'learning_streak_days': 0,
            'cache_stats': self.cache.get_stats(),
            'performance_stats': self.performance_monitor.get_stats()
        }

        if self.user_progress:
            # Calculate totals
            total_topics = sum(len(lang.topics) for lang in self._languages.values())
            completed_topics = sum(len(prog.get('completed_topics', []))
                                   for prog in self.user_progress.values())

            stats['total_topics_completed'] = completed_topics
            stats['total_progress_percentage'] = (completed_topics / total_topics * 100) if total_topics > 0 else 0

            # Find most recent language
            most_recent = max(self.user_progress.items(),
                              key=lambda x: x[1].get('last_accessed', 0))
            stats['most_recent_language'] = most_recent[0]

        return stats

    def cleanup(self):
        """Cleanup resources."""
        try:
            self.executor.shutdown(wait=True, timeout=5)
            self.cache.clear()
            logger.info("ContentManager cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            self.cleanup()
        except:
            pass  # Ignore errors during destruction