from rest_framework import serializers
from product.models.product import Product
from product.models.product_image import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'caption'] 

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)  # Use 'many=True' to handle multiple images

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
