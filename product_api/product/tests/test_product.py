from django.test import TestCase
from product.models.product import Product
from product.models.category import Category
from django.utils.timezone import now


class ProductModelTest(TestCase):
    def setUp(self):
        # Create categories for testing
        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Appliances")

        # Create a product for testing
        self.product = Product.objects.create(
            name="Test Product",
            description="This is a test product description.",
            price=99.99,
            stock_quantity=10,
        )
        self.product.categories.add(self.category1, self.category2)

    def test_product_creation(self):
        """Test that the product is created with the correct attributes."""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "This is a test product description.")
        self.assertEqual(self.product.price, 99.99)
        self.assertEqual(self.product.stock_quantity, 10)
        self.assertIsNotNone(self.product.created_date)
        self.assertIsNotNone(self.product.updated_date)

    def test_product_string_representation(self):
        """Test the string representation of the product."""
        self.assertEqual(str(self.product), "Test Product")

    def test_product_categories(self):
        """Test that the product is associated with the correct categories."""
        categories = self.product.categories.all()
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)
        self.assertEqual(categories.count(), 2)

    def test_updated_date_changes_on_save(self):
        """Test that the updated_date field is updated when the product is modified."""
        original_updated_date = self.product.updated_date
        self.product.name = "Updated Product Name"
        self.product.save()
        self.product.refresh_from_db()  # Refresh the object to get the latest data from the database
        self.assertNotEqual(original_updated_date, self.product.updated_date)

    def test_product_without_categories(self):
        """Test that a product can be created without categories."""
        product_without_category = Product.objects.create(
            name="Uncategorized Product",
            description="This product has no categories.",
            price=50.00,
            stock_quantity=5,
        )
        self.assertEqual(product_without_category.categories.count(), 0)
