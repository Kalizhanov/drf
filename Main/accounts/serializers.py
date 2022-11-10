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


class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    price = serializers.DecimalField(required=False, max_digits=9, decimal_places=2)
    description = serializers.CharField(required=False)

    class Meta:
        model = Item
        fields = ("__all__")


class BasketSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Basket
        fields = (
            "user",
        )


class BasketItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasketItem
        fields = ("item", "quantity")

    

    
        

    
