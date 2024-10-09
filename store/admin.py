from django.contrib import admin
from .models import Category, Product


class SlugifyName(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class CategoryView(admin.ModelAdmin):
    list_display = ('name', 'parent')


admin.site.register(Category, CategoryView)
admin.site.register(Product, SlugifyName)
