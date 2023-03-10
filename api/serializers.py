'''
Serializers in Django REST Framework are responsible for converting objects
into data types understandable by javascript and front-end frameworks.
Serializers also provide deserialization, allowing parsed data to be converted
back into complex types, after first validating the incoming data.
'''

from rest_framework import serializers
from store.models import (
    Category, 
    Product,)



        ###
# to list all products
class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name']

# to list products and their detail
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','description']

# to add product
class ProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# getting the cateogry 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# to get all of the products
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'

class ProductByCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductForSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price', 'description', 'digital', 'image')



        ###