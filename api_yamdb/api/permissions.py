from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()

class SignupUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or obj.token
                == request.user)


class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == User.MODERATOR
        )

class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            # request.method in permissions.SAFE_METHODS
            # or request.user.is_authenticated
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            # or request.user.is_superuser
            # request.user['role'] == 'admin'
        )

class IsAuthenticatedPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            # request.method in permissions.SAFE_METHODS
            # or request.user.is_authenticated
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            # request.method in permissions.SAFE_METHODS
            request.user.is_authenticated
            or request.user.is_admin
            # or request.user.is_superuser
        )

#
# class IsSuperUserPermission(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         return (
#                 request.method in permissions.SAFE_METHODS
#                 or request.user.is_superuser
#         )

