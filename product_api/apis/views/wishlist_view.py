from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from product.models.product_wishlist import Wishlist
from apis.serializers.wishlist_serializer import WishlistSerializer
from rest_framework.exceptions import ValidationError
from product.models.product import Product

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter the wishlist for the current logged-in user."""
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically associate the logged-in user with the wishlist item."""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Allow the user to add a product to their wishlist."""
        product_id = request.data.get('product')
        if not product_id:
            raise ValidationError("Product ID is required.")

        # Check if the product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Product not found.")

        # Check if the product is already in the user's wishlist
        if Wishlist.objects.filter(user=request.user, product=product).exists():
            raise ValidationError("This product is already in your wishlist.")

        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Allow the user to remove a product from their wishlist."""
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"detail": "You do not have permission to delete this item."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


