from rest_framework.test import APITestCase
from product.models.product import Product
from apis.serializers.product_serializers import ProductSerializer
from rest_framework import status

class ProductSerializerTest(APITestCase):
    def setUp(self):
        self.product_data = {
            'name': 'Product Name',
            'price': 10.0,
            'stock_quantity': 5,
            'description': 'this is a description'
        }

    def test_product_serializer_valid(self):
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid())  # Ensure the serializer is valid

    def test_product_serializer_invalid_name(self):
        invalid_data = self.product_data.copy()
        invalid_data['name'] = 'AB'  # Name too short
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())  # Ensure the serializer is invalid
        self.assertIn('name', serializer.errors)  # Check for name validation error

    def test_product_serializer_invalid_price(self):
        invalid_data = self.product_data.copy()
        invalid_data['price'] = -5  # Invalid price
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())  # Ensure the serializer is invalid
        self.assertIn('price', serializer.errors)  # Check for price validation error

    def test_product_serializer_invalid_stock_quantity(self):
        invalid_data = self.product_data.copy()
        invalid_data['stock_quantity'] = -1  # Invalid stock quantity
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())  # Ensure the serializer is invalid
        self.assertIn('stock_quantity', serializer.errors)  # Check for stock quantity validation error
