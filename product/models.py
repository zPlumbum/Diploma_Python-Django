from django.db import models


class Product(models.Model):

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(
        verbose_name='Создана',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлена',
        auto_now=True
    )

    def __str__(self):
        return f'{self.id}: {self.name}'
