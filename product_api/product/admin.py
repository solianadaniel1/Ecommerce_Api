from django.contrib import admin
from .models.product import Product
from .models.category import Category 


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'stock_quantity','price', 'display_categories']  # Display categories in the list view
    search_fields = ['name', 'stock_quantity', 'price', 'stock_quantity']
    list_filter = ['categories',]  # Allow filtering by categories in the sidebar
    readonly_fields = ['updated_date','created_date'] # Prevent manual editing

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Categories'  # Column header in the admin list view


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','parent_category')  # Show category name in the list view
    search_fields = ('name','parent_category')  # Add search functionality for categories
    readonly_fields = ('updated_at','created_at')  # Prevent manual editing

admin.site.register(Category, CategoryAdmin)