from django.contrib import admin
from user.models import User, UserProduct


class UserProductInLine(admin.TabularInline):
    model = UserProduct


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserProductInLine
    ]
