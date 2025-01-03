from django.test import TestCase
from django.contrib.auth import get_user_model
from product.models import Product
from product.models.review import Review
from django.core.exceptions import ValidationError

class ReviewModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )

        # Create a product
        self.product = Product.objects.create(
            name="Smartphone", description="A high-quality smartphone.", price=999.99, stock_quantity=10
        )

    def test_create_review(self):
        """Test that a review can be created and is associated with the correct user and product."""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment="Excellent product!"
        )
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent product!")


    def test_str_representation(self):
        """Test the string representation of the review."""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            comment="Good product."
        )
        self.assertEqual(str(review), "Review for Smartphone by testuser")

    def test_rating_validation(self):
        """Test that the rating field validates correctly."""
        invalid_review = Review(
            user=self.user,
            product=self.product,
            rating=6,  # Invalid rating (outside 1-5 range)
            comment="Invalid rating."
        )
        with self.assertRaises(ValidationError):
            invalid_review.clean()  # This should raise a ValidationError

        valid_review = Review(
            user=self.user,
            product=self.product,
            rating=3,  # Valid rating (within 1-5 range)
            comment="Valid rating."
        )
        try:
            valid_review.clean()  # This should not raise any errors
        except ValidationError:
            self.fail("Valid review raised a ValidationError")

