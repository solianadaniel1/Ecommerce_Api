import logging

from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from apis.serializers.review_serializer import ReviewSerializer
from product.models.review import Review

# Setting up a logger for the viewset
logger = logging.getLogger(__name__)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing review instances.

    This viewset allows authenticated users to create reviews for products and enables
    all users to view reviews. The viewset uses JWT authentication and enforces
    permissions so that only authenticated users can create reviews, while all users
    can read them. Additionally, the viewset handles integrity errors and ensures that
    a user cannot submit multiple reviews for the same product.

    Attributes:
        queryset (QuerySet): A queryset that retrieves all Review objects.
        serializer_class (ReviewSerializer): The serializer used to convert Review model instances
                                              into JSON and vice versa.
        authentication_classes (list): Specifies that JWT authentication is required.
        permission_classes (list): Specifies the permissions required to access or modify reviews,
                                   including `IsAuthenticatedOrReadOnly` for authenticated users to post
                                   and all users to read.

    Methods:
        perform_create(serializer): Override the default perform_create method to handle review creation,
                                    ensure users can only review a product once, and handle integrity errors.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Authenticated users can post, all users can read

    def perform_create(self, serializer):
        """
        Override the default perform_create method to save the review with the logged-in user,
        ensure the user has not already reviewed the product, and handle any IntegrityErrors
        related to duplicate reviews.

        Args:
            serializer (ReviewSerializer): The serializer containing validated review data.

        Raises:
            ValidationError: If the user has already reviewed the product, a validation error is raised.
        """
        user = self.request.user
        product = serializer.validated_data[
            "product"
        ]  # Extract the product from the validated data

        try:
            # Save the review with the logged-in user
            serializer.save(user=user)

        except IntegrityError as e:
            # Check if it's a duplicate entry error
            if "product_review_user_id_product_id_c29147c2_uniq" in str(e):
                logger.warning(
                    f"Duplicate review attempted: User '{user.username}' tried to review product {product.id} again."
                )
                raise ValidationError(
                    f"You have already reviewed product {product.name}."
                )
            # Re-raise the error if it's not related to duplicate entry
            logger.error(f"Database error: {str(e)}")
            raise e
