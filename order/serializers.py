from rest_framework import serializers
from order.models import Order, OrderProduct
from product.models import Product
from user.serializers import UserSerializer


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ('id', 'product', 'quantity',)


class OrderSerializer(serializers.ModelSerializer):
    creator_id = UserSerializer(
        read_only=True
    )

    order_positions = OrderProductSerializer(
        many=True,
        required=True
    )

    class Meta:
        model = Order
        fields = ('id', 'creator_id', 'order_positions', 'total_price',
                  'status', 'created_at', 'updated_at',)
        read_only_fields = ('status',)

    def validate_order_positions(self, order_positions):
        product_ids = [order_position['product'].id for order_position in order_positions]
        product_ids_set = set(product_ids)

        if len(product_ids_set) != len(product_ids):
            raise serializers.ValidationError('В заказе содержатся дубли товаров')

        return order_positions

    def create(self, validated_data):
        validated_data['creator_id'] = self.context['request'].user
        order_positions_data = validated_data.pop('order_positions')

        total_price = 0
        for order_position_data in order_positions_data:
            product = Product.objects.filter(id=order_position_data['product'].id).first()
            total_price += product.price * order_position_data['quantity']
        validated_data['total_price'] = total_price

        order = super().create(validated_data)

        raw_order_positions = []
        for order_position_data in order_positions_data:
            order_position = OrderProduct(
                order=order,
                product=order_position_data['product'],
                quantity=order_position_data['quantity']
            )
            raw_order_positions.append(order_position)

        OrderProduct.objects.bulk_create(raw_order_positions)

        return order

    def update(self, instance, validated_data):
        if instance.status != validated_data['status']:
            if not self.context['request'].user.is_staff:
                raise serializers.ValidationError('Только администраторы могут менять статус заказа')

        return super().update(self.instance, validated_data)
