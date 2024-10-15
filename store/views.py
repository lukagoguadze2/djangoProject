from django.core.paginator import Paginator
from django.db.models import Max, F, Min, Avg, Sum
from django.http import JsonResponse
from django.shortcuts import render

from .models import Category, Product


def categories(request):
    all_categories = Category.objects.select_related('parent').all()

    categories_list = []
    for category in all_categories:
        categories_list.append(
            category.values(
                include_parent=True
            )
        )

    return JsonResponse(categories_list, safe=False, status=200)


def products(request):
    all_products = Product.objects.all()

    products_list = []
    for product in all_products:
        products_list.append(
            product.values()
        )

    return JsonResponse(products_list, safe=False, status=200)


def category_html(request):
    all_categories = Category.objects.with_product_count()

    return render(request, 'category.html', {"categories": all_categories})


def category_products(request, category_id):
    page_id = int(page_id) if (page_id := request.GET.get('page', '1')).isdigit() else 1

    category = Category.objects.get(id=category_id)
    
    _products = Product.objects.get_products_by_category(
        category
    ).annotate(
        total_price=F('quantity') * F('price')
    )

    statistics = _products.aggregate(
        most_expensive_price=Max('price'),
        least_expensive_price=Min('price'),
        average_product_price=Avg('price'),
        total_price_of_product=Sum('total_price')
    )

    paginator = Paginator(_products, per_page=2)

    return render(
        request,
        template_name='products.html',
        context={
            "category": category,
            "statistics": statistics,
            "paginator": paginator.get_page(page_id)
        }
    )


def product_details(request, product_id: int):
    product = Product.objects.prefetch_related('category').get(id=product_id)
    print(product.values())
    return render(request, 'product_details.html', {"product": product})
