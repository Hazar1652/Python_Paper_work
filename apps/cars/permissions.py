from rest_framework import permissions


class IsSellerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['seller', 'admin']


class IsOwnerOrManagerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Спочатку перевіряємо чи користувач залогінений
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            obj.owner == request.user or
            request.user.role in ['manager', 'admin']
        )