from decimal import Decimal
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from products.models import Product
from .contexts import cart_contents


class CartView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve cart contents and other relevant data
        contents = cart_contents(request)

        # Get the product IDs from the cart
        product_ids = [item['product_id'] for item in contents['cart_items']]

        # Fetch product details based on product IDs
        cart_products = Product.objects.filter(id__in=product_ids)

        # Create a dictionary mapping product IDs to product details
        cart_product_details = {product.id: product for product in cart_products}

        # Add product details to cart items
        for item in contents['cart_items']:
            # Use get to avoid KeyError
            product_id = item.get('product_id')
            if product_id and product_id in cart_product_details:
                item['product'] = cart_product_details[product_id]

        # Define the context variable
        context = {
            'cart_items': contents['cart_items'],
            'total': contents['total'],
            'product_count': contents['product_count'],
        }

        # Render the template with the defined context
        return render(request, 'cart.html', context)

class AddToCart(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided
            product = get_object_or_404(Product, pk=product_id)
            cart = request.session.get('cake_cravings_cart', {})
            message_alert = ''

            if product_id in cart:
                cart[product_id]['quantity'] += quantity
                request.session['cake_cravings_cart'] = cart
                quantity_added = quantity
                message_alert = f'{product.name} UPDATED. {quantity_added} added.'
            else:
                cart[product_id] = {'quantity': quantity}
                request.session['cake_cravings_cart'] = cart
                quantity_added = quantity
                message_alert = f'{product.name} ADDED TO CART. {quantity_added} added.'

            request.session['cake_cravings_cart'] = cart
            contents = cart_contents(request)
            total = contents['total']
            product_count = contents['product_count']

            return JsonResponse(
                {
                    'success': True,
                    'message_alert': message_alert,
                    'total': total,
                    'product_count': product_count,
                }
            )
        return JsonResponse({'success': False})
        return JsonResponse({'success': False})


class RemoveFromCart(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            cart = request.session.get('cake_cravings_cart', {})

            if product_id in cart:
                del cart[product_id]
                request.session['cake_cravings_cart'] = cart

                contents = cart_contents(request)
                total = contents['total']
                product_count = contents['product_count']

                return JsonResponse(
                    {
                        'success': True,
                        'total': total,
                        'product_count': product_count,
                    }
                )

        return JsonResponse({'success': False})

    def get(self, request, *args, **kwargs):
        # Your logic for handling GET requests
        # This might involve rendering a confirmation page or redirecting somewhere
        return JsonResponse({'success': False})
