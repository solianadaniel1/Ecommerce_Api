from product.models.product import Product
from apis.serializers.product_serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'price', 'stock_quantity']
    search_fields = ['name', 'stock_quantity', 'category__name']
    ordering_fields = ['name', 'price']
    ordering = ['price']




