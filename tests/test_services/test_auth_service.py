import pytest
from unittest.mock import Mock, patch
from tutorial_agent.services.auth_service import AuthService
from tutorial_agent.database.models import User
from . import ServicesTestCase


class TestAuthService(ServicesTestCase):
    def setup_method(self):
        """Set up test method"""
        super().setup_method()
        self.auth_service = AuthService()
        self.test_user = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }

    def test_create_user_success(self):
        """Test successful user creation"""
        result = self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        assert result == True
        user = self.auth_service.get_user_by_username(self.test_user['username'])
        assert user is not None
        assert user['email'] == self.test_user['email']

    def test_create_user_duplicate_username(self):
        """Test user creation with duplicate username"""
        # Create first user
        self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        # Try to create duplicate user
        result = self.auth_service.create_user(
            self.test_user['username'],
            'DifferentPass123!',
            'different@example.com'
        )

        assert result == False

    def test_validate_user_success(self):
        """Test successful user validation"""
        # Create user
        self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        # Validate user
        result = self.auth_service.validate_user(
            self.test_user['username'],
            self.test_user['password']
        )

        assert result == True

    def test_validate_user_wrong_password(self):
        """Test user validation with wrong password"""
        # Create user
        self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        # Validate with wrong password
        result = self.auth_service.validate_user(
            self.test_user['username'],
            'WrongPass123!'
        )

        assert result == False

    def test_validate_user_nonexistent(self):
        """Test validation of nonexistent user"""
        result = self.auth_service.validate_user(
            'nonexistent',
            'AnyPass123!'
        )

        assert result == False

    def test_change_password_success(self):
        """Test successful password change"""
        # Create user
        self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        # Change password
        new_password = 'NewPass123!'
        result = self.auth_service.change_password(
            self.test_user['username'],
            self.test_user['password'],
            new_password
        )

        assert result == True

        # Verify new password works
        assert self.auth_service.validate_user(
            self.test_user['username'],
            new_password
        ) == True

    def test_change_password_wrong_old_password(self):
        """Test password change with wrong old password"""
        # Create user
        self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        # Try to change password with wrong old password
        result = self.auth_service.change_password(
            self.test_user['username'],
            'WrongPass123!',
            'NewPass123!'
        )

        assert result == False

    def test_generate_token(self):
        """Test token generation"""
        token = self.auth_service.generate_token(self.test_user['username'])
        assert token is not None
        assert isinstance(token, str)

    def test_verify_token_success(self):
        """Test successful token verification"""
        # Generate token
        token = self.auth_service.generate_token(self.test_user['username'])

        # Verify token
        result = self.auth_service.verify_token(token)
        assert result is not None
        assert result['username'] == self.test_user['username']

    def test_verify_token_invalid(self):
        """Test verification of invalid token"""
        result = self.auth_service.verify_token('invalid.token.here')
        assert result is None

    def test_reset_password_request(self):
        """Test password reset request"""
        # Create user
        self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        # Request password reset
        result = self.auth_service.reset_password(self.test_user['email'])
        assert result == True

    def test_reset_password_nonexistent_email(self):
        """Test password reset for nonexistent email"""
        result = self.auth_service.reset_password('nonexistent@example.com')
        assert result == False

    def test_get_user_settings(self):
        """Test getting user settings"""
        # Create user
        self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        settings = self.auth_service.get_user_settings(self.test_user['username'])
        assert isinstance(settings, dict)

    def test_update_user_settings(self):
        """Test updating user settings"""
        # Create user
        self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        # Update settings
        new_settings = {'theme': 'dark', 'notifications': True}
        result = self.auth_service.update_user_settings(
            self.test_user['username'],
            new_settings
        )

        assert result == True

        # Verify settings were updated
        settings = self.auth_service.get_user_settings(self.test_user['username'])
        assert settings.get('theme') == 'dark'
        assert settings.get('notifications') == True

    def test_delete_user_success(self):
        """Test successful user deletion"""
        # Create user
        self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        # Delete user
        result = self.auth_service.delete_user(
            self.test_user['username'],
            self.test_user['password']
        )

        assert result == True

        # Verify user is deleted
        assert self.auth_service.get_user_by_username(
            self.test_user['username']
        ) is None

    def test_delete_user_wrong_password(self):
        """Test user deletion with wrong password"""
        # Create user
        self.auth_service.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['email']
        )

        # Try to delete with wrong password
        result = self.auth_service.delete_user(
            self.test_user['username'],
            'WrongPass123!'
        )

        assert result == False

        # Verify user still exists
        assert self.auth_service.get_user_by_username(
            self.test_user['username']
        ) is not None


if __name__ == '__main__':
    pytest.main([__file__])