from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from ckeditor.fields import RichTextField


# Create your models here.

# class Customer(AbstractUser):

# 	verification_token = models.CharField(max_length=32, null=True)
# 	image = models.ImageField(null=True, blank=True)

# 	def __str__(self):
# 		return self.username

# 	@property
# 	def imageURL(self):
# 		try:
# 			url = self.image.url
# 		except:
# 			url = ''
# 		return url

class Customer(models.Model):
	# OneToOne - a user can only have one customer, customer can only have one user
	# [on_delete=models.CASCADE] delete this item if the user item is deleted
	user = models.OneToOneField(User,  on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	verification_token = models.CharField(max_length=32, null=True, blank= True)
	email = models.CharField(max_length=200)
	profile_pic = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	# @property
	# def imageURL(self):
	# 	try:
	# 		url = self.image.url
	# 	except:
	# 		url = ''
	# 	return url


	

class Category(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=200, null=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	description = RichTextField()
	# BooleanField because :
	# we want to know if the item is digital, we don't need to ship it if it's true
	# if it's a [(flase)physical product-by default] then we need to ship it.
	digital = models.BooleanField(default=False,null=True, blank=True)
	# pip install pillow to user ImageField
	image = models.ImageField(null=True, blank=True)
	# run migrations after adding this field

	def __str__(self):
		return self.name

# if we don't add an image for all the products, we will receive an error
# to avioid this error, we will create a function:
	'''
	A decorator function is basically a function that adds new functionality
	to a function that is passed as argument.
	In Python, the @property decorator allows you to call custom model methods
	as if they were normal model attributes.
	adding the @property decorator to that method would allow you to access
	its computed value like a model attribute without parenthesis
	The @property decorator is a built-in decorator in Python for the property()
	function. This function returns a special descriptor object which allows direct
	access to getter, setter, and deleter methods.
	'''
	@property # it's going to let us access this as an attribute rather than a method
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url



class Order(models.Model): # CART
	# we give it a relation to our customer, many to one relationship
	# which means that the customer can have many orders
	customer = models.ForeignKey(
		Customer, 
		# .SET_NULL
		# if a customer gets deleted, we don't want to delete the order
		# we want to just set the customer value to null
		on_delete=models.SET_NULL, 
		null=True, blank=True
		)
	date_ordered = models.DateTimeField(auto_now_add=True)
	# if complete is false, that is a open cart, 
	# we can continue adding items to that cart
	complete = models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
		# if we don't do anything, shipping is always going to be false
		shipping = False
		# query all the order items
		orderitems = self.orderitem_set.all()
		# loop through all of the order items and check if
		# any of those items have the value of digital set to false
		for i in orderitems:
			if i.product.digital == False:
				# changing the value
				shipping = True
			return  shipping

# error needs fix

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		print(orderitems)
		total = sum([item.quantity for item in orderitems])
		return total



class OrderItem(models.Model):
	# many to one relationship
	# order is our cart, orderItem is our item within our cart
	# cart can have multiple order items 
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)


# error needs fix

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total



class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address