from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import User
from product.models import Product


class ProductReview(models.Model):

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    creator_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_reviews',
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(verbose_name='Текст')
    evaluation = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    created_at = models.DateTimeField(
        verbose_name='Создана',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлена',
        auto_now=True
    )

    def __str__(self):
        return f'{self.creator_id} - {self.product_id}'
