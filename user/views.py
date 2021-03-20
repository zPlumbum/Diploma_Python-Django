from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from user.models import User
from user.serializers import UserSerializer
from user.permissions import IsOwner


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):

        if self.request.user.is_staff:
            queryset = User.objects.all()
        else:
            user_id = self.request.user.id
            queryset = User.objects.all().filter(id=user_id)

        return queryset

    def get_permissions(self):

        if self.action in ['create', 'destroy']:
            return [IsAdminUser()]

        if self.action in ['update', 'partial_update']:
            return [IsOwner()]

        return []
