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

# user = serializers.SlugRelatedField(slug_field='username', read_only=True)
# products = ProductsSerializer(many=True, read_only=True)


# user = User.objects.get(username="galymzhan")
# content_type = ContentType.objects.get_for_model(Item)
# permission = Permission.objects.get(
#     codename="view_item",
#     content_type=content_type
# )

# user.user_permissions.add(permission)
# user.user_permissions.remove(permission)


# class AdminPanel(APIView):
#     permission_classes = (permissions.IsAdminUser,)
#     serializer = ProductsSerializer()

#     @transaction.atomic
#     def post(self, request):
#         serializer = ProductsSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         existed, obj = Item.objects.update_or_create(
#             name = serializer.data['name'],
#             defaults=(
        

dict = {
    'name': 'SomeName',
    'surname': 'SomeSurname'
}

dict2 = {
    "name": 'AnotherName',
    'surname': "AnotherSurname"
}

for i, j in dict.items():
    print(dict2[i])

