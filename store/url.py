from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('store/',views.store,name='store'),

    path('update_item/',views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name="process_order"),
]
