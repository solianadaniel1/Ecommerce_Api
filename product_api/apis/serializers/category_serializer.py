from rest_framework import serializers
from product.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

 # Field-level validation for 'price'
    def validate_name(self, value):
        if value <= 0:
            raise serializers.ValidationError("Category name must be at least 3 characters long")
        return value
