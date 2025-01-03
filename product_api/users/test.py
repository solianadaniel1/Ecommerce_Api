import uuid
from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class CustomUserModelTest(TestCase):

    def setUp(self):
        """Create user data with unique emails."""
        # Generate unique emails using UUID
        self.unique_email_user1 = f'user1{uuid.uuid4()}@example.com'
        self.unique_email_user2 = f'user2{uuid.uuid4()}@example.com'

        # Create user data for testing
        self.user_data1 = {
            'email': self.unique_email_user1,
            'username': 'user1',
            'password': 'password123'
        }
        self.user_data2 = {
            'email': self.unique_email_user2,
            'username': 'user2',
            'password': 'password123'
        }

    def test_create_user(self):
        """Test that a user is created with email and username."""
        user = get_user_model().objects.create_user(**self.user_data1)

        # Check user properties
        self.assertEqual(user.email, self.user_data1['email'])
        self.assertEqual(user.username, self.user_data1['username'])
        self.assertTrue(user.check_password(self.user_data1['password']))
        self.assertFalse(user.is_staff)  # By default, is_staff should be False
        self.assertFalse(user.is_superuser)  # By default, is_superuser should be False

    def test_create_user_without_email(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='password123', username='testuser')

    def test_create_user_without_username(self):
        """Test that creating a user without a username raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='testuser@example.com', password='password123', username='')

    def test_create_superuser(self):
        """Test that a superuser is created with the correct flags."""
        superuser = get_user_model().objects.create_superuser(**self.user_data2)

        # Check superuser properties
        self.assertEqual(superuser.email, self.user_data2['email'])
        self.assertEqual(superuser.username, self.user_data2['username'])
        self.assertTrue(superuser.check_password(self.user_data2['password']))
        self.assertTrue(superuser.is_staff)  # Superuser should have is_staff set to True
        self.assertTrue(superuser.is_superuser)  # Superuser should have is_superuser set to True
    
    def test_email_as_unique_identifier(self):
        """Test that the email is used as the unique identifier."""
        # Create first user with a unique email
        user1 = get_user_model().objects.create_user(**self.user_data1)

        # Create second user with a different unique email
        user2 = get_user_model().objects.create_user(**self.user_data2)

        # Assert the emails are unique
        self.assertEqual(user1.email, self.user_data1['email'])
        self.assertEqual(user2.email, self.user_data2['email'])
        self.assertNotEqual(user1.email, user2.email)  # Ensure emails are unique

        # Attempt to create a user with the same email as user1 (should raise a ValidationError)
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(email=self.user_data1['email'], password='password123', username='user3')

    def test_user_password_hashing(self):
        """Test that the password is properly hashed and cannot be retrieved in plaintext."""
        user = get_user_model().objects.create_user(**self.user_data1)
        
        # Ensure the password is hashed
        self.assertNotEqual(user.password, self.user_data1['password'])
        self.assertTrue(user.check_password(self.user_data1['password']))  # Check password verification
