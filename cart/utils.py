# cart/utils.py

def cart_contents(request):
    cart = request.session.get('cart', {})
    total = 0
    product_count = 0

    for item_id, quantity in cart.items():
        # Retrieve product information and calculate total
        # Adjust this part based on your actual implementation
        pass  # Placeholder, replace with your actual code

    context = {
        'cart': cart,
        'total': total,
        'product_count': product_count,
    }

    return context
