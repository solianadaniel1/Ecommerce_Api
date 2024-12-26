from django.contrib import admin

from .models.category import Category
from .models.product import Product
from .models.product_wishlist import Wishlist
from .models.review import Review

"""
Django Admin configuration for the Product, Category, Review, and Wishlist models.

This module defines the admin interface for the Product, Category, Review, and Wishlist models,
enabling the ability to manage these models directly from the Django Admin panel.

Models:
    - Product: Represents products in the system with attributes like name, stock quantity, price, and categories.
    - Category: Represents product categories and their relationships with subcategories.
    - Review: Represents user reviews for products, including ratings and comments.
    - Wishlist: Represents the wishlist of users, which allows users to save products they are interested in.

Admin Configurations:
    - ProductAdmin: Customizes the admin interface for the Product model.
        - Displays the product name, stock quantity, price, and associated categories in the list view.
        - Allows search and filtering by product attributes and categories.
        - Prevents editing of created and updated dates.

    - CategoryAdmin: Customizes the admin interface for the Category model.
        - Displays the category name and its parent category in the list view.
        - Allows search and filtering by category attributes.
        - Prevents editing of created and updated dates.

    - ReviewAdmin: Customizes the admin interface for the Review model.
        - Displays the associated product, rating, and comment in the list view.
        - Allows search and filtering by review attributes such as rating and product name.
        - Prevents editing of created and updated dates.

    - WishlistAdmin: Customizes the admin interface for the Wishlist model.
        - Displays the user and product in the list view.
        - Allows search and filtering by user and product attributes.
        - Prevents editing of created and updated dates.

Each model has specific customizations for how it appears and behaves in the Django Admin interface, providing an enhanced user experience when managing data for the application.
"""


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "stock_quantity",
        "price",
        "display_categories",
    ]  # Display categories in the list view
    search_fields = ["name", "stock_quantity", "price", "stock_quantity"]
    list_filter = ["categories"]  # Allow filtering by categories in the sidebar
    readonly_fields = ["updated_date", "created_date"]  # Prevent manual editing

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    display_categories.short_description = (
        "Categories"  # Column header in the admin list view
    )


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_category")  # Show category name in the list view
    search_fields = (
        "name",
        "parent_category",
    )  # Add search functionality for categories
    list_filter = ["name"]  # Allow filtering by categories in the sidebar
    readonly_fields = ("updated_at", "created_at")  # Prevent manual editing


admin.site.register(Category, CategoryAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "rating",
        "comment",
    )  # Show review products in the list view
    search_fields = (
        "product",
        "rating",
        "comment",
    )  # Add search functionality for review
    list_filter = ["rating", "product__name"]
    readonly_fields = ("updated_at", "created_at")  # Prevent manual editing


admin.site.register(Review, ReviewAdmin)


class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product")  # Show wishlist products in the list view
    search_fields = ("user", "product")  # Add search functionality for wishlist
    list_filter = ["product__name"]  # to filter we should use the double underscore(__)
    readonly_fields = ("updated_at", "created_at")  # Prevent manual editing


admin.site.register(Wishlist, WishlistAdmin)
