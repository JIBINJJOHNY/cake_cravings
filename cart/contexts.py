# cart/contexts.py
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
            product = get_object_or_404(Product, pk=item_id)
            item_total = item_data * product.price
            total += item_total
            product_count += item_data
            cart_items.append({
                'product_id': item_id,
                'quantity': item_data,
                'product': product,
                'item_total': item_total,
            })

    delivery_rates = {
        'pickup': Decimal('0.00'),
        'local_delivery': Decimal('2.00'),  # Fixed rate for local delivery
        'national_delivery': Decimal('5.00'),  # Fixed rate for national delivery
    }

    delivery_rate = delivery_rates.get(selected_delivery_option, Decimal('0.00'))
    delivery = total * delivery_rate

    # Free delivery threshold
    free_delivery_threshold = Decimal('50.00')  # Free delivery for orders over €50

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

    if selected_delivery_option == 'local_delivery':
        context['delivery'] = min(delivery, Decimal('2.00'))

    return context
