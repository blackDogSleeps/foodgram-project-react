from rest_framework import permissions


class IsAuthorAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return request.user.is_authenticated

        if request.method in ['PATCH', 'DELETE']:
            return (obj.author == request.user
                    or obj.user == request.user
                    or request.user.is_superuser
                    or request.user.role == 'admin')

        return request.method in permissions.SAFE_METHODS


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.role == 'admin' or request.user.is_superuser)
                    )
                )
