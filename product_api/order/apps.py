from django.apps import AppConfig

"""
Configuration for the 'order' application.

This class is used to configure the 'order' app within a Django project. It defines the default auto field for primary keys and the app's name.

Attributes:
    default_auto_field (str): Specifies the type of auto field to use for primary keys in models. In this case, it is set to `BigAutoField`, which is suitable for handling a large number of rows.
    name (str): The name of the app. This is set to 'order', which corresponds to the app's directory name.

Usage:
    This class should be placed in the `apps.py` file of the 'order' app and is automatically used by Django when the application is included in the `INSTALLED_APPS` setting.
"""


class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order"
