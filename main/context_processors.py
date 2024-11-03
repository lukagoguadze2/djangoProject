from django.conf import settings
from django.urls import resolve, Resolver404
from django.core.cache import cache

from store.forms import SearchForm
from order.models import UserCart
from store.models import Category


def pages(request):
    path = request.path.strip('/').split('/')

    pages_ = []

    breadcrumb_url = ''

    for part in path:
        breadcrumb_url += '/' + part
        try:
            resolve(breadcrumb_url + "/")  # თუ არსებობს ეს URL მაშინ დავამატოთ
            pages_.append({
                'name': part.capitalize(),
                'href': breadcrumb_url
            })
        except Resolver404:
            pass

    return {
        'current_page': path[-1].capitalize(),
        'pages': pages_
    }


def website_name(request):
    return {
        'WEBSITE_NAME': settings.WEBSITE_NAME
    }


def global_variables(request):
    item_count = 0
    if request.user.is_authenticated:
        item_count = UserCart.objects.get(user=request.user).item_set.count()

    return {
        'search_form': SearchForm(),
        'item_count_in_cart': item_count,
    }


def all_categories(request):
    cache_key = 'all_categories'
    cache_timeout = 60 * 15  # 15 წუთი

    categories = cache.get(cache_key)

    if not categories:
        categories = Category.objects.all()
        cache.set(cache_key, categories, cache_timeout)

    return {
        'all_categories': Category.objects.all()
    }
