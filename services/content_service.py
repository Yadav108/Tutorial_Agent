import json
from pathlib import Path
from typing import List, Dict, Optional
from utils.content_loader import ContentLoader
from database.db_handler import DatabaseHandler


class ContentService:
    def __init__(self):
        self.content_loader = ContentLoader()
        self.db = DatabaseHandler()
        self.content_cache = {}

    def get_languages(self) -> List[Dict[str, str]]:
        """Get list of available programming languages"""
        return [
            {"id": "python", "name": "Python", "icon": "python.png"},
            {"id": "cpp", "name": "C++", "icon": "cpp.png"},
            {"id": "csharp", "name": "C#", "icon": "csharp.png"},
            {"id": "java", "name": "Java", "icon": "java.png"}
        ]

    def get_topics(self, language: str) -> List[Dict]:
        """Get topics for a specific language"""
        if language not in self.content_cache:
            self.content_cache[language] = self.content_loader.load_topics(language)
        return self.content_cache[language]

    def get_subtopics(self, language: str, topic_id: str) -> List[Dict]:
        """Get subtopics for a specific topic"""
        topics = self.get_topics(language)
        for topic in topics:
            if topic['id'] == topic_id:
                return topic.get('subtopics', [])
        return []

    def get_content(self, language: str, topic_id: str, subtopic_id: str) -> Optional[Dict]:
        """Get content for a specific subtopic"""
        subtopics = self.get_subtopics(language, topic_id)
        for subtopic in subtopics:
            if subtopic['id'] == subtopic_id:
                return subtopic
        return None

    def get_examples(self, language: str, topic_id: str, subtopic_id: str) -> List[Dict]:
        """Get code examples for a specific subtopic"""
        content = self.get_content(language, topic_id, subtopic_id)
        if content:
            return content.get('examples', [])
        return []

    def get_exercises(self, language: str, topic_id: str) -> List[Dict]:
        """Get exercises for a specific topic"""
        return self.content_loader.load_exercises(language, topic_id)

    def save_user_progress(self, user_id: str, language: str,
                           topic_id: str, subtopic_id: str, status: str) -> bool:
        """Save user's progress"""
        return self.db.save_progress(user_id, language, topic_id, subtopic_id, status)

    def get_user_progress(self, user_id: str, language: str = None) -> Dict:
        """Get user's progress"""
        progress = self.db.get_user_progress(user_id, language)

        # Calculate completion percentages
        total_topics = len(self.get_topics(language)) if language else 0
        completed_topics = len([p for p in progress if p['status'] == 'completed'])

        return {
            'progress': progress,
            'completion_rate': (completed_topics / total_topics * 100) if total_topics > 0 else 0,
            'total_topics': total_topics,
            'completed_topics': completed_topics
        }

    def search_content(self, query: str, language: str = None) -> List[Dict]:
        """Search through content"""
        results = []
        languages = [language] if language else [lang['id'] for lang in self.get_languages()]

        for lang in languages:
            topics = self.get_topics(lang)
            for topic in topics:
                if self._matches_query(topic, query):
                    results.append({
                        'language': lang,
                        'topic': topic['title'],
                        'type': 'topic',
                        'id': topic['id']
                    })

                for subtopic in topic.get('subtopics', []):
                    if self._matches_query(subtopic, query):
                        results.append({
                            'language': lang,
                            'topic': topic['title'],
                            'subtopic': subtopic['title'],
                            'type': 'subtopic',
                            'id': subtopic['id']
                        })

        return results

    def _matches_query(self, content: Dict, query: str) -> bool:
        """Check if content matches search query"""
        query = query.lower()
        return (
                query in content.get('title', '').lower() or
                query in content.get('content', '').lower() or
                any(query in example.get('code', '').lower()
                    for example in content.get('examples', []))
        )

    def get_recommended_topics(self, user_id: str, language: str) -> List[Dict]:
        """Get topic recommendations based on user's progress"""
        progress = self.get_user_progress(user_id, language)
        completed_topics = set(p['topic_id'] for p in progress['progress'])
        all_topics = self.get_topics(language)

        # Filter out completed topics and sort by difficulty
        recommendations = [
            topic for topic in all_topics
            if topic['id'] not in completed_topics
        ]

        return recommendations[:5]  # Return top 5 recommendations

    def get_next_topic(self, language: str, current_topic_id: str) -> Optional[Dict]:
        """Get the next topic in sequence"""
        topics = self.get_topics(language)
        for i, topic in enumerate(topics):
            if topic['id'] == current_topic_id and i < len(topics) - 1:
                return topics[i + 1]
        return None