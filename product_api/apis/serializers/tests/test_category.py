from rest_framework.test import APITestCase

from apis.serializers.category_serializer import CategorySerializer
from product.models.category import Category


class TestCategorySerializer(APITestCase):
    def setUp(self):
        # Create a sample category for testing
        self.valid_data = {"name": "Books"}
        self.invalid_data = {"name": "A"}

    def test_serializer_with_valid_data(self):
        """
        Test that the serializer is valid with proper data.
        """
        serializer = CategorySerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], self.valid_data["name"])

    def test_serializer_with_invalid_name(self):
        """
        Test that the serializer raises a validation error for a short name.
        """
        serializer = CategorySerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(
            serializer.errors["name"][0],
            "Category name must be at least 3 characters long",
        )

    def test_serializer_save(self):
        """
        Test that the serializer can save a valid object.
        """
        serializer = CategorySerializer(data=self.valid_data)
        if serializer.is_valid():
            category = serializer.save()
            self.assertIsInstance(category, Category)
            self.assertEqual(category.name, self.valid_data["name"])
