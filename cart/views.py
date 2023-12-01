from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .contexts import cart_contents
from products.models import Product
from django.http import JsonResponse

def add_to_cart(request):
    if request.method == 'POST':
        # Access form data, including the image
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        # Retrieve the product from the database
        product = get_object_or_404(Product, id=product_id)

        # Your existing logic for processing the form data
        image_url = product.images.first().image_url if product.images.exists() else None
        print('Image URL:', image_url)  # Log image_url to the console

        cart_p = {
            str(product_id): {
                'image': image_url,
                'title': request.POST.get('title'),
                'qty': quantity,
                'price': request.POST.get('price'),
            }
        }

        if 'cartdata' in request.session:
            if str(product_id) in request.session['cartdata']:
                cart_data = request.session['cartdata']
                cart_data[str(product_id)]['qty'] = int(cart_p[str(product_id)]['qty'])
                cart_data.update(cart_data)
                request.session['cartdata'] = cart_data
            else:
                cart_data = request.session['cartdata']
                cart_data.update(cart_p)
                request.session['cartdata'] = cart_data
        else:
            request.session['cartdata'] = cart_p

        return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})


def view_cart(request):
    context = cart_contents(request)
    return render(request, 'cart/cart.html', context)

def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data

    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty']) * float(item['price'])

    t = render_to_string('ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})

def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']

    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data

    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty']) * float(item['price'])

    t = render_to_string('ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


def get_cart_count(request):
    if 'cartdata' in request.session:
        cart_count = len(request.session['cartdata'])
    else:
        cart_count = 0

    return JsonResponse({'cart_count': cart_count})
