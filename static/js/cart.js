// Add to cart
$(document).on('click', ".add-to-cart", function () {
    var _vm = $(this);
    var _index = _vm.attr('data-index');
    var _qty = $(".product-qty-" + _index).val();
    var _productId = $(".product-id-" + _index).val();
    var _productImage = $(".product-image-" + _index).val();
    var _productTitle = $(".product-title-" + _index).val();
    var _productPrice = $(".product-price-" + _index).text();
    // Ajax
    $.ajax({
        url: '/add-to-cart/',
        method: 'POST', // Assuming you are using POST method for adding to cart
        data: {
            'id': _productId,
            'image': _productImage,
            'qty': _qty,
            'title': _productTitle,
            'price': _productPrice
        },
        dataType: 'json',
        beforeSend: function () {
            _vm.attr('disabled', true);
        },
        success: function (res) {
            $(".cart-list").text(res.totalitems);
            _vm.attr('disabled', false);
        },
        error: function (error) {
            console.error('Error adding to cart:', error);
            _vm.attr('disabled', false);
        }
    });
    // End
});

// Delete item from cart
$(document).on('click', '.delete-item', function () {
    var _pId = $(this).attr('data-item');
    var _vm = $(this);
    // Ajax
    $.ajax({
        url: '/delete-from-cart/',
        method: 'POST', // Assuming you are using POST method for deleting from cart
        data: {
            'id': _pId,
        },
        dataType: 'json',
        beforeSend: function () {
            _vm.attr('disabled', true);
        },
        success: function (res) {
            $(".cart-list").text(res.totalitems);
            _vm.attr('disabled', false);
            $("#cartList").html(res.data);
        },
        error: function (error) {
            console.error('Error deleting from cart:', error);
            _vm.attr('disabled', false);
        }
    });
    // End
});

// Update item from cart
$(document).on('click', '.update-item', function () {
    var _pId = $(this).attr('data-item');
    var _pQty = $(".product-qty-" + _pId).val();
    var _vm = $(this);
    // Ajax
    $.ajax({
        url: '/update-cart/',
        method: 'POST', // Assuming you are using POST method for updating the cart
        data: {
            'id': _pId,
            'qty': _pQty
        },
        dataType: 'json',
        beforeSend: function () {
            _vm.attr('disabled', true);
        },
        success: function (res) {
            // $(".cart-list").text(res.totalitems);
            _vm.attr('disabled', false);
            $("#cartList").html(res.data);
        },
        error: function (error) {
            console.error('Error updating cart item:', error);
            _vm.attr('disabled', false);
        }
    });
    // End
});


function updateCartCount() {
    var cartCountElement = document.getElementById('cart-count');

    if (!cartCountElement) {
        console.error('Cart count element not found.');
        return;
    }

    // Fetch the cart data from the session or wherever it's stored
    var cartData = JSON.parse(localStorage.getItem('cartdata')) || {};

    // Calculate the total items in the cart
    var totalItems = Object.keys(cartData).length;

    // Update the cart count in the navbar
    cartCountElement.textContent = totalItems;

    console.log('Cart count updated:', totalItems);
}


// Update the form with a unique ID
var addToCartForm = document.getElementById('addToCartForm');

addToCartForm.addEventListener('submit', function (event) {
    event.preventDefault();

    // Make an AJAX request to add the product to the cart
    $.ajax({
        url: addToCartForm.action,
        type: addToCartForm.method,
        data: $(addToCartForm).serialize(),
        success: function (response) {
            console.log('Success:', response);

            // Log the received data
            console.log('Received data:', response.data);

            // Assuming response.data is an array of added products
            var addedProducts = response.data;

            // Update the cart count in the navbar using the response data
            var cartCountElement = document.getElementById('cartCount');
            cartCountElement.textContent = response.totalitems;

            // Log before updating the cart content
            console.log('Before updating cart content:', addedProducts);

            // Update the cart content or display a success message
            updateCartContent(addedProducts);

            // Log after updating the cart content
            console.log('After updating cart content:', addedProducts);

            // ... (your existing code for handling the response)
        },
    })
})

function updateCartContent(addedProducts) {
    console.log('updateCartContent called with data:', addedProducts);
    // Assuming there is a container element with id="cartContent" to display the added products
    var cartContentElement = document.getElementById('cartContent');

    // Clear the existing content
    cartContentElement.innerHTML = '';

    // Check if addedProducts is an object
    if (typeof addedProducts === 'object' && Object.keys(addedProducts).length > 0) {
        // Iterate through the added products and append them to the cart content
        for (var key in addedProducts) {
            if (addedProducts.hasOwnProperty(key)) {
                appendProductToCart(addedProducts[key], cartContentElement);
            }
        }
    } else {
        console.error('addedProducts is not a non-empty object:', addedProducts);
    }

    // Display a success message or perform other actions
    var successMessage = document.createElement('p');
    successMessage.textContent = 'Product(s) added to the cart successfully!';
    cartContentElement.appendChild(successMessage);
}

function appendProductToCart(product, containerElement) {
    var productElement = document.createElement('div');
    productElement.innerHTML = `
        <img src="${product.image}" alt="${product.title}">
        <span>${product.title}</span>
        <span>Quantity: ${product.qty}</span>
        <span>Price: ${product.price}</span>
    `;
    containerElement.appendChild(productElement);
}

function appendProductToCart(product, containerElement) {
    var productElement = document.createElement('div');

    // Set a default image URL using the base URL for static files
    var imageUrl = product.image ? product.image : window.staticBaseUrl + 'images/default_image.png';

    productElement.innerHTML = `
        <img src="${imageUrl}" alt="${product.title}">
        <span>${product.title}</span>
        <span>Quantity: ${product.qty}</span>
        <span>Price: ${product.price}</span>
    `;
    containerElement.appendChild(productElement);
}