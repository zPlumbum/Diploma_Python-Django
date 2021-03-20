from django.db import models
from django.contrib.auth.models import AbstractUser
from product.models import Product


class User(AbstractUser):
    favorite = models.ManyToManyField(
        Product,
        through='UserProduct',
        related_name='user_favorite',
        blank=True
    )


class UserProduct(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorite_products',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Избранное'
    )
