from django.db import models

from product.models.product import Product

"""
ProductImage model to store images associated with products.

Fields:
    - product (ForeignKey): A foreign key to the Product model, representing the product to which the image belongs.
    - image (ImageField): The image file uploaded for the product.
    - caption (CharField): An optional caption for the image. This field can be left blank or null.
    - created_at (DateTimeField): Timestamp for when the image was created.
    - updated_at (DateTimeField): Timestamp for when the image was last updated.

Methods:
    - __str__: Returns a string representation of the image, showing the product's name associated with the image.
"""


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="product_images/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.product.name}"