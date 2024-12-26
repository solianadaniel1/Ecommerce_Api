from django.db import models

"""
Category model to represent product categories with potential hierarchical relationships (parent-child categories).

Fields:
    - name (CharField): The name of the category, must be unique.
    - created_at (DateTimeField): Timestamp for when the category is created.
    - updated_at (DateTimeField): Timestamp for the last time the category was updated.
    - parent_category (ForeignKey): A self-referential foreign key to represent parent-child category relationships. Can be null if the category has no parent (i.e., it's a top-level category).

Methods:
    - get_subcategories: Returns all the subcategories under the current category.
    - __str__: Returns the name of the category for string representation.
"""


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    parent_category = models.ForeignKey(
        "self",
        related_name="subcategories",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def get_subcategories(self):
        # This method returns all the subcategories under this category
        return self.subcategories.all()

    def __str__(self):
        return self.name
