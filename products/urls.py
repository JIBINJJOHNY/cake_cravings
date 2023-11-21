from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('category/<slug:category_slug>/', views.all_products, name='products_by_category'),
    # Add more patterns as needed, for example:
    # path('filter-products-by-price/', views.filter_products_by_price, name='filter_products_by_price'),
]
