from django.contrib import admin

# Register your models here.
from .models import (
    Product,
    Cart,
    Item
)

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Item)

