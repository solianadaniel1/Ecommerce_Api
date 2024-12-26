from django.contrib import admin

from .models import Order

"""
Admin configuration for the Order model.

This class defines the settings for displaying and interacting with the Order model in the Django admin interface.

Attributes:
    list_display (list): Fields to be displayed in the list view of the Order model in the admin interface.
    search_fields (list): Fields that can be searched in the admin search bar.
    list_filter (list): Fields that can be used to filter the orders in the admin interface.
    readonly_fields (list): Fields that are read-only in the admin interface and cannot be edited.

Usage:
    Register this `OrderAdmin` class with the `Order` model in the Django admin to customize its display and functionality.
"""


class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity", "order_status", "shipping_address"]
    search_fields = ["user", "product", "quantity", "order_status", "shipping_address"]
    list_filter = ["user", "product", "order_status"]
    readonly_fields = ["updated_at", "created_at"]


admin.site.register(Order, OrderAdmin)
