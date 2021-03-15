from django_filters import rest_framework as filters
from product_review.models import ProductReview


class ProductReviewFilter(filters.FilterSet):
    id = filters.ModelMultipleChoiceFilter(
        queryset=ProductReview.objects.all(),
        field_name='id',
        to_field_name='id'
    )
    creator_id = filters.ModelMultipleChoiceFilter(
        queryset=ProductReview.objects.all(),
        field_name='creator_id',
        to_field_name='creator_id_id'
    )
    product_id = filters.ModelMultipleChoiceFilter(
        queryset=ProductReview.objects.all(),
        field_name='product_id',
        to_field_name='product_id_id'
    )
    evaluation = filters.RangeFilter()
    created_at = filters.DateFromToRangeFilter()
