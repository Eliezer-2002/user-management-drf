from rest_framework.permissions import BasePermission


class IsMainUser(BasePermission):
    message = "A user manager account is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_manager or request.user.is_superuser)
        )
