from rest_framework import permissions

class IsAuthorToViewReceipt(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Checks if the user is the author of the booking summary.
        return obj.user == request.user
    

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user.is_superuser