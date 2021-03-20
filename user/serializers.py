from rest_framework import serializers
from user.models import User, UserProduct


class UserProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProduct
        fields = ('id', 'product')


class UserSerializer(serializers.ModelSerializer):
    favorite_products = UserProductSerializer(
        many=True,
        required=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'favorite_products',)

    def create(self, validated_data):
        favorite_products_data = validated_data.pop('favorite_products')
        user = super().create(validated_data)

        if len(favorite_products_data) > 0:
            raw_favorite_products = []
            for favorite_product_data in favorite_products_data:
                favorite_product = UserProduct(
                    user=user,
                    product=favorite_product_data['product']
                )
                raw_favorite_products.append(favorite_product)

            UserProduct.objects.bulk_create(raw_favorite_products)

        return user

    def update(self, instance, validated_data):
        favorite_products = validated_data.pop('favorite_products', [])
        instance = super().update(instance, validated_data)
        UserProduct.objects.filter(user=instance).delete()
        for favorite_product in favorite_products:
            UserProduct.objects.update_or_create(
                user=instance,
                product=favorite_product['product']
            )
        instance.save()
        return instance
