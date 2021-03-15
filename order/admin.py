from django.contrib import admin
from order.models import Order, OrderProduct


class OrderProductInLine(admin.TabularInline):
    model = OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderProductInLine
    ]
