from product.models.product import Product
from product.models.product_image import ProductImage
from apis.serializers.product_serializers import ProductSerializer
from rest_framework import viewsets
from apis.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from product.models import Category
from rest_framework.parsers import MultiPartParser, FormParser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]  # Enable file uploads

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'price', 'stock_quantity', 'categories__name']
    search_fields = ['name', 'stock_quantity', 'categories__name']
    ordering_fields = ['name', 'price']
    ordering = ['price']


    def perform_create(self, serializer):
            # Save the product instance
            product = serializer.save()
            # Handle the associated images (if any)
            images = self.request.FILES.getlist('images')  # 'images' is the field name in the form
            for image in images:
                ProductImage.objects.create(product=product, image=image)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get category filter from query parameters
        category_query = self.request.query_params.get('category', None)

        if category_query:
            # Get the selected category and its subcategories
            category = Category.objects.filter(name=category_query).first()
            if category:
                # Filter products in the selected category
                queryset = queryset.filter(categories=category)

        return queryset
