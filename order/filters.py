from django_filters import rest_framework as filters
from order.models import Order, OrderStatusChoices
from product.models import Product


class OrderFilter(filters.FilterSet):
    id = filters.ModelMultipleChoiceFilter(
        queryset=Order.objects.all(),
        field_name='id',
        to_field_name='id'
    )
    status = filters.ChoiceFilter(choices=OrderStatusChoices.choices)
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()
    positions = filters.ModelMultipleChoiceFilter(
        field_name="positions",
        to_field_name="id",
        queryset=Product.objects.all(),
    )
    total_price = filters.RangeFilter()

    class Meta:
        model = Order
        fields = ('id', 'status', 'created_at', 'updated_at', 'positions', 'total_price')
