from rest_framework import serializers
from product.models.product_wishlist import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields ='__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
