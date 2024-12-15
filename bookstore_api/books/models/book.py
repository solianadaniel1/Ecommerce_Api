from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    published_date = models.DateField()
    pages = models.PositiveIntegerField()
    cover_image_url = models.URLField()

    def __str__(self):
        return self.title
