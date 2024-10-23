from django.contrib import admin
from .models import UserCart, Item


@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


@admin.register(Item)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

    list_editable = ('quantity',)
