from django.test import TestCase
from order.models import Order
from apis.serializers.order_serializer import OrderSerializer
from product.models.product import Product
from django.contrib.auth import get_user_model

class TestOrderSerializer(TestCase):
    def setUp(self):
        # Create a test custom user (replace with your CustomUser model)
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", username="testuser", password="password123"
        )

        # Create a product for the order
        self.product = Product.objects.create(
            name="Test Product", stock_quantity=10, price=100.00
        )

        # Create order data for testing
        self.order_data = {
            "user": self.user.id,  # Use the CustomUser instance
            "product": self.product.id,
            "quantity": 1,
            "shipping_address": '123 street'

        }

    def test_order_serializer_stock_reduction(self):
        """
        Test that the stock quantity is correctly reduced when an order is created.
        """
        # Simplified test data
        order_data = {
            "user": self.user.id,  # Assuming self.user is a valid user instance
            "product": self.product.id,  # Assuming self.product is a valid product instance
            "quantity": 1 , # Ensure valid quantity
            "shipping_address": '123 street'

        }
        
        # Create serializer instance with simplified data
        serializer = OrderSerializer(data=order_data)
        
        # Validate the data
        if serializer.is_valid():
            order = serializer.save()  # Save the order
            self.product.refresh_from_db()  # Refresh product to check updated stock
            self.assertEqual(self.product.stock_quantity, 9)  # Expect stock to be reduced by 1
        else:
            self.fail(f"Serializer failed to validate data: {serializer.errors}")


    def test_order_serializer_total_price_calculation(self):
        """
        Test that the total price is correctly calculated.
        """
        # Simplified test data
        order_data = {
            "user": self.user.id,
            "product": self.product.id,
            "quantity": 1,
            "shipping_address": '123 street'

        }

        # Create serializer instance with simplified data
        serializer = OrderSerializer(data=order_data)

        # Validate the data
        if serializer.is_valid():
            order = serializer.save()
            # Assuming 'total_price' is a field that calculates price based on quantity
            self.assertEqual(order.total_price, self.product.price * 1)  # Assuming product price is multiplied by quantity
        else:
            self.fail(f"Serializer failed to validate data: {serializer.errors}")

    def test_order_serializer_with_valid_data(self):
        """
        Test the OrderSerializer with valid data.
        """
        # Simplified test data
        order_data = {
            "user": self.user.id,
            "product": self.product.id,
            "quantity": 1,
            "shipping_address": '123 street'
        }

        # Create serializer instance with simplified data
        serializer = OrderSerializer(data=order_data)

        # Validate the data
        if serializer.is_valid():
            order = serializer.save()  # Save the order
            self.assertIsInstance(order, Order)  # Ensure the order instance is created
        else:
            self.fail(f"Serializer failed to validate data: {serializer.errors}")
