from rest_framework import serializers
from order.models import Order
from product.models.product import Product

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total_price', 'user', 'order_status') 

    def validate(self, data):
        """
        Validate if the order quantity does not exceed stock.
        """
        product = data.get('product')
        quantity = data.get('quantity')

        if product and quantity:
            if quantity > product.stock_quantity:
                raise serializers.ValidationError(
                    f"Cannot order {quantity}. Only {product.stock_quantity} left in stock."
                )
        return data

    def create(self, validated_data):
            
            user = self.context['request'].user  # Get the logged-in user from the request context
            product = validated_data['product']
            quantity = validated_data['quantity']

            # Check if there's enough stock for the product
            if product.stock_quantity < quantity:
                raise serializers.ValidationError("Not enough stock available to fulfill this order.")

            # Reduce stock quantity
            product.stock_quantity -= quantity
            product.save()

            # Calculate the total price of the order (you can customize this logic)
            total_price = product.price * quantity
            validated_data['total_price'] = total_price
            validated_data['user'] = user
            # Create the order
            order = super().create(validated_data)

            return order