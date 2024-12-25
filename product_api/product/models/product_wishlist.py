from django.db import models
from django.contrib.auth import get_user_model
from product.models.product import Product  

user = get_user_model()

class Wishlist(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')  # Ensure a user can only add the same product once to the wishlist

    def __str__(self):
        return f"Wishlist: {self.user.username} - {self.product.name}"
