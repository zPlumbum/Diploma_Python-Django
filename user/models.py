from django.db import models
from django.contrib.auth.models import AbstractUser
from product.models import Product


class User(AbstractUser):
    favorite = models.ManyToManyField(Product, related_name='user_favorite', blank=True)
