from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to perform unsafe actions
    (POST, PUT, DELETE). Other users can only read.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True  # Allow read-only access for everyone (including non-authenticated)
        print(f"User: {request.user}, Is Admin: {request.user.is_staff}, Is Authenticated: {request.user.is_authenticated}")
        # Restrict unsafe methods to authenticated admin users
        return request.user and request.user.is_authenticated and request.user.is_staff
    

class IsOrderOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the logged-in user is the owner of the order
        return obj.user == request.user