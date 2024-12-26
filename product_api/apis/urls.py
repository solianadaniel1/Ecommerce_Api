from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from apis.views.category_view import CategoryViewSet
from apis.views.order_views import OrderViewSet
from apis.views.product_view import ProductViewSet
from apis.views.review_view import ReviewViewSet
from apis.views.user_views import LogoutView, RegisterViewSet, UserViewSet
from apis.views.wishlist_view import WishlistViewSet

"""
URL configuration for the API.

This file defines the URL patterns for the various viewsets and authentication-related views for the API.

- It includes routes for product, category, user, order, review, wishlist, and registration.
- It also defines the routes for token-based authentication (JWT), including token obtain, refresh, and verification.

The `DefaultRouter` from DRF is used to automatically generate URL patterns for viewsets. These include paths for common operations such as retrieving, creating, updating, and deleting resources.

Authentication routes:
- `/token/`: To obtain a JWT pair (access and refresh token) for authenticated users.
- `/token/refresh/`: To refresh the JWT access token using the refresh token.
- `/token/verify/`: To verify the validity of a JWT access token.
- `/logout/`: To log the user out by blacklisting the refresh token.

Viewset Routes:
- `/products/`: Product-related operations (CRUD operations on products).
- `/category/`: Category-related operations (CRUD operations on categories).
- `/users/`: User-related operations (CRUD operations on users, available only to admin).
- `/orders/`: Order-related operations (CRUD operations on orders).
- `/reviews/`: Review-related operations (CRUD operations on product reviews).
- `/wishlist/`: Wishlist-related operations (CRUD operations on user's wishlist items).
- `/register/`: Registration-related operations for user sign-up.

The static files route (`static()`) is added to serve media files (like images, videos) during development.

Attributes:
    router (DefaultRouter): Automatically generates URL patterns for registered viewsets.
    urlpatterns (list): List of URL patterns including viewsets and authentication routes.

Usage:
    Include this URL configuration in the root `urls.py` of the Django project.
"""

router = (
    DefaultRouter()
)  # (DRF) that automatically generates URL patterns for viewsets.

router.register(r"products", ProductViewSet, basename="product")
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"users", UserViewSet, basename="user")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"wishlist", WishlistViewSet, basename="wishlist")
router.register(r"register", RegisterViewSet, basename="register")


urlpatterns = [
    # apps route
    path("", include(router.urls)),
    # authentication route
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutView.as_view(), name="logout"),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # to serve media files
