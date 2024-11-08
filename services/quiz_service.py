from typing import List, Dict, Optional
from datetime import datetime
from database.db_handler import DatabaseHandler
from utils.quiz_handler import QuizHandler


class QuizService:
    def __init__(self):
        self.db = DatabaseHandler()
        self.quiz_handler = QuizHandler()

    def get_quiz(self, language: str, topic_id: str) -> Dict:
        """Get quiz questions for a specific topic"""
        quiz_data = self.quiz_handler.load_quiz(language, topic_id)
        if not quiz_data:
            return {
                'error': 'Quiz not found',
                'questions': []
            }

        return {
            'questions': self._prepare_quiz_questions(quiz_data),
            'total_questions': len(quiz_data),
            'time_limit': quiz_data.get('time_limit', 0),
            'passing_score': quiz_data.get('passing_score', 70)
        }

    def _prepare_quiz_questions(self, quiz_data: List[Dict]) -> List[Dict]:
        """Prepare quiz questions by removing answers"""
        prepared_questions = []
        for question in quiz_data:
            prepared_question = {
                'id': question['id'],
                'question': question['question'],
                'options': question['options'],
                'type': question.get('type', 'multiple_choice')
            }
            if question.get('code_snippet'):
                prepared_question['code_snippet'] = question['code_snippet']
            prepared_questions.append(prepared_question)
        return prepared_questions

    def submit_quiz(self, user_id: str, language: str,
                    topic_id: str, answers: Dict[str, int]) -> Dict:
        """Submit and grade quiz answers"""
        quiz_data = self.quiz_handler.load_quiz(language, topic_id)
        if not quiz_data:
            return {'error': 'Quiz not found'}

        score = 0
        total_questions = len(quiz_data)
        feedback = []

        for question in quiz_data:
            question_id = question['id']
            if question_id in answers:
                user_answer = answers[question_id]
                correct_answer = question['correct']
                is_correct = user_answer == correct_answer

                if is_correct:
                    score += 1

                feedback.append({
                    'question_id': question_id,
                    'correct': is_correct,
                    'explanation': question.get('explanation', '')
                })

        percentage = (score / total_questions) * 100
        passing_score = quiz_data.get('passing_score', 70)
        passed = percentage >= passing_score

        # Save result to database
        self.quiz_handler.save_result(
            user_id=user_id,
            language=language,
            topic=topic_id,
            score=score,
            total_questions=total_questions,
            duration=0  # TODO: Add duration tracking
        )

        return {
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'passed': passed,
            'feedback': feedback,
            'passing_score': passing_score
        }

    def get_user_quiz_history(self, user_id: str,
                              language: str = None) -> List[Dict]:
        """Get user's quiz history"""
        return self.quiz_handler.get_user_progress(user_id, language)

    def get_quiz_statistics(self, user_id: str,
                            language: str = None,
                            topic_id: str = None) -> Dict:
        """Get detailed quiz statistics"""
        return self.quiz_handler.get_statistics(user_id, language, topic_id)

    def get_leaderboard(self, language: str,
                        topic_id: str, limit: int = 10) -> List[Dict]:
        """Get leaderboard for a specific quiz"""
        return self.quiz_handler.get_leaderboard(language, topic_id, limit)

    def reset_quiz_progress(self, user_id: str,
                            language: str,
                            topic_id: str) -> bool:
        """Reset user's quiz progress for a specific topic"""
        return self.db.reset_quiz_progress(user_id, language, topic_id)

    def generate_practice_quiz(self, user_id: str,
                               language: str,
                               topic_id: str,
                               num_questions: int = 5) -> Dict:
        """Generate a practice quiz based on user's weak areas"""
        # Get user's quiz history
        history = self.get_user_quiz_history(user_id, language)

        # Load all questions for the topic
        all_questions = self.quiz_handler.load_quiz(language, topic_id)
        if not all_questions:
            return {'error': 'No questions available'}

        # Filter questions based on user's performance
        wrong_questions = []
        new_questions = []

        for question in all_questions:
            question_id = question['id']
            if self._is_question_answered_wrong(question_id, history):
                wrong_questions.append(question)
            else:
                new_questions.append(question)

        # Create practice quiz with mix of wrong and new questions
        practice_questions = []

        # Add wrong questions first
        wrong_count = min(num_questions // 2, len(wrong_questions))
        practice_questions.extend(wrong_questions[:wrong_count])

        # Fill remaining slots with new questions
        remaining_slots = num_questions - wrong_count
        practice_questions.extend(new_questions[:remaining_slots])

        return {
            'questions': self._prepare_quiz_questions(practice_questions),
            'total_questions': len(practice_questions),
            'is_practice': True
        }

    def _is_question_answered_wrong(self, question_id: str,
                                    history: List[Dict]) -> bool:
        """Check if a question was answered incorrectly in the past"""
        for attempt in history:
            if attempt.get('answers'):
                for answer in attempt['answers']:
                    if (answer.get('question_id') == question_id and
                            not answer.get('correct', False)):
                        return True
        return False

    def get_quiz_recommendations(self, user_id: str,
                                 language: str) -> List[Dict]:
        """Get quiz recommendations based on user's performance"""
        stats = self.get_quiz_statistics(user_id, language)
        topics = self.quiz_handler.get_recommended_topics(user_id, language)

        recommendations = []
        for topic in topics:
            recommendations.append({
                'topic_id': topic,
                'reason': 'Needs improvement',
                'current_score': stats.get('best_score', 0)
            })

        return recommendations