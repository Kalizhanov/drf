from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    

class BasketItem(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)