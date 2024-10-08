from django.contrib import admin
from .models import Category, Product


class SlugifyName(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Category)
admin.site.register(Product, SlugifyName)
