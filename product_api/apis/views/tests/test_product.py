from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from product.models import Category, Product


class ProductViewSetTest(APITestCase):
    def setUp(self):
        """
        Set up the test environment. Create users, categories, and products.
        """
        # Create users
        self.user1 = get_user_model().objects.create_superuser(
            username="user1", email="user1@example.com", password="password123"
        )
        self.user2 = get_user_model().objects.create_superuser(
            username="user2", email="user2@example.com", password="password123"
        )

        # Create categories
        self.category1 = Category.objects.create(name="Category1")
        self.category2 = Category.objects.create(name="Category2")

        # Create products
        self.product1 = Product.objects.create(
            name="Product1", price=100, stock_quantity=2
        )
        self.product2 = Product.objects.create(
            name="Product2", price=200, stock_quantity=3
        )
        self.product3 = Product.objects.create(
            name="Product3", price=300, stock_quantity=4
        )

        # Assign categories to products
        self.product1.categories.add(self.category1, self.category2)
        self.product2.categories.add(self.category1)

        # Obtain tokens for users
        self.token_user1 = RefreshToken.for_user(self.user1).access_token
        self.token_user2 = RefreshToken.for_user(self.user2).access_token

    def test_create_product(self):
        """
        Test creating a product. Only authenticated users can create products.
        """
        url = "/api/products/"
        data = {
            "name": "New Product",
            "price": 150,
            "stock_quantity": 10,
            "description": "tech",
            "categories": [
                self.category1.id
            ],  # Assigning categories to the new product
        }

        # Test creation for authenticated user (admin or authorized user)
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_access_permissions(self):
        """
        Test that users can access products but only admins can create/update/delete.
        """
        url = f"/api/products/{self.product1.id}/"

        # Test user1 (authenticated) accessing a product
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test user2 (authenticated) accessing the product
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token_user2}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        """
        Test updating a product. Only admins can update products.
        """
        url = f"/api/products/{self.product1.id}/"
        data = {
            "name": "Updated Product",
            "price": 120,
            "stock_quantity": 15,
        }

        # Test user1 (admin or authorized) updating the product
        response = self.client.patch(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        """
        Test deleting a product. Only admins can delete products.
        """
        url = f"/api/products/{self.product1.id}/"

        # Test user1 (admin or authorized) deleting the product
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Test user2 trying to delete the product that doesn't exist
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token_user2}"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_products(self):
        """
        Test retrieving a list of products.
        """
        url = "/api/products/"

        # Test retrieving products for authenticated user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure products exist in response

    def test_filter_products(self):
        """
        Test filtering products by price or other attributes.
        """
        url = "/api/products/?search=Product1"

        # Test filtering products by name
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token_user1}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
