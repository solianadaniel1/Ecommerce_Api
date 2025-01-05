from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apis.permissions import IsOrderOwner
from apis.serializers.order_serializer import OrderSerializer
from order.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing order instances.

    This viewset allows authenticated users to view, create, update, and delete orders.
    It uses JWT authentication and custom permissions to ensure that only authenticated
    users can perform these actions. Additionally, users can only interact with their own orders
    due to the custom permission `IsOrderOwner`. The viewset also supports filtering, searching,
    and ordering of orders based on specific fields.

    Attributes:
        queryset (QuerySet): A queryset that retrieves all Order objects.
        serializer_class (OrderSerializer): The serializer used to convert Order model instances
                                            into JSON and vice versa.
        authentication_classes (list): Specifies that JWT authentication is required.
        permission_classes (list): Specifies the permissions required to access or modify orders,
                                   including `IsAuthenticated` for general authentication
                                   and `IsOrderOwner` for restricting users to their own orders.
        filter_backends (list): A list of filter backends that enable filtering, searching, and ordering
                               on the orders.
        filterset_fields (list): Defines the fields that can be used for filtering orders.
        search_fields (list): Defines the fields that can be searched for orders.
        ordering_fields (list): Defines the fields by which orders can be ordered.
        ordering (list): Specifies the default ordering of orders by the user's ID.

    Methods:
        list(request): List all orders for the logged-in user, with optional filtering, searching,
                      and ordering.
        create(request): Create a new order for the logged-in user.
        retrieve(request, pk): Retrieve a single order by ID for the logged-in user.
        update(request, pk): Update an existing order (user can only modify their own orders).
        partial_update(request, pk): Partially update an order (user can only modify their own orders).
        destroy(request, pk): Delete an order (user can only delete their own orders).
        get_queryset(): Returns only the orders for the logged-in user.
        perform_create(serializer): Automatically associates the logged-in user with the order when creating it.

    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOrderOwner]

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "user__email",
        "product__name",
        "order_status",
        "quantity",
        "shipping_address",
    ]
    search_fields = [
        "user__email",
        "product__name",
        "order_status",
        "quantity",
        "shipping_address",
    ]
    ordering_fields = ["user", "product", "order_status"]
    ordering = ["user"]

    def get_queryset(self):
        """
        Override the default queryset to filter orders by the logged-in user.

        Returns:
            QuerySet: The queryset of orders filtered by the currently authenticated user.
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Override the default perform_create method to automatically associate
        the logged-in user with the created order.

        Args:
            serializer (OrderSerializer): The serializer containing validated order data.
        """
        serializer.save(user=self.request.user)
