from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from apis.serializers.user_serializer import RegisterSerializer, UserSerializer
from users.models import CustomUser

user = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.

    This viewset allows admins to view and edit user details. The viewset uses JWT authentication
    and requires admin permissions to access it. It also provides filtering, searching, and ordering
    capabilities for user data.

    Attributes:
        queryset (QuerySet): A queryset that retrieves all user instances.
        serializer_class (UserSerializer): The serializer used to convert user model instances
                                           into JSON format and vice versa.
        authentication_classes (list): Specifies that JWT authentication is required for this viewset.
        permission_classes (list): Specifies that only admin users have permission to access this viewset.
        filter_backends (list): Specifies the filtering, searching, and ordering backends.
        filterset_fields (list): Allows filtering by email.
        search_fields (list): Enables searching by email.
        ordering_fields (list): Allows ordering by email.
    """

    queryset = user.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [
        JWTAuthentication
    ]  # authenticating requests to this view using JWT.
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = [
        "email",
    ]
    search_fields = ["email"]
    ordering_fields = ["email"]


class RegisterViewSet(viewsets.ModelViewSet):
    """
    A viewset for user registration.

    This viewset allows anyone to register a new user. The viewset provides an endpoint for creating
    user accounts and uses the `RegisterSerializer` to handle registration data.

    Attributes:
        queryset (QuerySet): A queryset that retrieves all user instances.
        serializer_class (RegisterSerializer): The serializer used to handle user registration data.
        permission_classes (list): Specifies that anyone (no authentication required) can access this viewset.
    """

    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Allow anyone to register


class LogoutView(APIView):
    """
    A view for logging out the user.

    This view handles the logout process by invalidating the provided refresh token. After the token
    is invalidated, the user is effectively logged out and cannot use the refresh token to obtain new
    access tokens.

    Attributes:
        permission_classes (list): Specifies that only authenticated users can access this view.

    Methods:
        post(request): Handles the POST request to log the user out by blacklisting the refresh token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logs out the user by invalidating the provided refresh token.

        Args:
            request (Request): The HTTP request containing the refresh token to be invalidated.

        Returns:
            Response: A response indicating the success or failure of the logout attempt.
        """
        try:
            # Get the refresh token from request data
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Blacklist the token to invalidate it
            token = RefreshToken(refresh_token)
            token.blacklist()  # This invalidates the refresh token

            return Response(
                {"message": "Logged out successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
