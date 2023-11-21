from django.shortcuts import render, redirect,render, get_object_or_404
from django.db.models import Q
from .models import Product, Category
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction

def all_products(request):
    products = Product.objects.filter(is_active=True)
    query = request.GET.get('q')
    category_filter = request.GET.get('category')
    sorting = request.GET.get('sort')
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    if category_filter:
        products = products.filter(category__slug=category_filter)
       

    if sorting:
        if sorting == 'price_asc':
            products = products.order_by('original_price')
        elif sorting == 'price_desc':
            products = products.order_by('-original_price')
        elif sorting == 'name_asc':
            products = products.order_by('name')
        elif sorting == 'name_desc':
            products = products.order_by('-name')
        elif sorting == 'rating_asc':
            products = products.order_by('rating')
        elif sorting == 'rating_desc':
            products = products.order_by('-rating')
    
    context = {
        'products': products,
        'search_term': query,
        'current_category': category_filter,
        'current_sorting': sorting,
    }
    
    return render(request, 'products/products.html', context)
# views.py
def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_active=True)
    
    context = {
        'products': products,
        'current_category': category,
    }
    
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Fetch reviews for the current product
    reviews = Review.objects.filter(product=product)

    # Include the review form for adding new reviews
    review_form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'products/product_detail.html', context)
