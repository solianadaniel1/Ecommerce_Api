from django.test import TestCase
from users.models import CustomUser
from apis.serializers.user_serializer import UserSerializer, RegisterSerializer


class TestUserSerializers(TestCase):
    def setUp(self):
        # Create a sample user for testing
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="testpassword123",
        )

        self.valid_register_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "securepassword",
        }

        self.invalid_register_data = {
            "email": "invaliduser",  # Invalid email format
            "username": "newuser",
            "password": "",
        }

    def test_user_serializer(self):
        """
        Test the UserSerializer to ensure it serializes user data correctly.
        """
        serializer = UserSerializer(instance=self.user)
        data = serializer.data

        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["username"], self.user.username)

    def test_register_serializer_with_valid_data(self):
        """
        Test the RegisterSerializer with valid data.
        """
        serializer = RegisterSerializer(data=self.valid_register_data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.email, self.valid_register_data["email"])
        self.assertEqual(user.username, self.valid_register_data["username"])
        self.assertTrue(user.check_password(self.valid_register_data["password"]))

    def test_register_serializer_with_invalid_data(self):
        """
        Test the RegisterSerializer with invalid data.
        """
        serializer = RegisterSerializer(data=self.invalid_register_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)

