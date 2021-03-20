"""django_diploma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import ProductViewSet
from product_review.views import ProductReviewViewSet
from order.views import OrderViewSet
from product_collection.views import CollectionViewSet
from user.views import UserViewSet


router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('product-reviews', ProductReviewViewSet, basename='product-review')
router.register('orders', OrderViewSet, basename='order')
router.register('product-collections', CollectionViewSet, basename='product-collection')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
