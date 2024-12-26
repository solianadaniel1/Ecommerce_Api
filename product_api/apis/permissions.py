from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to all users, but restrict unsafe actions
    (POST, PUT, DELETE) to admin users only.

    - GET, HEAD, and OPTIONS requests are allowed for all users, including unauthenticated users.
    - POST, PUT, DELETE requests are only allowed for authenticated users with admin privileges.

    Methods:
        has_permission(request, view):
            Determines if the user has permission to access the resource based on the HTTP method.
            - If the method is safe (GET, HEAD, OPTIONS), permission is granted to everyone.
            - If the method is unsafe (POST, PUT, DELETE), permission is granted only if the user is authenticated and an admin.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True  # Allow read-only access for everyone (including non-authenticated)

        print(
            f"User: {request.user}, Is Admin: {request.user.is_staff}, Is Authenticated: {request.user.is_authenticated}"
        )
        # Restrict unsafe methods to authenticated admin users
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsOrderOwner(BasePermission):
    """
    Custom permission to ensure that a user can only access or modify their own orders.

    - This permission ensures that only the user who created the order can access or modify it.

    Methods:
        has_object_permission(request, view, obj):
            Determines if the requesting user has permission to access or modify the order object.
            - The user is allowed if they are the owner of the order (i.e., the order's user matches the requesting user).
    """

    def has_object_permission(self, request, view, obj):
        # Check if the logged-in user is the owner of the order
        return obj.user == request.user
