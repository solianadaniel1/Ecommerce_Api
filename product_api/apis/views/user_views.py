from django.contrib.auth import get_user_model
from apis.serializers.user_serializer import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

user = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['email',]
    search_fields = ['email']
    ordering_fields = ['email']
    