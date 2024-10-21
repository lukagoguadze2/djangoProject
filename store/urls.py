from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.index, name='category_html'),
    path('product/<slug:slug>-<int:product_id>/', views.product_details, name='product_details'),
]
