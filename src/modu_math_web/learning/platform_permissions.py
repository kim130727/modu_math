from rest_framework.permissions import BasePermission


def is_manager(user):
    return bool(
        user
        and user.is_authenticated
        and user.is_active
        and (
            user.is_staff
            or user.is_superuser
            or user.groups.filter(name="modu_teachers").exists()
        )
    )


class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_manager(request.user)


def owned(queryset, user, field="owner"):
    return (
        queryset
        if user.is_staff or user.is_superuser
        else queryset.filter(**{field: user})
    )
