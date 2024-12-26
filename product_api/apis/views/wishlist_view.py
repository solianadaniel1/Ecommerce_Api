from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apis.serializers.wishlist_serializer import WishlistSerializer
from product.models.product import Product
from product.models.product_wishlist import Wishlist


class WishlistViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing the wishlist of products for authenticated users.

    This viewset allows authenticated users to view, add, and remove products from their wishlist.
    Each user can only manage their own wishlist. The viewset supports creation and deletion of wishlist items.

    Attributes:
        queryset (QuerySet): A queryset that retrieves all wishlist items.
        serializer_class (WishlistSerializer): The serializer used to convert wishlist data into JSON format and vice versa.
        authentication_classes (list): Specifies that JWT authentication is required for this viewset.
        permission_classes (list): Specifies that only authenticated users can access this viewset.

    Methods:
        get_queryset(): Filters the wishlist to only show items for the currently authenticated user.
        perform_create(serializer): Automatically associates the logged-in user with the wishlist item when creating a new wishlist item.
        create(request, *args, **kwargs): Adds a product to the logged-in user's wishlist, ensuring the product exists and is not already in the wishlist.
        destroy(request, *args, **kwargs): Removes a product from the user's wishlist, with permission checks to ensure the user owns the item.
    """

    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter the wishlist for the current logged-in user.

        Returns:
            QuerySet: A queryset of the user's wishlist items.
        """
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically associate the logged-in user with the wishlist item.

        Args:
            serializer (Serializer): The serializer used to save the wishlist item.
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Allow the user to add a product to their wishlist.

        Validates that the product exists, that a product ID is provided, and that the product
        is not already in the user's wishlist. If these checks pass, the product is added to the wishlist.

        Args:
            request (Request): The HTTP request containing the product to be added to the wishlist.

        Returns:
            Response: A response indicating the success or failure of adding the product to the wishlist.
        """
        product_id = request.data.get("product")
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
        """
        Allow the user to remove a product from their wishlist.

        Ensures that only the user who added the item to the wishlist can delete it.

        Args:
            request (Request): The HTTP request containing the wishlist item to be deleted.

        Returns:
            Response: A response indicating whether the deletion was successful or if the user is not authorized.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this item."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)
