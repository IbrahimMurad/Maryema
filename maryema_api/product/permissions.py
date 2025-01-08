from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows access to all users to read-only actions.

    Only admin users can perform write actions.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.profile.is_admin
