from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешает доступ только администратором и суперюзерам."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает доступ на чтение."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает безопасные запросы всем.

    Изменение и удаление - только автору, модератору или админу.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
