from django.views.generic import TemplateView, ListView
from order.forms import AddItemForm
from store.models import Product


class IndexView(ListView):
    model = Product
    queryset = Product.objects.all()[:8]
    template_name = 'pages/index.html'
    context_object_name = 'products'


class ContactView(TemplateView):
    template_name = 'pages/contact.html'

