from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm,UpdateReviewForm
from django.views.decorators.cache import never_cache
from products.models import Product
from django.views.decorators.csrf import csrf_protect

@login_required
@csrf_protect
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.rating = form.cleaned_data['rating']
            review.save()

            return JsonResponse({'message': 'Review added successfully'})

    return JsonResponse({'error': 'Invalid form submission'}, status=400)

@login_required
@csrf_protect
def edit_review(request, review_id):
    if request.method == 'POST':
        print('Received data:', request.POST)
        form = UpdateReviewForm(request.POST)
        if form.is_valid():
            # Process the valid form
            print('Form is valid')
            # ...

            # Return a JsonResponse or another appropriate HttpResponse
            return JsonResponse({'message': 'Review updated successfully'})

        else:
            # Log validation errors
            print('Form errors:', form.errors)
            return JsonResponse({'error': 'Invalid form submission'}, status=400)

    # Handle other cases, for example, return a redirect or render a template
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def view_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    context = {
        'product': product,
        'reviews': reviews,
        'current_user': request.user,
    }

    return render(request, 'view_review.html', context)
@login_required
@never_cache
@csrf_protect
def delete_review(request, product_id, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if request.method == 'GET':
        review.delete()
        return JsonResponse({'message': 'Review deleted successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
