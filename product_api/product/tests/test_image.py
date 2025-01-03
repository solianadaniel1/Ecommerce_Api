from django.test import TestCase
from product.models.product import Product
from product.models.product_image import ProductImage
from product.models.category import Category


class ProductImageModelTest(TestCase):
    def setUp(self):
        # Create a category
        self.category = Category.objects.create(name="Electronics")

        # Create a product
        self.product = Product.objects.create(
            name="Smartphone",
            description="A high-quality smartphone.",
            price=999.99,
            stock_quantity=10,
        )
        self.product.categories.add(self.category)

    def test_create_product_image(self):
        """Test that a product image can be created and is associated with the correct product."""
        product_image = ProductImage.objects.create(
            product=self.product, image="product_images/smartphone.jpg", caption="Front view"
        )
        self.assertEqual(ProductImage.objects.count(), 1)
        self.assertEqual(product_image.product, self.product)
        self.assertEqual(product_image.caption, "Front view")
        self.assertEqual(product_image.image, "product_images/smartphone.jpg")

    def test_multiple_images_for_product(self):
        """Test that multiple images can be associated with a single product."""
        ProductImage.objects.create(
            product=self.product, image="product_images/smartphone_front.jpg", caption="Front view"
        )
        ProductImage.objects.create(
            product=self.product, image="product_images/smartphone_back.jpg", caption="Back view"
        )
        self.assertEqual(ProductImage.objects.filter(product=self.product).count(), 2)

    def test_str_representation(self):
        """Test the string representation of a product image."""
        product_image = ProductImage.objects.create(
            product=self.product, image="product_images/smartphone.jpg", caption="Front view"
        )
        self.assertEqual(str(product_image), f"Image for {self.product.name}")
