from decimal import Decimal
from django.db.models import F, Sum
from django.shortcuts import render
from .models import Item


def cart(request):
    if 'id' in request.POST:
        Item.objects.filter(id=request.POST['id']).delete()

    context = {}
    if request.user.is_authenticated:
        tax_rate = Decimal(0.18)  # 18%
        user_cart = Item.objects.select_related('product').filter(
            cart__user=request.user
        )

        cart_items = user_cart.annotate(
            total_price=F('product__price') * F('quantity')
        )
        context['cart_items'] = cart_items
        context['pricing'] = cart_items.aggregate(
            total_without_tax=Sum('total_price'),
            taxed_money=Sum('total_price') * tax_rate
        )

    return render(request, 'cart.html', context)


def checkout(request):
    return render(request, 'checkout.html', {})


# def delete_item(request):
#     if request.method == 'POST':
#         Item.objects.filter(id=request.POST['id']).delete()
#
#         return JsonResponse({'status': 'ok'})
#
#     return JsonResponse({'status': 'error'})
