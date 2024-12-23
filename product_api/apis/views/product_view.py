from product.models.product import Product
from apis.serializers.product_serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from product.models import Category

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'price', 'stock_quantity']
    search_fields = ['name', 'stock_quantity', 'categories__name']
    ordering_fields = ['name', 'price']
    ordering = ['price']


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
