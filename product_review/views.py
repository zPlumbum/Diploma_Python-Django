from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters

from product_review.models import ProductReview
from product_review.serializers import ProductReviewSerializer
from product_review.filters import ProductReviewFilter
from product_review.permissions import IsOwner


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductReviewFilter

    def get_permissions(self):

        if self.action == 'create':
            return [IsAuthenticated()]

        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]

        return []
