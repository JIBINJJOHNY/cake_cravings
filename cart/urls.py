# cart/urls.py
from django.urls import path
from .views import view_cart, add_to_cart, remove_from_cart,update_delivery_option

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_delivery_option/', update_delivery_option, name='update_delivery_option'),

]
