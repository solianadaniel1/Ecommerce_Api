from order.models import Order
from apis.serializers.order_serializer import OrderSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apis.permissions import IsOrderOwner


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'product', 'product','order_status','quantity','shipping_address']
    search_fields = ['user', 'product', 'product','order_status','quantity','shipping_address']
    ordering_fields = ['user', 'product','order_status'] 
    ordering = ['user']

    
    def get_queryset(self):
        # Return only the orders for the logged-in user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the logged-in user as the owner of the order
        serializer.save(user=self.request.user)

