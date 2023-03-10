from django.forms import ModelForm

from .models import Product, Customer, OrderItem

from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name','email','profile_pic']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class OrderHistoryForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product']

