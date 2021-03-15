from rest_framework import serializers
from user.serializers import UserSerializer
from product_review.models import ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):

    creator_id = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = ProductReview
        fields = ('id', 'creator_id', 'product_id', 'text',
                  'evaluation', 'created_at', 'updated_at',)

    def create(self, validated_data):
        validated_data["creator_id"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        creator_id = self.context['request'].user.id
        product_id = data['product_id']
        user_reviews = ProductReview.objects.all().filter(creator_id=creator_id).filter(product_id=product_id)

        if len(user_reviews) > 0:
            raise serializers.ValidationError({'creator_id': 'Этот пользователь уже оставил отзыв'})

        return data
