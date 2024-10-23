from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product


def index(request):
    latest_eight = Product.objects.prefetch_related('category').all()[:8]

    return HttpResponse(
        render(request, 'pages/index.html', context={
            "latest_products": latest_eight,
            "related_products": latest_eight
        })
    )


def contact(request):
    return render(request, 'pages/contact.html', {})
