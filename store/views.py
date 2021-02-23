from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from .util import cartData, cookieCart
from .models import Product
# Create your views here.


def home(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if cartItems <= 0:

        return redirect('store')

    else:

        context = {'cardItems':cartItems,'order':order,'items':items}

        return render(request,'store/cart.html',context)


def checkout(request):
    pass


def store(request):

    data = cartData(request)
    order = data['order']
    items = data['items']
    cartItems = data['cartItems']


    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems}
    return render(request, 'store/store.html',context)


def updateItem(request):
    pass


def processOrder(request):
    pass
