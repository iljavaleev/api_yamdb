from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'role'):
            return request.user.is_admin
        return False


class IsAuthorModeratorAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated

        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or (hasattr(request.user, 'role')
                    and (request.user.is_admin or request.user.is_moderator)))


class IsAuthenticatedPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (hasattr(request.user, 'role')
                 and request.user.is_admin)
        )
