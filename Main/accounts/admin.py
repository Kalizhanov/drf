from django.contrib import admin
from .models import Category, Item, Basket, BasketItem

# Register your models here.
admin.site.register(Item)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Category)