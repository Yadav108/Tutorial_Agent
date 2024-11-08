from typing import List, Dict, Optional
from datetime import datetime, timedelta
from database.db_handler import DatabaseHandler


class ProgressService:
    def __init__(self):
        self.db = DatabaseHandler()

    def track_progress(self, user_id: str, language: str,
                       topic_id: str, subtopic_id: str,
                       status: str, time_spent: int = 0) -> bool:
        """Track user's learning progress"""
        return self.db.save_progress(
            user_id=user_id,
            language=language,
            topic_id=topic_id,
            subtopic_id=subtopic_id,
            status=status,
            time_spent=time_spent
        )

    def get_user_progress(self, user_id: str, language: str = None) -> Dict:
        """Get comprehensive progress report for a user"""
        progress_data = self.db.get_user_progress(user_id, language)
        quiz_results = self.db.get_quiz_results(user_id, language)
        code_submissions = self.db.get_code_submissions(user_id, language)

        # Calculate overall statistics
        total_topics = len(progress_data)
        completed_topics = len([p for p in progress_data if p['status'] == 'completed'])
        completion_rate = (completed_topics / total_topics * 100) if total_topics > 0 else 0

        # Calculate quiz performance
        quiz_stats = self._calculate_quiz_stats(quiz_results)

        # Calculate coding progress
        coding_stats = self._calculate_coding_stats(code_submissions)

        return {
            'overall_progress': {
                'completion_rate': completion_rate,
                'total_topics': total_topics,
                'completed_topics': completed_topics,
                'in_progress_topics': len([p for p in progress_data if p['status'] == 'in_progress'])
            },
            'quiz_performance': quiz_stats,
            'coding_progress': coding_stats,
            'learning_streak': self._calculate_learning_streak(user_id),
            'recent_activity': self._get_recent_activity(user_id),
            'achievements': self._get_achievements(user_id)
        }

    def _calculate_quiz_stats(self, quiz_results: List[Dict]) -> Dict:
        """Calculate quiz statistics"""
        if not quiz_results:
            return {
                'average_score': 0,
                'best_score': 0,
                'total_quizzes': 0,
                'quizzes_passed': 0
            }

        total_quizzes = len(quiz_results)
        scores = [result['score'] / result['max_score'] * 100 for result in quiz_results]
        passed_quizzes = len([s for s in scores if s >= 70])  # Assuming 70% is passing

        return {
            'average_score': sum(scores) / len(scores),
            'best_score': max(scores),
            'total_quizzes': total_quizzes,
            'quizzes_passed': passed_quizzes
        }

    def _calculate_coding_stats(self, submissions: List[Dict]) -> Dict:
        """Calculate coding exercise statistics"""
        if not submissions:
            return {
                'total_submissions': 0,
                'successful_submissions': 0,
                'success_rate': 0
            }

        total = len(submissions)
        successful = len([s for s in submissions if s['status'] == 'success'])

        return {
            'total_submissions': total,
            'successful_submissions': successful,
            'success_rate': (successful / total * 100) if total > 0 else 0
        }

    def _calculate_learning_streak(self, user_id: str) -> Dict:
        """Calculate user's learning streak"""
        recent_activity = self.db.get_user_activity(user_id)

        # Sort activity by date
        activity_dates = sorted(set(
            datetime.fromisoformat(activity['timestamp']).date()
            for activity in recent_activity
        ))

        if not activity_dates:
            return {'current_streak': 0, 'longest_streak': 0}

        # Calculate current streak
        current_streak = 0
        today = datetime.now().date()

        for date in reversed(activity_dates):
            if (today - date).days > current_streak + 1:
                break
            current_streak += 1

        # Calculate longest streak
        longest_streak = 0
        current = 1

        for i in range(1, len(activity_dates)):
            if (activity_dates[i] - activity_dates[i - 1]).days == 1:
                current += 1
                longest_streak = max(longest_streak, current)
            else:
                current = 1

        return {
            'current_streak': current_streak,
            'longest_streak': max(longest_streak, current_streak)
        }

    def _get_recent_activity(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get user's recent learning activity"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.db.get_user_activity(user_id, after_date=cutoff_date)

    def _get_achievements(self, user_id: str) -> List[Dict]:
        """Get user's earned achievements"""
        return self.db.get_user_achievements(user_id)

    def update_learning_goals(self, user_id: str, goals: Dict) -> bool:
        """Update user's learning goals"""
        return self.db.update_learning_goals(user_id, goals)

    def get_learning_goals(self, user_id: str) -> Dict:
        """Get user's learning goals"""
        return self.db.get_learning_goals(user_id)

    def generate_progress_report(self, user_id: str,
                                 language: str = None,
                                 start_date: datetime = None,
                                 end_date: datetime = None) -> Dict:
        """Generate detailed progress report"""
        progress = self.get_user_progress(user_id, language)

        # Filter by date range if provided
        if start_date and end_date:
            progress['recent_activity'] = [
                activity for activity in progress['recent_activity']
                if start_date <= datetime.fromisoformat(activity['timestamp']) <= end_date
            ]

        # Add time-based analysis
        study_times = self.db.get_study_times(user_id, start_date, end_date)
        progress['time_analysis'] = {
            'total_time': sum(time['duration'] for time in study_times),
            'average_session': sum(time['duration'] for time in study_times) / len(study_times) if study_times else 0,
            'peak_hours': self._calculate_peak_hours(study_times)
        }

        return progress

    def _calculate_peak_hours(self, study_times: List[Dict]) -> List[int]:
        """Calculate peak study hours"""
        hour_counts = [0] * 24
        for time in study_times:
            hour = datetime.fromisoformat(time['timestamp']).hour
            hour_counts[hour] += time['duration']

        # Return the top 3 most productive hours
        peak_hours = sorted(range(24), key=lambda h: hour_counts[h], reverse=True)[:3]
        return peak_hours