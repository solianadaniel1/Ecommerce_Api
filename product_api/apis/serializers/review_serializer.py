from rest_framework import serializers
from product.models import Product
from product.models.review import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display the username
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) #user submit product ID when reviewing

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']  # User and creation date are read-only
