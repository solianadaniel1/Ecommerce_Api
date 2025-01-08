from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from product.models.product import Product
from product.models.product_wishlist import Wishlist


class WishlistViewSetTestCase(APITestCase):
    """
    Test suite for the WishlistViewSet.
    """

    def setUp(self):
        # Set up a test user and authenticate them
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", username="testuser", password="password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a test product
        self.product = Product.objects.create(
            name="Test Product", stock_quantity=10, price=50.00
        )

        # URL for the wishlist viewset
        self.wishlist_url = "/api/wishlist/"

    def test_add_product_to_wishlist(self):
        """
        Test adding a product to the wishlist.
        """
        response = self.client.post(self.wishlist_url, {"product": self.product.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Wishlist.objects.filter(user=self.user, product=self.product).exists()
        )

    def test_add_duplicate_product_to_wishlist(self):
        """
        Test adding the same product to the wishlist twice.
        """
        # Add product once
        self.client.post(self.wishlist_url, {"product": self.product.id})

        # Attempt to add it again
        response = self.client.post(self.wishlist_url, {"product": self.product.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This product is already in your wishlist.", response.data)

    def test_add_nonexistent_product_to_wishlist(self):
        """
        Test adding a non-existent product to the wishlist.
        """
        response = self.client.post(self.wishlist_url, {"product": 999})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Product not found.", response.data)

    def test_view_wishlist(self):
        """
        Test viewing the user's wishlist.
        """
        # Add a product to the wishlist
        Wishlist.objects.create(user=self.user, product=self.product)

        response = self.client.get(self.wishlist_url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_product_from_wishlist(self):
        """
        Test removing a product from the wishlist.
        """
        # Add a product to the wishlist
        wishlist_item = Wishlist.objects.create(user=self.user, product=self.product)

        response = self.client.delete(f"{self.wishlist_url}{wishlist_item.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Wishlist.objects.filter(user=self.user, product=self.product).exists()
        )

    def test_remove_other_user_wishlist_item(self):
        """
        Test removing a wishlist item that belongs to another user.
        """
        # Create another user and their wishlist item
        other_user = get_user_model().objects.create_user(
            email="otheruser@example.com", username="otheruser", password="password123"
        )
        wishlist_item = Wishlist.objects.create(user=other_user, product=self.product)

        response = self.client.delete(f"{self.wishlist_url}{wishlist_item.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Wishlist.objects.filter(id=wishlist_item.id).exists())
