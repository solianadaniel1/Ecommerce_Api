from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication

from apis.permissions import IsAdminOrReadOnly
from apis.serializers.category_serializer import CategorySerializer
from product.models.category import Category


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.

    This viewset allows authenticated users to perform CRUD operations on Category
    objects. It uses JWT authentication and custom permissions to ensure that only
    admins can create, update, or delete categories, while read-only access is allowed
    for non-admin users. The viewset also supports filtering, searching, and ordering
    of categories based on specific fields.

    Attributes:
        queryset (QuerySet): A queryset that retrieves all Category objects.
        serializer_class (CategorySerializer): The serializer used to convert Category
                                              model instances into JSON and vice versa.
        authentication_classes (list): Specifies that JWT authentication is required.
        permission_classes (list): Specifies custom permissions that restrict
                                   category modification to admins only.
        filter_backends (list): A list of filter backends that enable filtering,
                               searching, and ordering on the categories.
        filterset_fields (list): Defines the fields that can be used for filtering.
        search_fields (list): Defines the fields that can be searched.
        ordering_fields (list): Defines the fields by which categories can be ordered.
        ordering (list): Specifies the default ordering of categories by their name.

    Methods:
        list(request): List all categories with optional filtering, searching, and
                      ordering.
        create(request): Create a new category (admin only).
        retrieve(request, pk): Retrieve a single category by ID.
        update(request, pk): Update an existing category (admin only).
        partial_update(request, pk): Partially update a category (admin only).
        destroy(request, pk): Delete a category (admin only).
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name", "parent_category__name"]
    search_fields = ["name", "parent_category__name"]
    ordering_fields = ["name", "parent_category__name"]
    ordering = ["name"]
