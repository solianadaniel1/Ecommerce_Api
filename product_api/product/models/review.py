from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError

from product.models import Product

"""
Review model to represent product reviews in the system.

Fields:
    - user (ForeignKey): The user who submitted the review. It is a foreign key to the User model.
    - product (ForeignKey): The product being reviewed. It is a foreign key to the Product model.
    - rating (PositiveIntegerField): The rating given to the product, ranging from 1 to 5. It uses `RATING_CHOICES` for valid ratings.
    - comment (TextField): A text field for the user to provide their feedback on the product.
    - created_at (DateTimeField): The timestamp when the review was created.
    - updated_at (DateTimeField): The timestamp of the last update to the review.

Meta:
    - unique_together: Ensures that a user can only review a product once.

Methods:
    - __str__: Returns a string representation of the review in the format "Review for {product_name} by {user_username}".
    - clean: Validates the rating field to ensure it is between 1 and 5, raising a `ValidationError` if the rating is out of bounds.
"""


user = get_user_model()


class Review(models.Model):
    # Define rating choices
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1 to 5 ratings

    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES, default=1
    )  # Rating can be 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "user",
            "product",
        )  # To ensure a user can only review a product once

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

    def clean(self):
        """Override the clean method to validate the rating."""
        if not (1 <= self.rating <= 5):
            raise ValidationError("Rating must be between 1 and 5.")
