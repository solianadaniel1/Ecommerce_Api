from product.models.category import Category
from apis.serializers.category_serializer import CategorySerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apis.permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'parent_category__name']
    search_fields = ['name', 'parent_category__name']
    ordering_fields = ['name', 'parent_category__name']
    ordering = ['name']


 

