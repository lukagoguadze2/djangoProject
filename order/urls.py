from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]
