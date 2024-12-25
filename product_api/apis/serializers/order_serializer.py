from django.forms import ValidationError
from rest_framework import serializers
from order.models import Order
from product.models.product import Product
from rest_framework.exceptions import APIException

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total_price', 'user') 


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
    

    # def change_status(self, new_status):
    #         """
    #         Change the order status with the defined transition rules.
    #         """
    #         print(f"Current status: {self.order_status}, New status: {new_status}")
    #         valid_transitions = {
    #             'Pending': ['Payment Confirmed', 'Canceled'],
    #             'Payment Confirmed': ['Shipped', 'Canceled'],
    #             'Shipped': ['Out for Delivery', 'Canceled'],
    #             'Out for Delivery': ['Delivered'],
    #             'Delivered': [],
    #             'Canceled': ['Refunded'],
    #             'Refunded': [],
    #         }

    #         # Check if the new status is a valid transition
    #         if new_status not in valid_transitions.get(self.order_status, []):
    #             raise ValidationError(f"Invalid transition from {self.order_status} to {new_status}.")

    #         # Update order status and save
    #         self.order_status = new_status
    #         self.save()
    #         return self

