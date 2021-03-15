from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from product_collection.models import Collection
from product_collection.serializers import CollectionSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]

        return []
