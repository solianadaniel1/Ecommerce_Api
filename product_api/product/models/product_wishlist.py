from django.contrib.auth import get_user_model
from django.db import models

from product.models.product import Product

"""
Wishlist model to store products added to a user's wishlist.

Fields:
    - user (ForeignKey): A foreign key to the User model, representing the user who added the product to the wishlist.
    - product (ForeignKey): A foreign key to the Product model, representing the product added to the user's wishlist.
    - created_at (DateTimeField): Timestamp for when the product was added to the wishlist.
    - updated_at (DateTimeField): Timestamp for when the wishlist entry was last updated.

Meta:
    - unique_together: Ensures that a user can only add the same product to their wishlist once.

Methods:
    - __str__: Returns a string representation of the wishlist entry, showing the user's username and the product's name.
"""

user = get_user_model()


class Wishlist(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlists"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "user",
            "product",
        )  # Ensure a user can only add the same product once to the wishlist

    def __str__(self):
        return f"Wishlist: {self.user.username} - {self.product.name}"
