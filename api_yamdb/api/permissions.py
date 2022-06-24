from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
<<<<<<< HEAD
        return (
            request.method in permissions.SAFE_METHODS 
            or obj.token == request.user
        )
=======
        return (request.method in permissions.SAFE_METHODS or obj.author
                == request.user)
>>>>>>> 2fed6b6fe04a3b85b931a027229d752c6fb9a6e4


class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
<<<<<<< HEAD
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
        )

class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
=======
        return request.user.role == User.MODERATOR


class IsAdminPermission(permissions.BasePermission):

    # def has_permission(self, request, view):
    #     return (
    #         # request.method in permissions.SAFE_METHODS
    #         # or request.user.is_authenticated
    #         request.user.is_authenticated
    #     )

    def has_object_permission(self, request, view, obj):
        return (
                request.user.role == User.ADMIN
                or request.user.is_superuser == True
>>>>>>> 2fed6b6fe04a3b85b931a027229d752c6fb9a6e4
        )

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

