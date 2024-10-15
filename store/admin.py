from django.contrib import admin
from .models import Category, Product


class SlugifyName(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ('name', 'display_categories')

    def display_categories(self, obj):
        return ", ".join(category.name for category in obj.category.all())

    display_categories.short_description = 'კატეგორიები'


class CategoryView(admin.ModelAdmin):
    list_display = ('name', 'parent')


admin.site.register(Category, CategoryView)
admin.site.register(Product, SlugifyName)
