from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission to allow only admin to access the object

    P.S. admin is a user with a profile role of "admin"
    """

    def has_permission(self, request, view):
        return request.user.profile.is_admin


class IsOwner(permissions.BasePermission):
    """
    Permission to allow only the owner to access the object
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.profile.user
