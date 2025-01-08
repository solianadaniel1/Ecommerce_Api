from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSetTests(APITestCase):
    def setUp(self):
        # Create a superuser for testing admin functionality
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='password123',
            username="testuser",

        )
        # Create a regular user for testing
        self.regular_user = User.objects.create_user(
            email='user@example.com',
            password='password123',
            username="test2user",

        )

        # Generate JWT token for authentication
        self.admin_token = self.get_jwt_token(self.admin_user)
        self.regular_token = self.get_jwt_token(self.regular_user)

    def get_jwt_token(self, user):
        """
        Helper method to get JWT token for a user
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_user_viewset_admin_access(self):
        """
        Test that the User viewset is accessible by admin only
        """
        url = reverse('user-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_viewset_regular_user_access(self):
        """
        Test that regular users cannot access the User viewset
        """
        url = reverse('user-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_viewset_create_user(self):
        """
        Test that anyone can register a new user
        """
        url = reverse('register-list')
        data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'username':'testresgister',

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'newuser@example.com')

    def test_logout_view(self):
        """
        Test that logged-in users can log out by invalidating their refresh token
        """
        # Obtain the refresh token
        refresh_token = str(RefreshToken.for_user(self.regular_user))
        
        url = reverse('logout')
        data = {'refresh_token': refresh_token}

        # Make the POST request with the refresh token
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        
        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logged out successfully')


    def test_logout_view_no_token(self):
        """
        Test logout without a refresh token
        """
        url = reverse('logout')
        data = {}  # Missing refresh token
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Refresh token required', response.data['error'])

