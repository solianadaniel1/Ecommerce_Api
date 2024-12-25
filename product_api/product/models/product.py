from django.db import models
from product.models.category import Category

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image_url = models.ImageField(upload_to='product_image/', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name

