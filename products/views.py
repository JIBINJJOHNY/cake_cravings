from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.db.models.functions import Lower
from .models import Product, Category
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from reviews.forms import ReviewForm,UpdateReviewForm
from reviews.models import Review

@require_GET
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

def all_products(request, category_slug=None):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.filter(is_active=True)
    query = None
    sort = request.GET.get('sort', 'name')
    direction = request.GET.get('direction', 'asc')

    # Apply category filter if category_slug is provided
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if sort == 'name':
        sort_key = 'name' if direction == 'asc' else '-name'
    elif sort == 'price':
        sort_key = 'price' if direction == 'asc' else '-price'
    elif sort == 'rating':
        # Assuming 'rating' is a field in your Product model
        sort_key = 'rating' if direction == 'asc' else '-rating'
    else:
        # Default to sorting by name in ascending order
        sort_key = 'name'

    products = products.order_by(sort_key)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # Retrieve all categories for the category list
    all_categories = Category.objects.all()
    # Get total product count
    total_product_count = Product.objects.filter(is_active=True).count()
    print("Total Product Count:", total_product_count)
    # Get product counts for each category
    product_counts = Product.objects.values('category__name').annotate(count=Count('id'))

    current_sorting = f'{sort}_{direction}'
    # Add a success message
    messages.success(request, 'Successfully performed the action.')

    context = {
        'products': products,
        'search_term': query,
        'all_categories': all_categories,
        'product_counts': product_counts,
        'current_sorting': current_sorting,
        'selected_category_slug': category_slug,  # Pass the selected category slug for highlighting in the template
        'total_product_count': total_product_count,  
    }
    return render(request, 'products/products.html', context)
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Retrieve reviews for the specific product
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    # Create an instance of the ReviewForm
    review_form = ReviewForm()

    # Create a dictionary to hold instances of UpdateReviewForm for each review
    update_review_forms = {review.id: UpdateReviewForm(initial={'rating': review.rating, 'comment': review.comment})
                           for review in reviews}

    if request.method == 'POST':
        # Call the add_to_cart function from the cart app
        add_to_cart(request, product_id)

    context = {
        'product': product,
        'reviews': reviews,
        'reviewForm': review_form,
        'updateReviewForms': update_review_forms,
    }

    return render(request, 'products/product_detail.html', context)
