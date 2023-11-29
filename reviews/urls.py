from django.urls import path
from .views import add_review, edit_review, view_reviews, delete_review

app_name = 'reviews'

urlpatterns = [
    path('add/<int:product_id>/', add_review, name='add_review'),
    path('edit/<int:review_id>/', edit_review, name='edit_review'),
    path('view/<int:product_id>/', view_reviews, name='view_reviews'),
    path('delete/<int:product_id>/<int:review_id>/', delete_review, name='delete_review'),
]
