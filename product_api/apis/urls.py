from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from apis.views.user_views import UserViewSet
from apis.views.category_view import CategoryViewSet
from apis.views.product_view import ProductViewSet
from apis.views.order_views import OrderViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
router = DefaultRouter() #(DRF) that automatically generates URL patterns for viewsets.

router.register(r'products', ProductViewSet, basename='product')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'users', UserViewSet , basename='user')
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    #apps route
    path('', include(router.urls)),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #to serve media files


