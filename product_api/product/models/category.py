from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    parent_category = models.ForeignKey(
        'self', related_name='subcategories', null=True, blank=True, on_delete=models.CASCADE
    )

    def get_subcategories(self):
        # This method returns all the subcategories under this category
        return self.subcategories.all()
   
    def __str__(self):
        return self.name
