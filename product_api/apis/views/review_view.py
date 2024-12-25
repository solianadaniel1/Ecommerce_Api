import logging
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from product.models.review import Review
from apis.serializers.review_serializer import ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import IntegrityError

# Setting up a logger for the viewset
logger = logging.getLogger(__name__)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Authenticated users can post, all users can read

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']  # Extract the product from the validated data

        try:
            # Save the review with the logged-in user
            serializer.save(user=user)

        except IntegrityError as e:
            # Check if it's a duplicate entry error
            if 'product_review_user_id_product_id_c29147c2_uniq' in str(e):
                logger.warning(f"Duplicate review attempted: User '{user.username}' tried to review product {product.id} again.")
                raise ValidationError(f"You have already reviewed product {product.name}.")
            # Re-raise the error if it's not related to duplicate entry
            logger.error(f"Database error: {str(e)}")
            raise e
