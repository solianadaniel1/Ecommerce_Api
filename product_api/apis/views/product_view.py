from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication

from apis.permissions import IsAdminOrReadOnly
from apis.serializers.product_serializers import (ProductImageSerializer,
                                                  ProductSerializer)
from product.models import Category
from product.models.product import Product
from product.models.product_image import ProductImage


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.

    This viewset allows authenticated users to view, create, update, and delete products.
    It uses JWT authentication and custom permissions to ensure that only authorized users
    (admin or read-only for others) can perform these actions. The viewset also supports filtering,
    searching, and ordering of products based on specific fields.

    Attributes:
        queryset (QuerySet): A queryset that retrieves all Product objects.
        serializer_class (ProductSerializer): The serializer used to convert Product model instances
                                              into JSON and vice versa.
        authentication_classes (list): Specifies that JWT authentication is required.
        permission_classes (list): Specifies the permissions required to access or modify products,
                                   including `IsAdminOrReadOnly` for admin or read-only access.
        parser_classes (list): Specifies the parsers to handle file uploads and JSON parsing,
                               enabling `MultiPartParser`, `FormParser`, and `JSONParser`.
        filter_backends (list): A list of filter backends that enable filtering, searching, and ordering
                               on the products.
        filterset_fields (list): Defines the fields that can be used for filtering products.
        search_fields (list): Defines the fields that can be searched for products.
        ordering_fields (list): Defines the fields by which products can be ordered.
        ordering (list): Specifies the default ordering of products by price.

    Methods:
        list(request): List all products with optional filtering, searching, and ordering.
        create(request): Create a new product, allowing file uploads for associated images.
        retrieve(request, pk): Retrieve a single product by ID.
        update(request, pk): Update an existing product.
        partial_update(request, pk): Partially update a product.
        destroy(request, pk): Delete a product.
        perform_create(serializer): Handle product creation and image upload.
        get_queryset(): Override the default queryset to filter products based on the selected category.

    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser,
    ]  # Enable file uploads and enable JSON parsing

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name", "price", "stock_quantity", "categories__name"]
    search_fields = ["name", "stock_quantity", "categories__name"]
    ordering_fields = ["name", "price"]
    ordering = ["price"]

    def perform_create(self, serializer):
        """
        Override the default perform_create method to handle product creation
        and upload associated images.

        Args:
            serializer (ProductSerializer): The serializer containing validated product data.
        """
        # Save the product instance
        product = serializer.save()

        # Handle the associated images (if any)
        images = self.request.FILES.getlist(
            "images"
        )  # 'images' is the field name in the form
        for image in images:
            ProductImage.objects.create(product=product, image=image)

    def get_queryset(self):
        """
        Override the default queryset to filter products based on the selected category.

        The method checks if a category is specified in the query parameters and filters products
        to show only those belonging to the selected category or its subcategories.

        Returns:
            QuerySet: The queryset of products filtered by category (if provided).
        """
        queryset = super().get_queryset()

        # Get category filter from query parameters
        category_query = self.request.query_params.get("category", None)

        if category_query:
            # Get the selected category and its subcategories
            category = Category.objects.filter(name=category_query).first()
            if category:
                # Filter products in the selected category
                queryset = queryset.filter(categories=category)

        return queryset


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        product = self.get_object()  # Assuming product ID is passed in the URL
        serializer.save(product=product)
