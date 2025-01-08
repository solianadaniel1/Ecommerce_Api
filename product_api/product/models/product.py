from django.db import models

from product.models.category import Category

"""
Product model to represent products in the system.

Fields:
    - name (CharField): The name of the product. It is unique across all products.
    - image_url (ImageField): An optional field to store the product's image. The image is uploaded to 'product_image/' directory.
    - description (TextField): A detailed description of the product.
    - price (DecimalField): The price of the product, with a maximum of 10 digits and 2 decimal places.
    - stock_quantity (PositiveIntegerField): The quantity of the product available in stock.
    - created_date (DateTimeField): The timestamp of when the product was created.
    - updated_date (DateTimeField): The timestamp of the last update made to the product.
    - categories (ManyToManyField): A many-to-many relationship to the Category model, allowing a product to belong to multiple categories.

Methods:
    - __str__: Returns the name of the product as the string representation of the product.
"""


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name
