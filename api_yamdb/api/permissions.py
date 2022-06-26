from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS 
            or  obj.author == request.user
        )


class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(request.user, 'role'):
            return request.user.is_moderator
        return False


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'role'):
            return request.user.is_admin
        return False

class IsAuthenticatedPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

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
            or (request.user.is_authenticated and request.user.is_admin)
        )

    def has_object_permission(self, request, view, obj):
        return (
             request.user.is_admin
        )