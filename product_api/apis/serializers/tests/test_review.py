from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apis.serializers.review_serializer import ReviewSerializer
from product.models import Product
from product.models.review import Review


class ReviewSerializerTest(APITestCase):

    def setUp(self):
        # Create test users
        self.user = get_user_model().objects.create_user(
            username="user1", password="password123", email="user1@example.com"
        )

        # Create a test product
        self.product = Product.objects.create(
            name="Test Product", price=100.00, stock_quantity=50
        )

        # Ensure there's no pre-existing review
        Review.objects.filter(user=self.user, product=self.product).delete()

        # Prepare the data to be used in serializer
        self.serializer_data = {
            "user": self.user.username,  # Expecting the username as the read-only field
            "product": self.product.id,  # Using the product ID
            "rating": 5,
            "comment": "Excellent product!",
        }

    def test_review_serializer_valid(self):
        """
        Test that the serializer works correctly with valid data.
        """
        # Create the review
        review = Review.objects.create(
            user=self.user, product=self.product, rating=5, comment="Excellent product!"
        )

        serializer = ReviewSerializer(instance=review)
        self.assertEqual(serializer.data["user"], self.user.email)
        self.assertEqual(serializer.data["product"], self.product.id)
        self.assertEqual(serializer.data["rating"], 5)
        self.assertEqual(serializer.data["comment"], "Excellent product!")

    def test_review_serializer_create(self):
        """
        Test creating a review using the serializer and ensuring it's saved correctly.
        Ensure only one review is allowed per product-user combination.
        """
        # Ensure there's no pre-existing review
        Review.objects.filter(user=self.user, product=self.product).delete()

        # Check if we can create a review using the serializer
        serializer = ReviewSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        review = serializer.save(user=self.user)  # Create the review with user context

        # Check that the review was saved with the correct values
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent product!")

        # Ensure only one review exists for this user-product combination
        duplicate_review = Review.objects.filter(
            user=self.user, product=self.product
        ).count()
        self.assertEqual(
            duplicate_review,
            1,
            "Duplicate review exists for this user-product combination.",
        )

    def test_review_serializer_invalid_rating(self):
        """
        Test that the serializer raises validation error for invalid rating.
        """
        invalid_data = {
            "user": self.user.username,
            "product": self.product.id,
            "rating": 10,  # Invalid rating, as it must be between 1 and 5
            "comment": "Product is okay.",
        }

        serializer = ReviewSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "rating", serializer.errors
        )  # The rating should raise a validation error
