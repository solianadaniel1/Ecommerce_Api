# Create your tests here.
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from product.models import Product

from .models import Order


class OrderModelTest(TestCase):
    def setUp(self):
        """Set up initial test data."""
        # Create a user
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="password123", username="user1"
        )

        # Create a product
        self.product = Product.objects.create(
            name="Test Product",
            description="Test product description",
            price=Decimal("99.99"),
            stock_quantity=100,
        )

        # Create an order
        self.order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
            total_price=Decimal("199.98"),  # 2 * 99.99
            shipping_address="123 Test St, Test City, Test Country",
        )

    def test_order_creation(self):
        """Test that the order is created successfully."""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.product, self.product)
        self.assertEqual(self.order.quantity, 2)
        self.assertEqual(self.order.total_price, Decimal("199.98"))
        self.assertEqual(
            self.order.shipping_address, "123 Test St, Test City, Test Country"
        )
        self.assertEqual(self.order.order_status, "Pending")
        self.assertIsNotNone(self.order.created_at)
        self.assertIsNotNone(self.order.updated_at)

    def test_order_status_choices(self):
        """Test that the order status choices are correct."""
        valid_statuses = [
            "Pending",
            "Payment_Confirmed",
            "Shipped",
            "Delivered",
            "Canceled",
            "Refunded",
        ]
        for status in valid_statuses:
            order = Order.objects.create(
                user=self.user,
                product=self.product,
                quantity=1,
                total_price=Decimal("99.99"),
                shipping_address="123 Test St, Test City, Test Country",
                order_status=status,
            )
            self.assertEqual(order.order_status, status)

    def test_str_method(self):
        """Test the string representation of the order."""
        expected_str = f"Order #{self.order.id} by {self.user} for {self.product.name}"
        self.assertEqual(str(self.order), expected_str)

    def test_order_total_price(self):
        """Test that the total price is calculated correctly based on quantity and product price."""
        self.assertEqual(
            self.order.total_price, self.product.price * self.order.quantity
        )

    def test_order_status_default(self):
        """Test that the default order status is 'Pending'."""
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
            total_price=self.product.price,
            shipping_address="123 Test St, Test City, Test Country",
        )
        self.assertEqual(order.order_status, "Pending")

    def test_order_with_null_user(self):
        """Test that an order can be created with a null user."""
        order = Order.objects.create(
            user=None,
            product=self.product,
            quantity=1,
            total_price=self.product.price,
            shipping_address="123 Test St, Test City, Test Country",
        )
        self.assertIsNone(order.user)

    def test_order_with_null_product(self):
        """Test that an order can be created with a null product."""
        order = Order.objects.create(
            user=self.user,
            product=None,
            quantity=1,
            total_price=self.product.price,
            shipping_address="123 Test St, Test City, Test Country",
        )
        self.assertIsNone(order.product)
