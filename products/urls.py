from django.urls import path
from . import views


app_name = 'products'
urlpatterns = [
    path('', views.all_products, name='products'),
    path('category/', views.all_products, name='products_by_category'),
    path('category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
  
]