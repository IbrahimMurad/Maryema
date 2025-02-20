from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission to allow only admin to access the object

    P.S. admin is a user with a profile role of "admin"
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.profile.is_admin


class IsOwner(permissions.BasePermission):
    """
    Permission to allow only the owner to access the object
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.profile.user


class IsCustomer(permissions.BasePermission):
    """
    Permission to allow only customer to access the object

    P.S. customer is a user with a profile role of "customer"
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.profile.is_customer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows access to all users to read-only actions.

    Only admin users can perform write actions.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.profile.is_admin
