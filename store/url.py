from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    path('cart/',views.cart,name='cart'),
    path('store/',views.store,name='store'),
    path('process-order/', views.processOrder, name="process_order"),
]
