from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apis.views.user_views import UserViewSet
from apis.views.category_view import CategoryViewSet
from apis.views.product_view import ProductViewSet
from apis.views.order_views import OrderViewSet

router = DefaultRouter() #(DRF) that automatically generates URL patterns for viewsets.

router.register(r'products', ProductViewSet, basename='product')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'users', UserViewSet , basename='user')
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
]
