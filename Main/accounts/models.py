from email.policy import default
from queue import Empty
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
    number = models.PositiveIntegerField(default=0)                 #number of products that we have
    sold = models.PositiveIntegerField(default=0)                   #number of sold the product
    viewed = models.PositiveIntegerField(default=0)                 #how many times this product was viewed

    def __str__(self):
        return self.name


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    

class BasketItem(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



