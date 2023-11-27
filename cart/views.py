# cart/views.py
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from products.models import Product
from .contexts import cart_contents
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.http import JsonResponse

def view_cart(request):
    context = cart_contents(request)
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart = request.session.get('cake_cravings_cart', {})

    if product_id in cart:
        cart[product_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {cart[product_id]}')
    else:
        cart[product_id] = quantity
        messages.success(request, f'Added {product.name} to your cart')

    request.session['cake_cravings_cart'] = cart
    return redirect(reverse('view_cart'))

def remove_from_cart(request, product_id):
    cart = request.session.get('cake_cravings_cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cake_cravings_cart'] = cart
    
    return redirect('view_cart')

def update_delivery_option(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        selected_option = request.POST.get('selected_delivery_option')
        request.session['delivery_option'] = selected_option

        cart_context = cart_contents(request)

        response_data = {
            'delivery': '{:.2f}'.format(cart_context['delivery']),
            'grand_total': '{:.2f}'.format(cart_context['grand_total']),
        }

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'})
