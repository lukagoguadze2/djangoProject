from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product


@admin.register(Product)
class ProductView(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ('name', 'display_categories')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('category')

    @admin.display(description='კატეგორიები')
    def display_categories(self, obj):
        return ", ".join(category.name for category in obj.category.all())


@admin.register(Category)
class CategoryView(MPTTModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

    list_display = ('name', 'parent')

    list_select_related = ('parent',)
