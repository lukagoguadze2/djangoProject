from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, FormView
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

from main.forms import EmailForm
from store.models import Product


class IndexView(ListView):
    model = Product
    queryset = Product.objects.prefetch_related('category').all()[:8]
    template_name = 'pages/index.html'
    context_object_name = 'products'


@method_decorator(login_required(login_url='user:login'), name='dispatch')
class ContactView(FormView):
    form_class = EmailForm
    template_name = 'pages/contact.html'
    success_url = '/contact'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        subject = f'New Contact Form Submission from {name}'
        full_message = f"Message from {name} ({email}):\n\n{message}"

        # გავუგზავნოთ email-ი ადმინს
        send_mail(
            subject,
            full_message,
            from_email=None,  # რადგან კონსოლის ბექენდს ვიყენებთ არ სჭირდება ეს არგუმენტი
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        return super().form_valid(form)


class _404(TemplateView):
    template_name = '404.html'


class _500(TemplateView):
    template_name = '500.html'
