from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'Вы не являетесь создателем этого объявления или администратором. ' \
              'Удаление и редактирование объявления не разрешены.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj.creator_id == request.user
