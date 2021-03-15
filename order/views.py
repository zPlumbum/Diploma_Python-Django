from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters

from order.models import Order
from order.serializers import OrderSerializer
from order.permissions import IsOwner
from order.filters import OrderFilter


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):

        if self.request.user.is_staff:
            queryset = Order.objects.all()
        else:
            user_id = self.request.user.id
            queryset = Order.objects.all().filter(creator_id=user_id)

        return queryset

    def get_permissions(self):

        if self.action in ['create', 'list', 'retrieve']:
            return [IsAuthenticated()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]

        return []
