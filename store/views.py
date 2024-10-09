from django.http import JsonResponse
from .models import Category, Product
from djangoProject.settings import MEDIA_URL


def categories(request):
    all_categories = Category.objects.all()

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