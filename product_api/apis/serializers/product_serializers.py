from rest_framework import serializers
from product.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

 # Field-level validation for 'price'
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    # Field-level validation for 'name'
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Product name must be at least 3 characters long.")
        return value
    
    def validate_stock_quantity(self, value):
        if not isinstance(value, int) or value <= 0:
            raise serializers.ValidationError("Stock Quantity must be a positive integer.")
        return value
