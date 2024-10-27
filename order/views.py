from decimal import Decimal
from django.db.models import F, Sum
from django.views.generic import TemplateView, ListView

from .models import Item


class CartView(ListView):
    model = Item
    template_name = 'cart.html'
    context_object_name = 'cart_items'

    def get_context_data(self, **kwargs):
        tax_rate = Decimal(0.18)  # 18%

        context = super().get_context_data(**kwargs)

        if self.object_list:
            context['pricing'] = self.object_list.aggregate(
                total_without_tax=Sum('total_price'),
                taxed_money=Sum('total_price') * tax_rate
            )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            queryset = queryset.select_related('product').filter(
                cart__user=self.request.user
            )

            queryset = queryset.annotate(
                total_price=F('product__price') * F('quantity')
            )

            return queryset

        else:
            return []

    def post(self, request, *args, **kwargs):  # delete() ფუნქცია უნდა იყოს მაგრამ form-ით DELETE request ვერ ვაგზავნინებ
        if 'id' in request.POST:
            Item.objects.filter(id=request.POST['id']).delete()

        return self.get(request, *args, **kwargs)


class CheckoutView(TemplateView):
    template_name = 'checkout.html'
