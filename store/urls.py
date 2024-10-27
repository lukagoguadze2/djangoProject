from django.urls import path
from .views import IndexView, ProductView


app_name = 'store'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', IndexView.as_view(), name='category_html'),
    path('product/<slug:slug>-<int:product_id>/', ProductView.as_view(), name='product_details'),
]
