from django.apps import AppConfig

"""
Django App configuration for the 'users' app.

This class provides configuration for the 'users' app within a Django project.
It specifies how the app should be handled by Django's application registry.

Attributes:
    - default_auto_field: Sets the default type for auto-incrementing primary keys to 'BigAutoField',
      which uses a 64-bit integer to represent unique IDs.
    - name: Defines the name of the app as 'users', which is used to identify the app within the Django project.

This configuration class ensures that Django correctly initializes and manages the 'users' app during startup.
"""


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
