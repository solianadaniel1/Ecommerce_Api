from rest_framework import serializers

from product.models import Product
from product.models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    This serializer is used to convert Review model instances to and from JSON format.
    It includes the user who made the review, the product being reviewed, and other review-related data.
    It also handles the read-only fields for the user and timestamps (created_at, updated_at).

    Fields:
        - 'id': The unique identifier of the review.
        - 'user': The username of the user who made the review (read-only).
        - 'product': The product being reviewed, identified by its primary key.
        - 'rating': The rating given by the user for the product.
        - 'comment': The review text written by the user.
        - 'created_at': The timestamp of when the review was created (read-only).
        - 'updated_at': The timestamp of when the review was last updated (read-only).
    """

    user = serializers.StringRelatedField(read_only=True)  # Display the username
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )  # User submits product ID when reviewing

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "product",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]  # User and creation date are read-only
