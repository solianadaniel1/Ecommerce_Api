from rest_framework.test import APITestCase
from rest_framework import status
from order.models import Order
from product.models import Product
from django.contrib.auth import get_user_model
from apis.serializers.order_serializer import OrderSerializer


class OrderSerializerTest(APITestCase):
    
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(username='testuser', password='password123', email="user1@example.com")

        # Create a product with stock quantity
        self.product = Product.objects.create(
            name='Test Product',
            price=100.0,
            stock_quantity=10,
        )

        # Authenticate the user
        self.client.login(email="user1@example.com", password='password123')  

        # The endpoint for creating orders
        self.url = '/api/orders/'

        # Prepare data for creating an order
        self.order_data = {
        'product': self.product.id,
        'quantity': 5,  
        'shipping_address': '123 Street Name' 
    }

    def test_order_serializer_valid(self):
        """
        Test creating an order with valid data (sufficient stock).
        """
        # Create an order using serializer
        serializer = OrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid())

        order = serializer.save(user=self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 5)
        self.assertEqual(order.total_price, self.product.price * 5)

    def test_order_serializer_create(self):
        """
        Test creating an order using the serializer and ensuring it's saved correctly.
        Ensure sufficient stock is available.
        """
        # Check if we can create an order using the serializer
        serializer = OrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save(user=self.user)  # Create the order with user context

        # Check that the order was saved with the correct values
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 5)
        self.assertEqual(order.total_price, self.product.price * 5)

    def test_order_serializer_invalid_stock(self):
        """
        Test that the serializer raises a validation error for stock exceeding the available quantity.
        """
        invalid_data = {
            'product': self.product.id,
            'quantity': 20,  # Invalid quantity, more than the available stock
            'shipping_address': '123 Street Name' 

        }

        serializer = OrderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('detail', serializer.errors)  # Ensure a stock validation error is raised
        self.assertEqual(
            str(serializer.errors['detail'][0]),
            'Not enough stock available to fulfill this order.'
        )

    def test_order_serializer_invalid_total_price(self):
        """
        Test that the serializer correctly calculates the total price.
        """
        invalid_data = {
            'product': self.product.id,
            'quantity': 3 , # Should calculate total price as 3 * 100 = 300
            'shipping_address': '123 Street Name' 

        }

        serializer = OrderSerializer(data=invalid_data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save(user=self.user)
        self.assertEqual(order.total_price, self.product.price * 3)

    def test_order_serializer_unauthenticated_user(self):
        """
        Test that an unauthenticated user cannot create an order.
        """
        # Log out the user to simulate an unauthenticated request
        self.client.logout()

        data = {
            'product': self.product.id,
            'quantity': 2,
            'shipping_address': '123 Street Name' 

        }
        response = self.client.post(self.url, data, format='json')

        # Check that the unauthenticated user receives a 401 Unauthorized error
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_serializer_duplicate_order(self):
        """
        Test that the serializer raises a validation error when creating duplicate orders for the same user-product combination.
        """
        # Create an order first
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=3,
            total_price=self.product.price * 3
        )

        # Try to create a duplicate order
        duplicate_data = {
            'product': self.product.id,
            'quantity': 3,
            'shipping_address': '123 Street Name' 

        }

        serializer = OrderSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('detail', serializer.errors)
        self.assertEqual(
            str(serializer.errors['detail'][0]),
            'You have already ordered this product.'
        )
