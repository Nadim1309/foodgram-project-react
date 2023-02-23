from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_staff)


class IsFollowerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.user == request.user)
