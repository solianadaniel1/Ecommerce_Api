from django.test import TestCase
from order.models import Order
from apis.serializers.order_serializer import OrderSerializer
from product.models.product import Product
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

class TestOrderSerializer(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", username="testuser", password="password123"
        )

        # Create a product for the order
        self.product = Product.objects.create(
            name="Test Product", stock_quantity=10, price=100.00
        )

        # Create order data for testing
        self.order_data = {
            "product": self.product.id,
            "quantity": 1,
            "shipping_address": "123 street",
        }

        # Set up API request factory and request object
        self.factory = APIRequestFactory()
        self.request = self.factory.post("/orders/", data=self.order_data)
        self.request.user = self.user

    def test_order_serializer_stock_reduction(self):
        """
        Test that the stock quantity is reduced after saving the order.
        """
        # Pass the request in context
        serializer = OrderSerializer(data=self.order_data, context={"request": self.request})

        # Validate serializer
        self.assertTrue(serializer.is_valid(), f"Errors: {serializer.errors}")
        order = serializer.save()

        # Verify stock reduction
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 9)

    def test_order_serializer_total_price_calculation(self):
        """
        Test that the total price is correctly calculated.
        """
        # Pass the request in context
        serializer = OrderSerializer(data=self.order_data, context={"request": self.request})

        # Validate serializer
        self.assertTrue(serializer.is_valid(), f"Errors: {serializer.errors}")
        order = serializer.save()

        # Verify total price calculation
        self.assertEqual(order.total_price, self.product.price * self.order_data["quantity"])

    def test_order_serializer_with_valid_data(self):
        """
        Test the OrderSerializer with valid data to ensure an order is created.
        """
        # Pass the request in context
        serializer = OrderSerializer(data=self.order_data, context={"request": self.request})

        # Validate serializer
        self.assertTrue(serializer.is_valid(), f"Errors: {serializer.errors}")
        order = serializer.save()

        # Verify the order instance
        self.assertIsInstance(order, Order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, self.order_data["quantity"])

    def test_order_serializer_insufficient_stock(self):
        """
        Test that the serializer raises a validation error for insufficient stock.
        """
        # Modify order data to exceed stock
        self.order_data["quantity"] = 15

        # Pass the request in context
        serializer = OrderSerializer(data=self.order_data, context={"request": self.request})

        # Validate serializer
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]),
            f"Cannot order 15. Only {self.product.stock_quantity} left in stock."
        )

