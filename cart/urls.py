from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
]
