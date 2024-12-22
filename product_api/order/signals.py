from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order

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
