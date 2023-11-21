from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

# Assuming you have a Review model
class ReviewForm(forms.ModelForm):
    class Meta:
        
        fields = ['user', 'comment', 'rating']


