from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('item/<int:_id>', views.item, name='item'),
    path('item/<int:_id>/<str:component>', views.display_component, name='component')
]
