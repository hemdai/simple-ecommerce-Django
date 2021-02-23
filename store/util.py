import json
from .models import Product


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart={}
    print('Cart:', cart)
    #Create Empty cart for now for none-logged in users
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)

        except:
            pass
    return {'cartItems':cartItems, 'order':order,'items':items }


def cartData(request):
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
    return {'cartItems':cartItems,'order':order,'items':items}