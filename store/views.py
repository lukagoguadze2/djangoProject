from django.core.paginator import Paginator
from django.db.models import Max, F, Min, Avg, Sum, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def index(request, slug=''):  # index view-ს იძახებს ორი სხვადასხვა URL
    page_id = int(page_id) if (page_id := request.GET.get('page', '1')).isdigit() else 1

    if slug:
        category = Category.objects.filter(slug=slug).first()

        _products = Product.objects.prefetch_related('category').filter(
            category__in=category.get_descendants(include_self=True)
        ).distinct()
    else:
        category = None
        _products = Product.objects.prefetch_related('category')

    paginator = Paginator(_products, per_page=6)

    return render(
        request,
        template_name='index.html',
        context={
            "current_page_overload": category.name if category else None,
            "category": category,
            "categories": Category.objects.get_categories_with_product_count(),
            "page_obj": paginator.get_page(page_id),
        }
    )


def product_details(request, slug: str, product_id: int):
    product = get_object_or_404(Product.objects.prefetch_related('category'), id=product_id)

    return render(
        request,
        'product_details.html',
        {
            "current_page_overload": product.name,
            "product": product,
            "categories": Category.objects.get_categories_with_product_count(),
            "related_products": Product.objects.filter(category__in=product.category.all())
        }
    )

