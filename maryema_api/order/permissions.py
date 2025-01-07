from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permission to allow only admin or owner to access the object
    and only the admin can modify the object
    """

    def has_permission(self, request, view):
        # Check permissions at the request level for list actions
        if view.action == "list":
            return request.user.profile.is_admin or request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        # Check permissions at the object level for other actions
        if request.method in permissions.SAFE_METHODS:
            return request.user.profile.is_admin or request.user == obj.profile.user
        return request.user.profile.is_admin


class IsOwner(permissions.BasePermission):
    """
    Permission to allow only the owner to access the object
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.profile.user


class IsAdmin(permissions.BasePermission):
    """
    Permission to allow only admin to access the object
    """

    def has_permission(self, request, view):
        return request.user.profile.is_admin
