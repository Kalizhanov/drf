from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from .models import Basket, BasketItem, Item
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.db import transaction


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
    
    def post(self, request):
        serializer = BasketItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        basket, _ = Basket.objects.get_or_create(user=request.user)

        existed, obj = BasketItem.objects.update_or_create(
            basket=basket, 
            item=serializer.validated_data['item'],
            defaults={'quantity' : serializer.validated_data['quantity']}
            )

        return Response({"data": 'success'})

    def get(self, request):
        cart, _ = Basket.objects.get_or_create(user=request.user)
        basket = BasketItem.objects.filter(basket=cart)
        serializer = BasketItemSerializer(basket, many=True)
        return Response(serializer.data)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
        

class ItemAPI(generics.ListAPIView):
    serializer_class = ProductsSerializer
    queryset = Item.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ["category"]
    search_fields = ("name", "price")
    pagination_class = StandardResultsSetPagination

    
class SingleItem(APIView):
    serializer = ProductsSerializer()

    
    def get(self, request, pk):
        item = Item.objects.get(id=pk)
        item.viewed += 1
        item.save()

        serializer = ProductsSerializer(item)

        return Response(serializer.data)


class BestSelling(generics.ListAPIView):
    serializer_class = ProductsSerializer
    queryset = Item.objects.order_by('-sold')[:3]


class Popular(generics.ListAPIView):
    serializer_class = ProductsSerializer
    queryset = Item.objects.order_by('-viewed')


class Purchase(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        cart, _ = Basket.objects.get_or_create(user=request.user)
        basket = BasketItem.objects.filter(basket=cart)
        
        for i in basket:
            item = Item.objects.get(name=i.item)
            item.number -= i.quantity
            item.sold += i.quantity
            item.save()

        try:    
            basket.delete()
        except:
            print('Error!')

        return Response('You bought, thanks!!!')





