from dataclasses import fields
from email.policy import default
import numbers
from statistics import quantiles
from xml.etree.ElementInclude import include
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password']) 

        return user              


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("__all__")


class BasketSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    # products = ProductsSerializer(many=True, read_only=True)
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Basket
        fields = (
            "user",
        )


class BasketItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasketItem
        fields = ("item", "quantity")

    

    
        

    
