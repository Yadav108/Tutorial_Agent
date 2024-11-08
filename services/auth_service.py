import hashlib
import jwt
from datetime import datetime, timedelta
from database.db_handler import DatabaseHandler
from config.settings import Settings

class AuthService:
    def __init__(self):
        self.db = DatabaseHandler()
        self.settings = Settings()
        self.secret_key = self.settings.get('auth', 'secret_key')

    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username: str, password: str, email: str = None) -> bool:
        """Create a new user"""
        hashed_password = self.hash_password(password)
        return self.db.create_user(username, hashed_password, email)

    def validate_user(self, username: str, password: str) -> bool:
        """Validate user credentials"""
        hashed_password = self.hash_password(password)
        user = self.db.get_user_by_username(username)
        if user and user['password_hash'] == hashed_password:
            self.db.update_user_login(user['user_id'])
            return True
        return False

    def generate_token(self, username: str) -> str:
        """Generate JWT token for authenticated user"""
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token: str) -> dict:
        """Verify JWT token"""
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return None

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        if self.validate_user(username, old_password):
            new_hash = self.hash_password(new_password)
            return self.db.update_user_password(username, new_hash)
        return False

    def reset_password(self, email: str) -> bool:
        """Initiate password reset process"""
        user = self.db.get_user_by_email(email)
        if user:
            # Generate reset token
            reset_token = self.generate_token(user['username'])
            # Send reset email (implement email sending logic)
            return True
        return False

    def get_user_settings(self, username: str) -> dict:
        """Get user settings"""
        return self.db.get_user_settings(username)

    def update_user_settings(self, username: str, settings: dict) -> bool:
        """Update user settings"""
        return self.db.update_user_settings(username, settings)

    def delete_user(self, username: str, password: str) -> bool:
        """Delete user account"""
        if self.validate_user(username, password):
            return self.db.delete_user(username)
        return False