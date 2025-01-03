from django.test import TestCase
from django.contrib.auth import get_user_model
from product.models.product import Product
from product.models.product_wishlist import Wishlist
from product.models.category import Category

User = get_user_model()


class WishlistModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass123"
        )

        # Create a category
        self.category = Category.objects.create(name="Electronics")

        # Create two products
        self.product1 = Product.objects.create(
            name="Smartphone",
            description="A high-quality smartphone.",
            price=999.99,
            stock_quantity=10,
        )
        self.product1.categories.add(self.category)

        self.product2 = Product.objects.create(
            name="Laptop",
            description="A powerful laptop.",
            price=1999.99,
            stock_quantity=5,
        )
        self.product2.categories.add(self.category)

    def test_add_product_to_wishlist(self):
        """Test that a user can add a product to their wishlist."""
        wishlist_entry = Wishlist.objects.create(user=self.user, product=self.product1)
        self.assertEqual(Wishlist.objects.count(), 1)
        self.assertEqual(wishlist_entry.user, self.user)
        self.assertEqual(wishlist_entry.product, self.product1)

    def test_unique_user_product_constraint(self):
        """Test that a user cannot add the same product to their wishlist twice."""
        Wishlist.objects.create(user=self.user, product=self.product1)
        with self.assertRaises(Exception):
            Wishlist.objects.create(user=self.user, product=self.product1)

    def test_add_multiple_products_to_wishlist(self):
        """Test that a user can add multiple products to their wishlist."""
        Wishlist.objects.create(user=self.user, product=self.product1)
        Wishlist.objects.create(user=self.user, product=self.product2)
        self.assertEqual(Wishlist.objects.count(), 2)

    def test_str_representation(self):
        """Test the string representation of a wishlist entry."""
        wishlist_entry = Wishlist.objects.create(user=self.user, product=self.product1)
        self.assertEqual(
            str(wishlist_entry), f"Wishlist: {self.user.username} - {self.product1.name}"
        )
