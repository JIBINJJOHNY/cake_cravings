from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.conf import settings
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

    # Set delivery percentage based on the selected delivery option
    if selected_delivery_option == 'local_delivery':
        delivery_percentage = Decimal(10 / 100)  # Use 10% for local delivery
    elif selected_delivery_option == 'national_delivery':
        delivery_percentage = Decimal(20 / 100)  # Use 20% for national delivery
    else:
        # Default to a standard percentage if the delivery option is not recognized
        delivery_percentage = Decimal(0) 

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * delivery_percentage
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'selected_delivery_option': selected_delivery_option,
    }

    if selected_delivery_option == 'local_delivery':
        context['delivery'] = min(delivery, Decimal('2.00'))

    return context
