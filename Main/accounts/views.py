from multiprocessing import context
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import BasketSerializer, UserSerializer, RegisterSerializer, BasketItemSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from .models import Basket, BasketItem
from rest_framework.fields import CurrentUserDefault

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)


class BasketAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer = BasketItemSerializer()
    # cart = BasketSerializer()
    
    def post(self, request):
        serializer = BasketItemSerializer(data=request.data)
        basket, _ = Basket.objects.get_or_create(user=request.user)
        # user = request.user
        # cart = BasketSerializer(user=user.id)
        # if cart.is_valid():
        #     cart.save(user=request.user)

        if serializer.is_valid():
            # serializer.save(basket=request.cart)
            serializer.save(basket=basket)
            return Response({"data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def get(self, request):
        basket = BasketItem.objects.all()
        serializer = BasketItemSerializer(basket, many=True)
        return Response(serializer.data)
