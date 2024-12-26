from rest_framework import serializers

from product.models.product_wishlist import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    """
    Serializer for the Wishlist model.

    This serializer is used to convert instances of the `Wishlist` model into JSON format
    and to validate incoming data for creating or updating a wishlist.

    It includes fields like 'user', 'created_at', and 'updated_at', with certain fields marked as read-only.

    Fields:
        - All fields of the Wishlist model.
        - 'user', 'created_at', 'updated_at' are read-only fields.

    Methods:
        - Meta: Specifies model and fields for serialization.
    """

    class Meta:
        model = Wishlist
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]
