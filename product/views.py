from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django_filters import rest_framework as filters

from product.models import Product
from product.serializers import ProductSerializer
from product.filters import ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]

        return []
