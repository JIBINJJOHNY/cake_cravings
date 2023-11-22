# cart/urls.py
from django.urls import path
from .views import view_cart, add_to_cart, update_cart, remove_from_cart

app_name = 'cart'

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('add/<item_id>/', add_to_cart, name='add_to_cart'),
    path('update/<item_id>/', update_cart, name='update_cart'),
    path('remove/<item_id>/', remove_from_cart, name='remove_from_cart'),
]
