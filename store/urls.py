from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('category/', views.category_html, name='category_html'),
    path('category/<int:category_id>/products', views.category_products, name='category_products'),
    path('product/<int:product_id>/details', views.product_details, name='product_details')
]
