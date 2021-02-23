# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=255, null=False, default="")
    price_ex_tax = models.DecimalField(max_digits=10, decimal_places=2)
    vat_choices = [
        (5.5, 5.5),
        (20, 20)
    ]
    vat = models.IntegerField(choices=vat_choices, default=0)
    ordered_stock = models.PositiveIntegerField()
    maximum_stock_available = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name

    @property
    def price_inc_vat(self):
        price = (self.price_ex_tax * self.vat)
        return "%.2f" % round(price, 2)

    @property
    def stock_available(self):
        return self.maximum_stock_available - self.ordered_stock


class Cart(models.Model):
    check_out = models.BooleanField(default=True)


class Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_items')
    quantity = models.PositiveIntegerField()

    @property
    def total_ttc(self):
        return self.product.price_inc_tax * self.quantity


