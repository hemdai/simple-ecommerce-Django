from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Item, Cart
from django.db.models import F
from .forms import ProductForm
from django.urls import reverse
import json
# Create your views here.
from django import template

register = template.Library()

def home(request):
    """
    returning just normal page
    """
    context = {}
    return render(request, "store/main.html", context)

def create_response(items):
    print(items.count)
    item_quantity = 0
    total_price = float(0)
    response_data = {"totalQty": item_quantity,"totalPrice": total_price}
    if not items:
        print("here is none")
        return response_data

    for item in items:
        quantity = item.quantity
        item_quantity += quantity
        item_price = item.total_ttc
        total_price += item_price
        response_data = {"totalQty": item_quantity, "totalPrice": total_price}
    return response_data


def cart(request):
    if request.method == 'GET':
        # get only such products which stock available is greater than 0
        products = [obj for obj in Product.objects.all() if obj.stock_available > 0]
        context = {"products": products}

        return render(request, 'store/cart.html', context)

    elif request.method == 'POST':
        data = json.loads(request.body)

        # in case cart is already exist
        if data['cart']:
            item_object = {
                "cart_id": int(data['cart']),
                "product_id": int(data['product']),
                "quantity": int(data['quantity'])
            }
            # check cart and product already exist or not and update if exist
            update_quantity = Item.objects.filter(
                cart_id=item_object['cart_id'],
                product_id=item_object['product_id']).update(quantity=item_object['quantity'])

            # if cart and product exist return the calculated details
            if update_quantity:
                # remove product from item if value is 0
                if item_object['quantity'] == 0:
                    Item.objects.filter(product_id=item_object['product_id']).delete()
                    cartItems = Item.objects.filter(cart_id=item_object['cart_id'])
                    for items in cartItems:
                        print(items)
                    response_data = create_response(cartItems)
                    response_data['cart'] = item_object['cart_id']
                    print("response data", response_data)
                    return HttpResponse(json.dumps(response_data), content_type="application/json")

                cartItems = Item.objects.filter(cart_id=item_object['cart_id'])
                response_data = create_response(cartItems)
                response_data['cart'] = item_object['cart_id']
                """
                item_quantity = 0
                total_price = float(0)
                for item in cartItems:
                    quantity = item.quantity
                    item_quantity += quantity
                    item_price = item.total_ttc
                    total_price += item_price

                response_data = {"totalQty": item_quantity, "totalPrice": total_price, "cart": item_object['cart_id']}
                """

                return HttpResponse(json.dumps(response_data), content_type="application/json")

            # if cart exists but products is not in Item list then create new product
            # and return the calculated details of total and quantity wit cart id
            cartItem = Item.objects.create(**item_object)
            cartItems = Item.objects.filter(cart_id=item_object['cart_id'])
            response_data = create_response(cartItems)
            response_data['cart'] = item_object['cart_id']
            """
            item_quantity = 0
            total_price = float(0)
            for item in cartItems:
                quantity = item.quantity
                item_quantity += quantity
                item_price = item.total_ttc

                total_price += item_price
            response_data = {"totalQty":item_quantity, "totalPrice":total_price, "cart": item_object['cart_id']}
            """

            return HttpResponse(json.dumps(response_data), content_type="application/json")

        # if there is no cart exist, then create new cart and after that create product and quantity in Item
        # after that return the total price and quantity and cart id
        cart = Cart.objects.create()
        item_object = {
            "cart_id": cart.id,
            "product_id": int(data['product']),
            "quantity": int(data['quantity'])
        }
        cartItem = Item.objects.create(**item_object)
        item_quantity = item_object['quantity']
        total_price = cartItem.total_ttc

        response_data = {"totalQty":item_quantity, "totalPrice":total_price, "cart": cart.id}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def store(request):
    """
    as from the back office the store objects are creating here.
    """

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse('home'))

            except:
                pass
        return HttpResponse("Error in saving form")

    elif request.method == 'GET':
        form = ProductForm
        context = {'message':"create your new product", "form":form}
        return render(request, 'store/store.html', context)


def updateItem(request):
    pass

def processOrder(request):
    """
    Here the process if completing. The available stock quantity is updating here with ordered Items.
    similarly the cart is being check out here.
    """

    data = json.loads(request.body)
    cart = data['cart']
    cartItems = Item.objects.filter(cart_id=cart)
    for items in cartItems:
        Product.objects.filter(
            id=items.product.id
        ).update(maximum_stock_available=F('maximum_stock_available') - int(items.quantity))
    response_message = {"message":"OK", "redirectURL":"/cart/"}
    Cart.objects.filter(id=cart).update(check_out=True)
    return HttpResponse(json.dumps(response_message), content_type="application/json")


