from django.http.response import (
    HttpResponse, 
    JsonResponse)

from django.shortcuts import (
    render, 
    redirect)

from store.models import ( 
    Category, 
    Product,)

from api.serializers import (
     
    CategorySerializer, 
    ListProductSerializer, 
    ProductDetailSerializer, 
    ProductAddSerializer,
    ProductSerializer,
    ProductByCatSerializer,
    ProductForSearchSerializer)

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


# api to list all products
class ProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ListProductSerializer(products, many=True)
        return Response(serializer.data)

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
class ProductDescription(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)
    


# api to POST
class ProductAdding(APIView):
    def post(self, request, format=None):
        serializer = ProductAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api to get, update and delete
class ProductDetail(APIView):
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


# API to list products by categories

class ProductListByCategory(ListAPIView):
    serializer_class = ProductByCatSerializer

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        return Product.objects.filter(category__name=category_name)

    def get_context_data(self, **kwargs):
        category_name = self.kwargs['category_name']
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(name=category_name)
        return context


# API for search functionality

class ProductForSearch(APIView):
    def get(self, request):
        q = request.GET.get('q')            # request . query params
        categoryFilter = request.GET.get('category')
        if categoryFilter:
            products = Product.objects.filter(category=categoryFilter)
        else:
            products = Product.objects.all()
        if q:
            products = products.filter(name__icontains=q)
        serializer = ProductForSearchSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# ----------------------------------
# ----------------------------------
# ----------------------------------

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