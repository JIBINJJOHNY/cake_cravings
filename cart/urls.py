from django.urls import path
from .views import CartView, AddToCart, RemoveFromCart

urlpatterns = [
    path('', CartView.as_view(), name='view_cart'),
    path('add-to-cart/', AddToCart.as_view(), name='add_to_cart'),
    path('remove-from-cart/', RemoveFromCart.as_view(), name='remove_from_cart'),
]
