from django.apps import AppConfig

"""
Django App Configuration for the 'product' app.

This class defines the configuration for the 'product' app, which handles all aspects related to products
such as their attributes, categories, reviews, and wishlists.

Attributes:
    - default_auto_field: Specifies the default type of primary key field to use for model fields.
      The default is set to BigAutoField, which is a 64-bit integer that auto-increments.
    - name: Specifies the name of the app, which is 'product'. This is the app that contains the models,
      views, and other related components for handling products.

This configuration class is automatically used by Django when the application is started to set up
the necessary app configurations and model behaviors.
"""


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product"
