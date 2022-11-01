from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, BasketItemSerializer, ProductsSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from .models import Basket, BasketItem, Item
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination


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

        '''
        ********************************** This working code *********************

        existed = BasketItem.objects.filter(basket=basket, item=serializer.validated_data['item'])

        if existed:
            existed = existed[0]
            existed.quantity += serializer.validated_data['quantity']
            existed.save()
            return Response({"data": 'success'})
        else:
            serializer.save(basket=basket)
            return Response({"data": serializer.data})
        '''

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


''' 
Searching by "POST" method

class ItemAPI(APIView):
    serializer = SearchSerializer()

    def get(self, request):
        item = Item.objects.all()
        serializer = ProductsSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = Item.objects.filter(name=serializer.data['item_name'])
        item_api = ProductsSerializer(item, many=True)

        if item:
            return Response(item_api.data)
        else:
            return Response('There is no such product')
'''

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
        

class ItemAPI(generics.ListAPIView):
    serializer_class = ProductsSerializer
    queryset = Item.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ["category"]
    search_fields = ("name", "price")
    pagination_class = StandardResultsSetPagination


class Purchase(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        cart, _ = Basket.objects.get_or_create(user=request.user)
        basket = BasketItem.objects.filter(basket=cart)
        
        for i in basket:
            item = Item.objects.get(name=i.item)
            item.number -= i.quantity
            item.save()

        basket.delete()
        return Response('You bought, thanks!!!')





