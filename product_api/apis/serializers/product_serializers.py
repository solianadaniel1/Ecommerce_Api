from rest_framework import serializers

from product.models.product import Product
from product.models.product_image import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductImage model.

    This serializer converts ProductImage instances into JSON format
    and validates the input data for creating or updating product images.
    """

    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    This serializer converts Product instances into JSON format and
    handles validation for product fields like price, name, and stock quantity.
    It also includes the ability to handle multiple associated images via
    ProductImageSerializer.
    """

    images = ProductImageSerializer(
        many=True, required=False
    )  # Use 'many=True' to handle multiple images associated with the product

    class Meta:
        model = Product
        fields = "__all__"

    def validate_price(self, value):
        """
        Validate the price of the product.

        Ensures that the price is greater than zero.

        Args:
            value (float): The price of the product.

        Returns:
            float: The validated price.

        Raises:
            serializers.ValidationError: If the price is not greater than zero.
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_name(self, value):
        """
        Validate the name of the product.

        Ensures that the name is at least 3 characters long.

        Args:
            value (str): The name of the product.

        Returns:
            str: The validated product name.

        Raises:
            serializers.ValidationError: If the name is shorter than 3 characters.
        """
        if len(value) < 3:
            raise serializers.ValidationError(
                "Product name must be at least 3 characters long."
            )
        return value

    def validate_stock_quantity(self, value):
        """
        Validate the stock quantity of the product.

        Ensures that the stock quantity is a positive integer.

        Args:
            value (int): The stock quantity of the product.

        Returns:
            int: The validated stock quantity.

        Raises:
            serializers.ValidationError: If the stock quantity is not a positive integer.
        """
        if not isinstance(value, int) or value <= 0:
            raise serializers.ValidationError(
                "Stock Quantity must be a positive integer."
            )
        return value
