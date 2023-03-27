from django.http.response import (
    HttpResponse, 
    JsonResponse)

from django.shortcuts import (
    render, 
    redirect)

from store.models import ( 
    Category, 
    Product,
    Customer)

from api.serializers import (
    StoreProductsSerializer,
    UserSerializer,
    UserLogInSerializer,
    CustomerSerializer,
    )

from rest_framework import status, generics

from rest_framework.views import APIView

from rest_framework.generics import ListAPIView

from rest_framework.decorators import api_view

from rest_framework.response import Response

from django.core import serializers

from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LogoutView

from .permissions import IsSuperUser

# for basic auth
from rest_framework.permissions import IsAuthenticated

# for token auth
from rest_framework.authtoken.models import Token




# API to list all products
class ListProductView(ListAPIView):
    queryset=Product.objects.all()
    serializer_class=StoreProductsSerializer



class ListProductView(APIView):
    def get(self, request, format=None):
        products = Product.objects.values(
            'id',
            'name',
            'category',
            'price',
            'description',
            'digital',
            'image')
        serializer = StoreProductsSerializer(data=products, many=True)
        serializer.is_valid()
        return Response(serializer.data)
    

# API to Create Product
class CreateProductView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = StoreProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to Retrieve, Update and Delete
class ProductRetrieveUpdateAndDeleteView(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id, format=None):
        product = self.get_object(id)
        serializer = StoreProductsSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        product = self.get_object(id)
        serializer = StoreProductsSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# API to list products by category
class ListProductByCategoryView(ListAPIView):
    serializer_class = StoreProductsSerializer

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        return Product.objects.filter(category__name=category_name)

# APi to search
class ProductSearchView(APIView):
    def get(self, request):
        q = request.GET.get('q')            # request . query params
        categoryFilter = request.GET.get('category')
        if categoryFilter:
            products = Product.objects.filter(category=categoryFilter)
        else:
            products = Product.objects.all()
        if q:
            products = products.filter(name__icontains=q)
        serializer = StoreProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Api for registration:
class UserRegistrationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # email = request.data.get('email')
        
        if not username or not password:     #or not email:
            # If any required field is missing, return an error response.
            return Response({'error': 'Username and password are required.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Create a new user with the provided data.
            user = User.objects.create_user(username=username, password=password)   # email=email)
            #token = Token.objects.create(user=user)
            # Return a success response with the created user and auth token data.
            return Response({
                'id': user.id,
                'username': user.username,
                # 'email': user.email,
                # 'auth_token': token.key
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            # If there's any error while creating the user, return an error response.
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# API to log a user in:
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):

        serializer = UserLogInSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk
            })
        
        return Response({'error': 'Username or password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)


# API to log a user out:
class LogoutAPIView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({'message': 'User logged out successfully'})  

          
# API to create User
class CreateUserView(APIView):
    def post(self, request, format=None):
        if not request.user.is_superuser:
            return Response({'message':'Only superusers can create users.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# APIT to view all Customers
class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # def get(self, request, format=None):
    #     customers = Customer.objects.values(
    #         'user',
    #         'name',
    #         'verification_token',
    #         'email',
    #         'profile_pic')
    #     serializer = CustomerSerializer(data=customers, many=True)
    #     serializer.is_valid()
    #     return Response(serializer.data)


# API to activate/deactivate users

class UserActivationView(APIView):
    permission_classes = [IsSuperUser]

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user.is_active = False
        user.save()
        return Response({'is_active': user.is_active})










# api to list all products
'''
class ListProductView(APIView):
    def get(self, request, format=None):
        products = Product.objects.values('id', 'name')
        serializer = StoreProductsSerializer(data=products, many=True)
        serializer.is_valid()
        return Response(serializer.data)
'''



    # def post(self, request, format=None):
    #     ''' 
    #     create a products serializer,
    #     instead of passing in some value,
    #     we're going to get that data from the request.
    #     '''
    #     serializer = ListProductSerializer(data=request.data)
    #     # check to see if the data is valid
    #     if serializer.is_valid():
    #         # save it
    #         serializer.save()
    #         # return a response, pass a status code
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         # if data is not valid, we send in an error and a status code
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# api to view detail of each product and add new product
'''
class DescribeProductView(APIView):
    def get(self, request, format=None):
        products = Product.objects.values('id','name','description')
        serializer = StoreProductsSerializer(products, many=True)
        return Response(serializer.data)
'''

    


# api to POST
'''
class CreateProductView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = ProductAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''



# api to get, update and delete
'''
class ProductGetPutDel(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''



# API to list products by categories
'''
class ProductListByCategory(ListAPIView):
    serializer_class = ProductByCatSerializer

    def get_queryset(self):
        print("=====get request=======")
        category_name = self.kwargs.get('category_name')
        return Product.objects.filter(category__name=category_name)
'''


    # def get_context_data(self, **kwargs):
    #     print("=====context=====")
    #     category_name = self.kwargs['category_name']
    #     context = super().get_context_data(**kwargs)

        

    #     print("=====context parent========",context)
    #     context['category'] = Category.objects.get(name=category_name)
    #     return context


# API for search functionality
'''
class SearchProduct(APIView):
    def get(self, request):
        q = request.GET.get('q')            # request . query params
        categoryFilter = request.GET.get('category')
        if categoryFilter:
            products = Product.objects.filter(category=categoryFilter)
        else:
            products = Product.objects.all()
        if q:
            products = products.filter(name__icontains=q)
        serializer = SearchProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
'''




# ----------------------------------
# ----------------------------------
# ----------------------------------
'''
class UserRegistrationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # email = request.data.get('email')
        
        if not username or not password:     #or not email:
            # If any required field is missing, return an error response.
            return Response({'error': 'Username and password are required.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Create a new user with the provided data.
            user = User.objects.create_user(username=username, password=password)   # email=email)
            #token = Token.objects.create(user=user)
            # Return a success response with the created user and auth token data.
            return Response({
                'id': user.id,
                'username': user.username,
                # 'email': user.email,
                # 'auth_token': token.key
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            # If there's any error while creating the user, return an error response.
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
'''







# class LoginAPIView(APIView):
#     def post(self, request, format=None):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         try:
#             user = User.objects.get(username=username)
#         except:
#             return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
#         user = authenticate(request, username=username, password=password)
    
#         if user is not None:
#             token = Token.objects.create(user=user)
#             print(token.key)
#             # login(request, user)
#             # if user.is_superuser:
#             #     return Response({'redirect': 'adminDashboard2'})
#             return Response({'token': token})
#         else:
#             return Response({'error': 'Username or password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        

'''
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):

        serializer = UserLogInSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk
            })
        
        return Response({'error': 'Username or password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({'message': 'User logged out successfully'})  

          

class CreateUserView(APIView):
    def post(self, request, format=None):
        if not request.user.is_superuser:
            return Response({'message':'Only superusers can create users.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

# @api_view(['GET','POST'])
# def product_list(request, format=None):
#     if request.method == 'GET':
#         name = request.GET.get('name', '')
#         products = Product.objects.filter(name__icontains=name)
#         serializer = ProductSerializer(products, many=True)
#         return JsonResponse({'products':serializer.data}, safe=False)
#     if request.method == 'POST':
#         serializer=ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

###


# list all products
# @api_view(['GET', 'POST'])
# def product_list(request, format=None):
#     print("====methods====")
#     if request.method == 'GET':
#         name = request.query_params.get('name')
#         if name:
#             products = Product.objects.filter(name__icontains=name)
#         else:
#             products = Product.objects.all()
#         serializer = ListProductSerializer(products, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ListProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# * * *

# class ProductList(APIView):
#     def get(self, request, format=None):
#         products = Product.objects.all()
#         serializer = ListProductSerializer(products, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = ListProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



'''
class ProductList(APIView):

This defines a class named ProductList that inherits from the APIView class in Django REST Framework.
APIView is a class-based view that provides many helper methods to create API views.

def get(self, request, format=None):
This defines a method named get that handles HTTP GET requests.
The self argument refers to the instance of the ProductList class,
while request is an instance of the Request class that represents the incoming HTTP request.
The format argument is used to specify the content type of the response,
but since it's not used in the implementation, it's set to None.

name = request.query_params.get('name') retrieves the value of the name query parameter from the request's query parameters.
If name is not None, it filters the Product objects by name using Product.objects.filter(name__icontains=name).
If name is None, it returns all Product objects using Product.objects.all().

The resulting queryset is passed to a ListProductSerializer instance called serializer.
The many=True argument indicates that serializer should serialize multiple Product instances, not just one.
Finally, serializer.data is returned as a response using Response(serializer.data).

def post(self, request, format=None):

This defines a method named post that handles HTTP POST requests.
The self, request, and format arguments are the same as in the get method.
A ListProductSerializer instance called serializer is created with request.data as its data argument.
request.data contains the parsed request payload.
If serializer.is_valid() returns True, the serializer.save() method is called to create a new Product instance using the serialized data.
Response(serializer.data, status=status.HTTP_201_CREATED) is returned as a response.
If serializer.is_not_valid() returns False, Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) is returned instead.
'''


# * * *

# class ProductDescription(APIView):
#     def get(self, request, format=None):
#         products = Product.objects.all()
#         serializer = ProductDetailSerializer(products, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = ProductDetailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# product description api
# @api_view(['GET', 'POST'])
# def product_description(request, format=None):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductDetailSerializer(products, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductDetailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET','PUT','DELETE'])
# def product_detail(request, id, format=None):
#     try:
#         product = Product.objects.get(pk=id) 
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
        
#         instance = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(instance, data=request.data ,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# * * *

# class ProductDetail(APIView):
#     def get_object(self, id):
#         try:
#             return Product.objects.get(pk=id)
#         except Product.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
    
#     def get(self, request, id, format=None):
#         product = self.get_object(id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, id, format=None):
#         product = self.get_object(id)
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, id, format=None):
#         product = self.get_object(id)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

'''
The first line class ProductDetail(APIView):
creates a new class called ProductDetail that extends the APIView class provided by Django REST Framework.

The get_object method is defined to retrieve a single Product object based on the id parameter passed to it.
If the object is not found, the method returns a Response object with a status code of 404 Not Found.

The get method is defined to handle HTTP GET requests for a single product.
It calls the get_object method with the id parameter to retrieve the product,
then uses the ProductSerializer to serialize the product object and return the serialized data as a response.

The put method is defined to handle HTTP PUT requests for a single product.
It also calls the get_object method with the id parameter to retrieve the product.
It then uses the ProductSerializer to deserialize the request data and validate it against the serializer's fields.
If the data is valid, the serializer saves the updated data to the product object and returns the updated data as a response.
If the data is invalid, the method returns a Response object with a status code of 400 Bad Request.

The delete method is defined to handle HTTP DELETE requests for a single product.
It calls the get_object method with the id parameter to retrieve the product, and then deletes the product from the database.
It returns a Response object with a status code of 204 No Content to indicate that the deletion was successful and no content is returned.

Overall, this code defines a class-based view that provides CRUD (Create, Read, Update, Delete) operations for a single Product object.
'''

        

        
###

# @api_view(['GET','POST'])
# def product_list(request, format=None):
#     # check for GET
#     if request.method == 'GET':

#         # get all the products
#         products = Product.objects.all()

#         # serialize them
#         serializer = ProductSerializer(products, many=True)

#         # return json ( old way )
#         #   return JsonResponse({'products':serializer.data})
#         # using the method we did below ( updated )
#         return JsonResponse({'products':serializer.data}, safe=False)

#     # check for POST
#     '''
#     take the data they sent us,
#     deserialize it,
#     and then create a product object out of it
#     '''
#     if request.method == 'POST':
#         ''' 
#         create a products serializer,
#         instead of passing in some value,
#         we're going to get that data from the request.
#         '''
#         serializer=ProductSerializer(data=request.data)
#         # check to see if the data is valid
#         if serializer.is_valid():
#             # save it
#             serializer.save()
#             # return a response, pass a status code
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET','PUT','DELETE'])
# def product_detail(request, id, format=None):
#     '''
#     We passed in an extra parameter in our urls.py : '<int:id>'
#     The value of this is going to be sent to views in - def product_detail(request, id): into the id variable
#     So we can get a product by it's id using the id variable in (pk=id) and assigning it to the pk parameter
#     And we can check to see if this is valid...
#     so we can say 
#     try:
#     and it can throw an exception
#     except:
#     '''
#     # checking if it is a valid request,
#     # and we can use the product object throughout
#     # so we'll assign our query set to a variable product
#     # so we can refer to drink without having to go through the process down again and again
#     try:
#         product = Product.objects.get(pk=id)
#     # if something goes wrong, this exception will be hit    
#     except Product.DoesNotExist:
#         # return a response
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         # creating a product serializer which will take the object to GET
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         # serializer is a new product serializer, pass-in product as we'll be updating product
#         # we need to pass in the data so (data=request.data)
        
#         instance = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(instance, data=request.data ,partial=True)
#         # check to see if it's valid
#         if serializer.is_valid():
#             # save the data
#             serializer.save()
#             # return response(serializer.data)
#             return Response(serializer.data)
#         # if it's not valid 
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         # to delete , just product.delete()
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


'''
class ProductListByCategory(ListAPIView):
    serializer_class = ProductByCatSerializer

This creates a class called ProductListByCategory 
that inherits from the ListAPIView class provided by Django REST Framework (DRF).

serializer_class is a class attribute that specifies 
which serializer should be used to serialize the queryset. 
In this case, it's ProductByCatSerializer.



    def get_queryset(self):
        category_name = self.kwargs['category_name']
        return Product.objects.filter(category__name=category_name)

get_queryset is a method provided by DRF that returns 
the queryset of objects that will be used to generate the response.

self refers to the instance of the view class that is currently being used.

self.kwargs is a dictionary containing the URL keyword arguments 
captured by the URL dispatcher. 

In this case, category_name is one of those arguments.

Product.objects.filter(category__name=category_name) 
is a query that filters the Product objects based on their related Category name. 
The double underscore notation is used to follow the 
relationship between the Product and Category models.



    def get_context_data(self, **kwargs):
        category_name = self.kwargs['category_name']
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(name=category_name)
        return context

get_context_data is another method provided by DRF 
that returns the additional context that will be used to generate the response.

category_name is retrieved from the URL keyword arguments 
just like in the get_queryset method.

super() is used to call the parent class's implementation of get_context_data.
context is set to the result of calling the parent class's implementation of 
get_context_data with the keyword arguments passed into this method.

Category.objects.get(name=category_name) retrieves the Category object 
with the specified name.
context['category'] adds the Category object to the context dictionary, 
which will be used to generate the response.
'''