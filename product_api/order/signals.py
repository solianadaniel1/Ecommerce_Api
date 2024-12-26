from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Order

"""
Signal receivers to adjust product stock when an order is created, updated, or deleted.

- `update_stock_on_order_save`: Updates the stock quantity when an order is created or updated.
- `update_stock_on_order_delete`: Restores the stock quantity when an order is deleted.

Signal Handlers:
    - post_save (Order): Triggered after an `Order` instance is saved.
    - post_delete (Order): Triggered after an `Order` instance is deleted.

Signal Handlers' Responsibilities:
    1. **update_stock_on_order_save**: 
        - If the order is newly created, it reduces the stock quantity of the ordered product by the quantity in the order, ensuring enough stock is available.
        - If the order is updated (quantity changed), it adjusts the stock based on the difference between the original quantity and the updated quantity.

    2. **update_stock_on_order_delete**:
        - When an order is deleted, the stock quantity of the associated product is increased by the order quantity, reflecting the reversal of the order.

Exceptions:
    - `ValueError`: Raised when there is insufficient stock to fulfill an order (for creation or update).
"""


# Adjust stock when an order is created or updated
@receiver(post_save, sender=Order)
def update_stock_on_order_save(sender, instance, created, **kwargs):
    product = instance.product
    if created:
        # Deduct stock for a new order
        if product.stock_quantity >= instance.quantity:
            product.stock_quantity -= instance.quantity
            product.save()
        else:
            raise ValueError("Not enough stock available.")
    else:
        # If order is updated, adjust stock accordingly
        original = sender.objects.get(pk=instance.pk)
        difference = instance.quantity - original.quantity
        if product.stock_quantity >= difference:
            product.stock_quantity -= difference
            product.save()
        else:
            raise ValueError("Not enough stock available.")


# Adjust stock when an order is deleted
@receiver(post_delete, sender=Order)
def update_stock_on_order_delete(sender, instance, **kwargs):
    product = instance.product
    product.stock_quantity += instance.quantity
    product.save()
