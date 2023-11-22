from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from products.models import Product
from .contexts import cart_contents
from django.contrib import messages

def view_cart(request):
    """A view that renders the cart contents page"""

    # Call the cart context function to get the required data
    cart_contents_data = cart_contents(request)

    if request.is_ajax():
        # If it's an AJAX request, return a JSON response with updated cart details
        response_data = {
            'cart_items': cart_contents_data['cart_items'],
            'total': cart_contents_data['total'],
            'product_count': cart_contents_data['product_count'],
            'delivery': cart_contents_data['delivery'],
            'free_delivery_threshold': cart_contents_data['free_delivery_threshold'],
            'grand_total': cart_contents_data['grand_total'],
        }
        return JsonResponse(response_data)
    else:
        # If it's a regular request, render the HTML template with the cart context data
        return render(request, 'cart/cart.html', cart_contents_data)



def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size')

    # Get the current cart from the session
    cart = request.session.get('cake_cravings_cart', {})
    
    # Update the cart based on the selected size and quantity
    if size:
        if item_id in cart and size in cart[item_id]['items_by_size']:
            cart[item_id]['items_by_size'][size] += quantity
        else:
            cart[item_id] = {'items_by_size': {size: quantity}}
        messages.success(request, f'Successfully added size {size.upper()} {product.name} to your cart.')
    else:
        if item_id in cart:
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity
        messages.success(request, f'Successfully added {product.name} to your cart.')

    # Save the updated cart back to the session
    request.session['cake_cravings_cart'] = cart

    # Get messages as a list of strings
    message_list = [str(message) for message in messages.get_messages(request)]

    # Get cart contents data
    cart_contents_data = cart_contents(request)

    # Prepare the JSON response
    response_data = {
        'success': True,
        'message_alert': '\n'.join(message_list),
        'total': cart_contents_data['total'],
        'product_count': cart_contents_data['product_count'],
    }

    return JsonResponse(response_data)

def update_cart(request, item_id):
    """Adjust the quantity of the specified product in the shopping cart"""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']

    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {cart[item_id]["items_by_size"][size]}')
        else:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your cart')
    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart')

    request.session['cart'] = cart

    # Send a JSON response with updated cart details
    cart_contents = cart_contents(request)
    response_data = {
        'success': True,
        'message_alert': messages.get_messages(request),
        'total': cart_contents['total'],
        'product_count': cart_contents['product_count'],
    }
    return JsonResponse(response_data)

def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart"""
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None

        if 'product_size' in request.POST:
            size = request.POST['product_size']

        cart = request.session.get('cart', {})

        if size:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your cart')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart')

        request.session['cart'] = cart

        # Send a JSON response with updated cart details
        cart_contents = cart_contents(request)
        response_data = {
            'success': True,
            'message_alert': messages.get_messages(request),
            'total': cart_contents['total'],
            'product_count': cart_contents['product_count'],
        }
        return JsonResponse(response_data)
    except Exception as e:
        # Send a JSON response indicating the failure
        response_data = {'success': False, 'error_message': str(e)}
        return JsonResponse(response_data)

