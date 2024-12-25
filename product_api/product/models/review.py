from django.db import models
from django.forms import ValidationError

from product.models import Product
from django.contrib.auth import get_user_model

user = get_user_model()

class Review(models.Model):
    # Define rating choices
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1 to 5 ratings

    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=1)  # Rating can be 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    class Meta:
        unique_together = ('user', 'product')  # To ensure a user can only review a product once

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
    
    def clean(self):
            """Override the clean method to validate the rating."""
            if not (1 <= self.rating <= 5):
                raise ValidationError('Rating must be between 1 and 5.')