from django.urls import path
from . import views
from .views import product_detail, get_csrf_token

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('category/<slug:category_slug>/', views.all_products, name='products_by_category'),
    path('<int:product_id>/', product_detail, name='product_detail'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
]
