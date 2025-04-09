from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    message = 'You are not admin'

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.role==request.user.RoleChoices.owner))


class OwnerPermission(BasePermission):
    message = 'You are not owner'

    def has_permission(self, request, view):
        return bool(request.user and request.user.role==request.user.RoleChoices.owner)
