from django.test import TestCase

from product.models.category import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        # Create top-level categories
        self.electronics = Category.objects.create(name="Electronics")
        self.fashion = Category.objects.create(name="Fashion")

        # Create subcategories for Electronics
        self.phones = Category.objects.create(
            name="Phones", parent_category=self.electronics
        )
        self.laptops = Category.objects.create(
            name="Laptops", parent_category=self.electronics
        )

        # Create subcategories for Fashion
        self.men_clothing = Category.objects.create(
            name="Men's Clothing", parent_category=self.fashion
        )
        self.women_clothing = Category.objects.create(
            name="Women's Clothing", parent_category=self.fashion
        )

    def test_category_creation(self):
        """Test that categories are created successfully."""
        self.assertEqual(Category.objects.count(), 6)

    def test_parent_category(self):
        """Test that parent-child relationships are established correctly."""
        self.assertEqual(self.phones.parent_category, self.electronics)
        self.assertEqual(self.laptops.parent_category, self.electronics)
        self.assertEqual(self.men_clothing.parent_category, self.fashion)
        self.assertEqual(self.women_clothing.parent_category, self.fashion)

    def test_get_subcategories(self):
        """Test that subcategories are retrieved correctly."""
        electronics_subcategories = self.electronics.get_subcategories()
        fashion_subcategories = self.fashion.get_subcategories()

        self.assertIn(self.phones, electronics_subcategories)
        self.assertIn(self.laptops, electronics_subcategories)
        self.assertIn(self.men_clothing, fashion_subcategories)
        self.assertIn(self.women_clothing, fashion_subcategories)

    def test_str_method(self):
        """Test the string representation of the Category model."""
        self.assertEqual(str(self.electronics), "Electronics")
        self.assertEqual(str(self.fashion), "Fashion")
        self.assertEqual(str(self.phones), "Phones")
