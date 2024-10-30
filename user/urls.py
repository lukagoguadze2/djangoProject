from django.urls import path
from .views import AuthView, AuthLogout, AuthRegisterView

app_name = 'user'

urlpatterns = [
    path('login/', AuthView.as_view(), name='login'),
    path('logout/', AuthLogout.as_view(), name='logout'),
    path('register/', AuthRegisterView.as_view(), name='register'),
]
