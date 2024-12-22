from order.models import Order
from apis.serializers.order_serializer import OrderSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'product', 'product','order_status','quantity','shipping_address']
    search_fields = ['user', 'product', 'product','order_status','quantity','shipping_address']
    ordering_fields = ['user', 'product','order_status'] 
    ordering = ['user']




