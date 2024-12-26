from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    This serializer handles the conversion of Order model instances
    to and from JSON format, validation for stock quantity, and the
    creation of an order. It also ensures that the total price is
    calculated correctly based on the quantity and product price.

    Methods:
        validate: Validates if the order quantity does not exceed the available stock.
        create: Creates a new order, ensuring sufficient stock and calculating the total price.
    """

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("total_price", "user")

    def validate(self, data):
        """
        Validate the order data to ensure the quantity does not exceed the available stock.

        This method checks if the quantity of the product ordered is less than or equal to
        the stock quantity of the product. If the quantity exceeds the stock, a validation error
        is raised with a relevant message.

        Args:
            data (dict): The validated order data, including product and quantity.

        Returns:
            dict: The validated order data.

        Raises:
            serializers.ValidationError: If the order quantity exceeds available stock.
        """
        product = data.get("product")
        quantity = data.get("quantity")

        if product and quantity:
            if quantity > product.stock_quantity:
                raise serializers.ValidationError(
                    f"Cannot order {quantity}. Only {product.stock_quantity} left in stock."
                )
        return data

    def create(self, validated_data):
        """
        Create a new order while ensuring the stock is updated and total price is calculated.

        This method creates an order instance after validating that there is enough stock
        for the product. It also calculates the total price of the order based on the quantity
        and product price and updates the stock quantity.

        Args:
            validated_data (dict): The validated data for the order, including product and quantity.

        Returns:
            Order: The created order instance.

        Raises:
            serializers.ValidationError: If there is not enough stock for the order.
        """
        user = self.context[
            "request"
        ].user  # Get the logged-in user from the request context
        product = validated_data["product"]
        quantity = validated_data["quantity"]

        # Check if there's enough stock for the product
        if product.stock_quantity < quantity:
            raise serializers.ValidationError(
                "Not enough stock available to fulfill this order."
            )

        # Reduce stock quantity
        product.stock_quantity -= quantity
        product.save()

        # Calculate the total price of the order (you can customize this logic)
        total_price = product.price * quantity
        validated_data["total_price"] = total_price
        validated_data["user"] = user
        # Create the order
        order = super().create(validated_data)

        return order
