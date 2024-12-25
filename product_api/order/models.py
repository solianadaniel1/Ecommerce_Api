from django.db import models
from django.conf import settings
from product.models.product import Product
from django.contrib.auth import get_user_model

user = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()

    # Order status (choices could be 'Pending', 'Shipped', 'Delivered', etc.)
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Payment_Confirmed', 'Payment_Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
        ('Refunded', 'Refunded'),
    ]
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user} for {self.product.name}"

   