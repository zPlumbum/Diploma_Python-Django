from rest_framework import serializers
from product.models import Product
from product_collection.models import ProductInCollection, Collection


class ProductInCollectionSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product.id")
    name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductInCollection
        fields = ('product_id', 'name')


class CollectionSerializer(serializers.ModelSerializer):
    products_in = ProductInCollectionSerializer(
        many=True,
        read_only=False
    )

    class Meta:
        model = Collection
        fields = ('id', 'title', 'text', 'products_in', 'created_at', 'updated_at',)

    def create(self, validated_data):
        products = validated_data.pop("products_in")
        collection = super().create(validated_data)
        for product in products:
            ProductInCollection.objects.create(
                product=product["product"]["id"],
                collection=collection,
            )
        return collection

    def update(self, instance, validated_data):
        products = validated_data.pop('products_in', [])
        instance = super().update(instance, validated_data)
        for product in products:
            ProductInCollection.objects.update_or_create(
                product=product["product"]["id"],
                collection=instance,
            )
        instance.save()
        return instance
