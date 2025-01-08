from rest_framework import status
from rest_framework.test import APITestCase

from apis.serializers.wishlist_serializer import WishlistSerializer
from product.models.product import Product
from product.models.product_wishlist import Wishlist
from users.models import CustomUser


class WishlistSerializerTest(APITestCase):
    def setUp(self):
        # Set up any necessary data for your test
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="testpassword", username="testuser"
        )
        self.product = Product.objects.create(
            name="Test Product", stock_quantity=10, price=10.0
        )

        # Create initial wishlist data
        self.wishlist_data = {"product": self.product.id}

    def test_readonly_fields(self):
        # Create a serializer instance with initial data
        serializer = WishlistSerializer(data=self.wishlist_data)

        # Validate the serializer
        self.assertTrue(serializer.is_valid())

        # Check that 'user', 'created_at', and 'updated_at' are not included in validated data
        validated_data = serializer.validated_data

        # Assert that these fields are not included in the validated data
        self.assertNotIn("user", validated_data)
        self.assertNotIn("created_at", validated_data)
        self.assertNotIn("updated_at", validated_data)

        # Ensure the serializer doesn't accept these fields from input data
        # Instead, the user field is automatically set, and created_at/updated_at are handled by ORM
        wishlist_item = serializer.save(
            user=self.user
        )  # Manually set the user in the save method

        # Ensure that the user is set correctly
        self.assertEqual(wishlist_item.user, self.user)

        # Ensure the created_at and updated_at fields are populated by the ORM
        self.assertIsNotNone(wishlist_item.created_at)
        self.assertIsNotNone(wishlist_item.updated_at)
