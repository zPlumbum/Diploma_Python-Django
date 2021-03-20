from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'Вы не являетесь данным пользователем. Редактирование информации о нем запрещено.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj.id == request.user.id
