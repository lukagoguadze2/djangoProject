from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from store.models import Product


class IndexView(ListView):
    model = Product
    queryset = Product.objects.prefetch_related('category').all()[:8]
    template_name = 'pages/index.html'
    context_object_name = 'products'


@method_decorator(login_required(login_url='user:login'), name='dispatch')
class ContactView(TemplateView):
    template_name = 'pages/contact.html'

