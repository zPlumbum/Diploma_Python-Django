from django_filters import rest_framework as filters
from product.models import Product


class ProductFilter(filters.FilterSet):
    id = filters.ModelMultipleChoiceFilter(
        queryset=Product.objects.all(),
        field_name='id',
        to_field_name='id'
    )
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']
