$(document).ready(function(){
    // Get total product length from data attribute of table
    let count = parseInt($('#cart-table').attr('data-cart'));

    const csrftoken = $('input[name ="csrfmiddlewaretoken"]').val();
    const totalPrice = $('#total-price');
    const totalQty = $('#total-qty');

    // Get cart from cookies≥
    let cart = Cookies.get("cart");

    // If cart is present parse to json
    if(cart) {
        cart = JSON.parse(cart);
        totalPrice.html("Total price fixed &euro; "+cart.totalPrice);
        totalQty.html("Total quantity "+cart.totalQty);
    }else {
        totalPrice.html("Total price fixed &euro; ");
        totalQty.html("Total quantity ");
    }

    // Create on change function to all the select input of the product list
    for(let i = 1; i <= count; i++) {
        const product = $('#select-'+i).attr('data-product');
        if(cart && product in cart){
            $('#select-'+i).val(cart[product].quantity)
        }

        // On change function for each select input
        $('#select-'+i).change(function () {
            // Check cart cookies
            cart = Cookies.get("cart");
            if(cart) {
                cart = JSON.parse(cart);
            }

            const $this = $(this);
            const $qty = parseInt($this.val());
            const $product = $this.attr('data-product');

            let body = {
                product: $product,
                quantity: $qty,
                cart: cart && cart.cart ? cart.cart : null // Add cart number if present in cookie or add null
            }

            // Update cart value from backend
            fetch('/cart/',{
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                headers: {
                  'Content-Type': 'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body: JSON.stringify(body) // body data type must match "Content-Type" header
            }).then(  res => {
                return res.json();
            }).then(data => {
                totalPrice.html("Total price fixed &euro; "+data.totalPrice);
                totalQty.html("Total quantity "+data.totalQty);
                console.log({data})
                body = {...body, cart: data.cart};
                cart = {...cart, [$product]: body,  cart: data.cart, totalPrice:data.totalPrice, totalQty:data.totalQty}
                Cookies.set('cart', cart);
            }).catch(err => {
                console.log({error: err})
            })
        });
    }

    // Click function to checkout cart items
    const orderButton = $('#orderbtn');
    orderButton.click(function(e){
        e.preventDefault();
        cart = Cookies.get("cart");
        if(cart) {
            cart = JSON.parse(cart);
            fetch('/process-order/',{
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                headers: {
                  'Content-Type': 'application/json',
                    'X-CSRFToken':csrftoken,
                },
                body: JSON.stringify({cart: cart.cart}) // body data type must match "Content-Type" header
            }).then(  res => {
                return res.json();
            }).then(data => {
                console.log({data})
                if(data.message && data.message === 'OK'){
                    // Delete cart cookies if checkout is success
                    Cookies.remove('cart');
                    // Redirect page
                    window.location.href = data.redirectURL;
                }
            }).catch(err => {
                console.log({error: err})
            });
        }
    });
});
