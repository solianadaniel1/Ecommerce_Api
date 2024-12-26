from django.contrib.auth import get_user_model
from django.db import models

from product.models.product import Product

"""
Represents an Order within the e-commerce system.

Attributes:
    user (ForeignKey): A reference to the User model, indicating the customer who placed the order. It can be set to `null` and will use `SET_NULL` when deleted.
    product (ForeignKey): A reference to the Product model, indicating the product being ordered. It can be set to `null` and will use `SET_NULL` when deleted.
    quantity (PositiveIntegerField): The number of units of the product being ordered. Defaults to 1.
    total_price (DecimalField): The total cost of the order, stored as a decimal with a maximum of 10 digits and 2 decimal places.
    shipping_address (TextField): The address to which the order will be shipped.
    order_status (CharField): The current status of the order. Choices include 'Pending', 'Payment_Confirmed', 'Shipped', 'Delivered', 'Canceled', 'Refunded'. Defaults to 'Pending'.
    created_at (DateTimeField): Timestamp indicating when the order was created.
    updated_at (DateTimeField): Timestamp indicating the last update time of the order.

Methods:
    __str__(): Returns a string representation of the order, including the order ID, user, and product name.
"""

user = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        user, on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()

    # Order status (choices could be 'Pending', 'Shipped', 'Delivered', etc.)
    ORDER_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Payment_Confirmed", "Payment_Confirmed"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Canceled", "Canceled"),
        ("Refunded", "Refunded"),
    ]
    order_status = models.CharField(
        max_length=50, choices=ORDER_STATUS_CHOICES, default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user} for {self.product.name}"
