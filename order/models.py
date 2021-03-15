from django.db import models
from product.models import Product
from user.models import User


class OrderStatusChoices(models.TextChoices):

    NEW = "NEW", "Новый"
    IN_PROGRESS = "IN_PROGRESS", "В процессе"
    DONE = "DONE", "Выполненный"


class Order(models.Model):

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    creator_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    positions = models.ManyToManyField(
        Product,
        through='OrderProduct',
        blank=False,
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.TextField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW
    )
    created_at = models.DateTimeField(
        verbose_name='Создана',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлена',
        auto_now=True
    )


class OrderProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_positions'
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.order} - {self.product}: {self.quantity}'
