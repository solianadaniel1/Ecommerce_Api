from django.contrib import admin
from django.contrib.auth import get_user_model

"""
Custom Django Admin configuration for the User model.

This class provides customizations for the display and functionality of the User model in the Django admin interface.
It is used to manage and configure how user-related data is presented and interacted with in the admin panel.

Attributes:
    - list_display: Specifies the fields to display in the admin list view for the User model.
      In this case, the 'username' and 'email' fields are displayed.
    - search_fields: Defines the fields by which admin users can search for users in the admin interface.
      Here, 'username' and 'email' are searchable fields.
    - list_filter: Allows filtering the list of users by the 'username' and 'email' fields in the sidebar.

The `UserAdmin` class is registered with Django's admin site to customize the behavior and appearance of the User model in the admin interface.
"""

user = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]
    search_fields = ["username", "email"]
    list_filter = ["username", "email"]


admin.site.register(user, UserAdmin)
