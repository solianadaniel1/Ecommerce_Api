from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from product.models import Product
from product.models.review import Review


class ReviewViewSetTest(APITestCase):

    def setUp(self):
        """
        Set up test data for authenticated user, product, and review.
        """
        # Create test users
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="password123", email="user1@example.com"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="password222", email="user2@example.com"
        )

        # Create a test product
        self.product = Product.objects.create(
            name="Test Product", price=100.00, stock_quantity=50
        )

        # Create JWT tokens for authentication
        self.token_user1 = RefreshToken.for_user(self.user1).access_token
        self.token_user2 = RefreshToken.for_user(self.user2).access_token

        # Create a review for user1
        self.review_data = {
            "rating": 4,
            "comment": "Good product.",
            "product": self.product.id,  # Use the product ID, not the instance
        }

    def test_create_review_authenticated(self):
        """
        Test creating a review for a product as an authenticated user.
        """
        url = "/api/reviews/"
        response = self.client.post(
            url, self.review_data, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["rating"], 4)
        self.assertEqual(response.data["comment"], "Good product.")

    def test_create_review_unauthenticated(self):
        """
        Test creating a review as an unauthenticated user.
        """
        url = "/api/reviews/"
        response = self.client.post(url, self.review_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_duplicate_review(self):
        """
        Test that a user cannot review the same product twice.
        """
        # First review creation
        url = "/api/reviews/"
        self.client.post(
            url, self.review_data, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )

        # Attempt to create a duplicate review
        response = self.client.post(
            url, self.review_data, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You have already reviewed product", str(response.data))

    def test_read_reviews(self):
        """
        Test that all users (authenticated and unauthenticated) can view reviews.
        """

        # Test reading reviews
        url = f"/api/reviews/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_review(self):
        """
        Test that a user can update their own review.
        """
        # Create a review for user1
        url = "/api/reviews/"
        response = self.client.post(
            url, self.review_data, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        review_id = response.data["id"]

        # Update the review
        update_data = {"rating": 5, "comment": "Updated comment."}
        url = f"/api/reviews/{review_id}/"
        response = self.client.patch(
            url, update_data, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["comment"], "Updated comment.")

    def test_update_other_user_review(self):
        """
        Test that a user cannot update another user's review.
        """
        # Create a review for user1
        url = "/api/reviews/"
        response = self.client.post(
            url, self.review_data, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        review_id = response.data["id"]

        # Try to update user1's review with user2's token
        update_data = {"rating": 5, "comment": "Updated comment."}
        url = f"/api/reviews/{review_id}/"
        response = self.client.put(
            url, update_data, HTTP_AUTHORIZATION=f"Bearer {self.token_user2}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_review(self):
        """
        Test that a user can delete their own review.
        """
        # Create a review for user1
        url = "/api/reviews/"
        response = self.client.post(
            url, self.review_data, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        review_id = response.data["id"]

        # Delete the review
        url = f"/api/reviews/{review_id}/"
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_user_review(self):
        """
        Test that a user cannot delete another user's review.
        """
        # Create a review for user1
        url = "/api/reviews/"
        response = self.client.post(
            url, self.review_data, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        review_id = response.data["id"]

        # Try to delete user1's review with user2's token
        url = f"/api/reviews/{review_id}/"
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token_user2}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
