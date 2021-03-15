from django.contrib import admin
from product_collection.models import Collection, ProductInCollection


class ProductInCollectionInLine(admin.TabularInline):
    model = ProductInCollection


@admin.register(Collection)
class ProductCollectionAdmin(admin.ModelAdmin):
    inlines = [
        ProductInCollectionInLine
    ]
