from rest_framework import permissions
from rest_framework.permissions import AllowAny, BasePermission


class RoleBasedPermission(BasePermission):
    """
    Base permission class to check user role
    """

    def __init__(self, role_code):
        self.role_code = role_code
        super().__init__()

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        if user.is_anonymous or user.role is None:
            return False
        return user.role.code == self.role_code


PERMISSION_MAP = {
    "list": [AllowAny],
    "retrieve": [AllowAny],
}


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "worker"
