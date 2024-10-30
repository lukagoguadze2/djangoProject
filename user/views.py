from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.contrib.auth import login
from django.utils import timezone

from .forms import AuthForm, RegistrationForm
from .models import User


class AuthView(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthForm
    next_page = 'store:index'
    redirect_authenticated_user = True

    def form_valid(self, form):
        x = super().form_valid(form)  # ჯერ შევიყვანოთ იუზერი ექაუნთში
        self.request.user.last_activity = timezone.now()  # შემდეგ შევუცვალოთ ბოლო აქტივობა
        self.request.user.save()  # ამით middleware არ დაალოგაუთებს პირველივე რექუესტზე
        return x


class AuthLogout(LogoutView):
    template_name = 'registration/logout.html'
    next_page = 'user:login'
    http_method_names = LogoutView.http_method_names + ['get']

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# თუ მომხმარებელი ხელით გადავა რეგისტრაციზე როდესაც ექაუნთშია შესული მაშინ დეკორატორი გადაამისამართეს LOGOUT-ის გვერდზე
@method_decorator(user_passes_test(lambda u: u.is_anonymous, login_url='user:logout'), name='dispatch')
class AuthRegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        x = super().form_valid(form)
        self.object.is_staff = True
        self.object.save()
        login(self.request, self.object)  # შევიყვანოთ მომხმარებელი ექაუნთში რეგისტრაციის შემდეგ
        return x
