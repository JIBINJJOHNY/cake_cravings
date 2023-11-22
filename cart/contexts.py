# contexts.py
from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_contents(request):
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cake_cravings_cart', {})
    selected_delivery_option = request.session.get('delivery_option', 'pickup')

    for item_id, item_data in cart.items():
        if isinstance(item_data, int):
            cake = get_object_or_404(Product, pk=item_id)
            total += item_data * cake.price
            product_count += item_data
            cart_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'cake': cake,
            })

    # Customize delivery logic based on the selected option
    if selected_delivery_option == 'pickup':
        delivery = 0
    elif selected_delivery_option == 'local_delivery':
        delivery = total * Decimal('0.05')  # 5% of total for local delivery
    elif selected_delivery_option == 'national_delivery':
        delivery = total * Decimal('0.1')  # 10% of total for national delivery
    else:
        # Default to pickup if the selected option is not recognized
        delivery = 0

    free_delivery_threshold = Decimal('50.00')  # Free delivery for orders over $50
    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_threshold': free_delivery_threshold,
        'grand_total': grand_total,
        'selected_delivery_option': selected_delivery_option,
    }

    return context
