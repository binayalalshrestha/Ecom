import json
import datetime

from .models import * # * will import all the database models
# from .utils import cookieCart, cartData, guestOrder
from randomObject.models import RandomObject

# for search
from django.db.models import Q

# for class based views
from django.views import View

from django.shortcuts import render, redirect

# for login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

#for message
from django.contrib import messages

# from django.conf import settings
# User = settings.AUTH_USER_MODEL

# for email

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from django.core.mail import send_mail
from django.urls import reverse

#for userCreationForm
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import TemplateView

from .forms import  UserForm, ProductForm

from django.http import JsonResponse

from .utils import has_customer, send_email

from django.contrib.auth import get_user_model


# setting a user as a staff 

# This line gets the user model from Django's authentication system.
# It assigns it to a variable called User so it can be used later in the code.
User = get_user_model()

# This defines a view function called make_users_staff that takes a request object as an argument.
# The view will handle a POST request that is sent when the user submits a form.
def make_users_staff(request):
	# This checks if the HTTP method used in the request is POST.
	# In this case, it's looking for a form submission.
	if request.method == 'POST':
		# This gets a list of user IDs from the POST data.
		# It's looking for form fields with the name "users" and getting their values.
		# Get the users you want to make staff from the form data
		user_ids = request.POST.getlist('users')
		# This uses the Django ORM to get a queryset of User objects whose IDs match the IDs in user_ids.
		users_to_make_staff = User.objects.filter(id__in=user_ids)

		# Loop through the users and make them staff
		# This loops through the queryset of users and sets their is_staff attribute to True,
		# then saves the changes to the database.
		for user in users_to_make_staff:
			user.is_staff = True
			user.save()
		# This sets a boolean variable success to True.
		# This is used later to determine if the action was successful.	
		success = True
	# If the HTTP method was not POST,
	# it sets success to False and sets users_to_make_staff to an empty queryset.
	else:
		success = False
		users_to_make_staff = User.objects.none()
	# This gets a queryset of all User objects in the database.
	users = User.objects.all()
	# This creates a dictionary called context that contains the
	# users, users_to_make_staff, and success variables.
	# This will be used to pass data to the template.
	context = {
        'users': users,
        'users_to_make_staff': users_to_make_staff,
        'success': success
    }
	return render(request, 'store/make_staff.html', context)

'''
User = get_user_model()

def make_users_staff(request):
    if request.method == 'POST':
        # Get the users you want to make staff from the form data
        user_ids = request.POST.getlist('users')
        users_to_make_staff = User.objects.filter(id__in=user_ids)

        # Loop through the users and make them staff
        for user in users_to_make_staff:
            user.is_staff = True
            user.save()

        return render(request, 'store/make_staff.html', {'success': True})

    users = User.objects.all()
    return render(request, 'store/make_staff.html', {'users': users})
'''



#Admin Dashboard
# class AboutView(TemplateView):
# 	template_name = "store/adminDashboard2.html"

def adminDashboard(request):

	products = Product.objects.all()
	customers = Customer.objects.all()
	randomObjects = RandomObject.objects.all()

	context={
		'products':products,
		'customers':customers,
		'randomObjects':randomObjects,

	}
	return render(request, 'store/adminDashboard2.html', context)


def adminPage(request):
	context={

	}
	return render(request, 'store/adminPage', context)


# views for LOGIN

def loginPage(request):
	page = 'login'
	if request.user.is_authenticated:
		return redirect('store:store')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		try:
			user = User.objects.get(username=username)
		except:
			messages.error(request, 'User does not exist')
		user = authenticate(request, username=username, password=password)
	
		if user is not None:
			login(request, user)
			if user.is_superuser:
				return redirect('store:adminDashboard2')
			return redirect('store:store')
		else:
			messages.error(request, 'Username OR password does not exist')
	context={
		'page':page,
	# 'username':username,
	# 'password':password,
  }
	return render(request, 'store/login_register.html', context)




# views for LOGOUT


@login_required(login_url='login')

def logoutUser(request):
	logout(request)
	return redirect('store:store')



# views for REGISTER

# def registerPage(request):
#     page='register'
#     form = UserCreationForm()
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()

#             user.is_active = False

#             user.save()
#             # customer=Customer(user=user)
			

#             # customer.save()

#             token = get_random_string(length=32)
#             profile = Customer.objects.create(user=user, verification_token=token)

#             verification_url = request.build_absolute_uri(
#             reverse('verify_email', kwargs={'user_id': user.id, 'token': token})
#             )
	
#             send_mail(
#                 'Verify your email',
#                 f'Thank you for registering in the AOIS ( All in one store ). Please click the following link to verify your email: {verification_url}. After your email has been verified, enjoy shopping!!',
#                 'noreply@infodev.com.np',
#                 [user.username],
#                 fail_silently=False,
#             )
			
#             # send_email(user)

#             return redirect('login')
#         else:
#             messages.error(request, 'An error occurred during registration')
#     return render(request, 'store/login_register.html', {'form':form, 'page':page})


def registerPage(request):
	
	page='register'
	form = UserCreationForm()
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():

			user = form.save(commit=False)
			user.username = user.username.lower()

			# user.is_active = False

			user.save()
			c=Customer(user=user)	#
			c.save()	#

			# email verification :


			# token = get_random_string(length=32)

			# profile = Customer.objects.create(user=user, verification_token=token)
			
			# print(profile)

			# verification_url = request.build_absolute_uri(
			# reverse('store:verify_email', kwargs={'user_id': user.id, 'token': token})
			# )
			# send_mail(
			#     'Verify your email',
			#     f'Thank you for registering in the AOIS ( All in one store ). Please click the following link to verify your email: {verification_url}. After your email has been verified, enjoy shopping!!',
			#     'noreply@infodev.com.np',
			#     [user.username],
			#     fail_silently=False,
			# )


			# end of email verification !
			
			send_email(user)
			messages.success(request, 'Your account has been created. Please check your email to verify your account.')
			return redirect('store:login')
		else:
			print(form.errors)
			messages.error(request, 'An error occurred during registration')
	else:
		form = UserCreationForm()  # re-instantiate form if request method is not POST
	return render(request, 'store/login_register.html', {'form':form, 'page':page})



# VERIFY EMAIL

# def verify_email(request, user_id, token):
#     user = User.objects.get(id=user_id)
#     profile = Customer.objects.get(user=user, verification_token=token)
	
#     if profile is not None:
#         user.is_active = True
#         user.save()
#         profile.delete()
		
#         # Log the user in
#         user = authenticate(username=user.username, password=user.password)
#         login(request, user)
		
#         return redirect('login')
#     else:
#         # Handle invalid or expired tokens
#         pass



# views for USERPROFILE

def userProfile(request, pk):
	orderDetail = Order.objects.filter(customer=request.user.customer)
	orderdetails = OrderItem.objects.filter(order__in=orderDetail)
	# product = Product.objects.get(id=pk)
	# order = Order.objects.all()
	# orderItem = OrderItem.objects.all()
	if request.user.is_authenticated:
		try:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			
			cartItems = order.get_cart_items
		except:
			cartItems = order['get_cart_items']
	else:
		cartItems = order['get_cart_items']

	context = {
		
		'orderDetails': orderdetails,
		'cartItems':cartItems,	
		
		# 'product': product,
		# 'order': order,
		# 'orderItem':orderItem,
	}
	return render(request, 'store/profile.html', context)



# views for UPDATE USER

@login_required(login_url='login')

def updateUser(request, pk):
	user = Customer.objects.get(id=pk) #request.user.customer
	form = UserForm(instance=user)
	if request.method == 'POST':
		form = UserForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			return redirect('store:user-profile', pk=user.id)
	if request.user.is_authenticated:
		try:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			
			cartItems = order.get_cart_items
		except:
			cartItems = order['get_cart_items']
	else:
		cartItems = order['get_cart_items']
	
	context = {
		'form':form,
		'cartItems':cartItems
	}
	return render(request, 'store/update-user.html', context)

# from django.views.generic import UpdateView
# from django.urls import reverse_lazy
# from .models import Customer
# from .forms import UserForm
'''
class UserUpdateView(UpdateView):
	model = Customer
	form_class = UserForm
	template_name = 'store/update-user.html'

	def get_success_url(self):
		return reverse_lazy('user-profile', kwargs={'pk': self.object.id})
'''

@login_required(login_url='login')

def deleteUser(request, pk):
	user = Customer.objects.get(id=pk)
	if request.method == 'POST':
		user.delete()
		logout(request)
		return redirect('store:register')
	return render(request, 'store/delete.html',{'obj':request.user})
	


# views for STORE PAGE

def store(request):
	category = Category.objects.all()
	products = Product.objects.all()
	q = request.GET.get('q')
	categoryFilter = request.GET.get('category')
	if categoryFilter:
		products=products.filter(category=categoryFilter)
	if q:
		products = products.filter(name__icontains=q)
	if request.user.is_authenticated:
		try:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			items = order.orderitem_set.all()
			
			cartItems = order.get_cart_items
		except:
			items = []
			order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
			cartItems = order['get_cart_items']
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	
	
	context = {
		'products':products,
		'category':category,
		'cartItems':cartItems,
		# 'productSearch':productSearch,
		
		}
	return render(request, 'store/store.html', context)


# views for PRODUCT PAGE

# def productPage(request, pk):
#     product = Product.objects.get(id=pk)
#     context = {
#         'product':product
#     }
#     return render(request, 'store/product.html',context)

class ProductPage(View):
	def get(self, request,pk):
		product = Product.objects.get(id=pk)
		context = {
			'product':product
		}
		return render(request, 'store/product.html',context)



# views for CREATE PRODUCT
def createProduct(request):
	form = ProductForm()
	if request.method == "POST":
		form=ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('store:store')
	context={
		'form':form
	}
	return render(request, 'store/product_form.html', context)



# views for UPDATE PRODUCT

def updateProduct(request, pk):
	product = Product.objects.get(id=pk)
	form = ProductForm(instance=product)
	if request.method == 'POST':
		form=ProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			return redirect('store:store')
	context={
		'form':form
	}
	return render(request, 'store/product_form.html', context)



# views for DELETE PRODUCT

def deleteProduct(request, pk):
	product= Product.objects.get(id=pk)
	if request.method == 'POST' and request.user.is_superuser:
		product.delete()
		return redirect('store:store')
	return render(request, 'store/delete.html',{'obj':product})


# views for CART

@login_required(login_url='login')

def cart(request):
	user=request.user
	if user.is_authenticated:
		customer= has_customer(user)

		if customer:
			order= Order.objects.filter(customer=customer, complete=False).first()
			items = order.orderitem_set.all()
			cartItems = order.get_cart_items
		else:

			items = []
			order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
			cartItems = order['get_cart_items']
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart={}
		print('Cart:', cart)
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
		for i in cart:
			cartItems += cart[i]["quantity"]
	context = {
		'items':items,
		'order':order,
		'cartItems':cartItems,
	}
	return render(request, 'store/cart.html', context)



# views for CHECKOUT

'''
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
'''

@login_required(login_url='login')

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {
		'items':items,
		'order':order,
		'cartItems':cartItems,
	}
	print(order)
	return render(request, 'store/checkout.html', context)




# views for UPDATE ITEM

def updateItem(request):

	
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	
	print('Action:', action)
	print('Product:', productId)
	customer = request.user.customer

	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)



# views for PROCESS ORDER

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == float(order.get_cart_total):
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)

	else:
		print('User is not logged in..')
	return JsonResponse('Payment submitted..', safe=False)


# # for class based views
# from django.views import View

# from django.shortcuts import render, redirect
# # for search
# from django.db.models import Q
# # for login
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.forms import UserCreationForm
# from django.views.generic import TemplateView

# from .forms import  ProductForm, SignupForm

# from django.http import JsonResponse
# import json
# from .utils import has_customer

# import datetime

# from .models import * # * will import all the database models
# # from .utils import cookieCart, cartData, guestOrder



# #Admin Dashboard


# class AboutView(TemplateView):
#     template_name = "store/index.html"


# # views for LOGIN

# def signup(request):  
#     if request.method == 'POST':  
#         form = SignupForm(request.POST)  
#         if form.is_valid():  
#             # save form in the memory not in database  
#             user = form.save(commit=False)  
#             user.is_active = False  
#             user.save()  
#             # to get the domain of the current site  
#             current_site = get_current_site(request)  
#             mail_subject = 'Activation link has been sent to your email id' 
#             message = render_to_string('acc_active_email.html', {  
#                 'user': user,  
#                 'domain': current_site.domain,  
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
#                 'token':account_activation_token.make_token(user),  
#             })  
#             to_email = form.cleaned_data.get('email')  
#             email = EmailMessage(  
#                         mail_subject, message, to=[to_email]  
#             )  
#             email.send()  
#             return HttpResponse('Please confirm your email address to complete the registration') 
#     else:  
#         form = SignupForm()  
#     return render(request, 'signup.html', {'form': form})   

# def loginPage(request):
#     page = 'login'
#     if request.user.is_authenticated:
#         return redirect('store')
#       # first we are going to check the method
#     if request.method == 'POST': # the user entered their information and logged in here
#     # get the username
#         username = request.POST.get('username')
#     # get the password
#         password = request.POST.get('password')
#     # making sure the user exists
#         try:
#             user = User.objects.get(username=username) # import the user model to use
#         except:
#       # using flash messages
#             messages.error(request, 'User does not exist')
#     # now, if the user does exist we are gonna go ahead and continue here
#     # we'll use the authenticate method which needs to be imported
#     # once we make sure that we have a user, we will authenticate this user
#     # that means that whatever the credentials this user has, it is correct
#         user = authenticate(request, username=username, password=password)
#     # So what authenticate is going to do is it's either gonna give us an error
#     # or return back a user object that matches these credentials
	
#         if user is not None: # this means that we got a user, then login the user
#       # to login, we will be using the login method
#       # this creates a session in the browser and the database
#             login(request, user) # pass in the request object and the user
#       # then we redirect the user to the homepage after they are logged in
#             return redirect('store')
#       # if the user does not exist then
#         else:
#             messages.error(request, 'Username OR password does not exist')
	


#     context={
#         'page':page,
#     # 'username':username,
#     # 'password':password,
#   }
#     return render(request, 'store/login_register.html', context)



# # views for LOGOUT


# @login_required(login_url='login')

# def logoutUser(request):
#     logout(request)
#     return redirect('store')



# # views for REGISTER

# def registerPage(request):
#     page='register'
#     form = UserCreationForm()

#     # method check garney POST ho vaney chai
#     if request.method == 'POST':
#         # UserCreationForm vaney form cha django ma vayeko
#         # tesma chai username , password huncha
#         form = UserCreationForm(request.POST)   # form fill garney
#         if form.is_valid():     # form valid cha vaney

#             print("=========")
#             user = form.save(commit=False)      # paila user save huncha, tara commit=Flase le chai save hudaina

#             user.username = user.username.lower()       # paila aba change garney, .lower() function use garera

#             user.save()     # ani balla save garney

#             customer=Customer(user=user)        # aba customer lai user nai assign garney, vaneko user is the customer

#             customer.save()     # customer lai save garney, customer ko database ma user save
#             '''
#             The request argument is an instance of the HttpRequest object that represents the current user request to the server.
#             The user argument is an instance of the User object, which represents the authenticated user.
#             The login function performs two main tasks:

#             1. It sets a session cookie on the user's browser to keep them logged in, using Django's built-in session framework.
#             2. It updates the request object to associate the current user with the request, so that the server can recognize them as an authenticated user for future requests.
		
#             '''
#             '''
#                                 Instance
#             In object-oriented programming (OOP), an instance is a specific occurrence of a class, which is a blueprint or template for creating objects.

#             To create an object in OOP, you typically define a class with attributes (data) and methods (functions) that operate on that data.
#             An instance of the class is created by calling the class constructor, which returns a new object with its own set of attributes and methods.

#             For example, let's say you have a class called Person that has attributes for a person's name, age, and gender, as well as methods for setting and getting those attributes.
#             You can create an instance of this class like so:

#             class Person:
#                 def __init__(self, name, age, gender):
#                     self.name = name
#                     self.age = age
#                     self.gender = gender

#             person1 = Person("Alice", 30, "female")

#             In this example, person1 is an instance of the Person class. 
#             It has its own set of attributes (name, age, and gender) that are specific to this instance, 
#             and it can call the class's methods to modify or access those attributes.

#             You can create multiple instances of the same class, each with its own unique set of attributes and methods. 
#             This allows you to create multiple objects that share the same behavior but have different data.

#             '''
#             login(request, user)        # login request garney

#             return redirect('store')
#         else:
#             print("-----------",form.errors)

#             messages.error(request, 'An error occurred during registration')
	
			

#     return render(request, 'store/login_register.html', {'form':form, 'page':page})



# # views for USERPROFILE

# def userProfile(request, pk):
#     user = User.objects.get(id=pk)
#     # product = Product.objects.get(id=pk)
#     # order = Order.objects.all()
#     # orderItem = OrderItem.objects.all()

#     context = {
#         'user': user,
#         # 'product': product,
#         # 'order': order,
#         # 'orderItem':orderItem,
#     }
#     return render(request, 'store/profile.html', context)



# # views for UPDATE USER

# @login_required(login_url='login')

# def updateUser(request):
#     # This line retrieves the currently logged in user from the request object.
#     user = request.user
#     # This line creates a new UserForm object with the current user's information filled in as the initial data.
#     # This form is used to display the user's current information and allow them to update it.
#     form = UserForm(instance=user)
	
#     # The function checks whether the request method is POST.
#     # If it is, this means that the user has submitted the form, and the function processes the form data.
#     if request.method == 'POST':
#         # This line creates a new UserForm object with the updated form data from the POST request and the current user's instance.
#         # This allows the form to be updated with the new user data.
#         form = UserForm(request.POST, instance=user)
#         # This line checks if the form data is valid. If it is, the updated data is saved to the database using the form.save() method.
#         if form.is_valid():
#             form.save()
#             # This line redirects the user to their profile page after the update is complete.
#             return redirect('user-profile', pk=user.id)
#     # If the request method is not POST, the function returns a rendered template with the UserForm object as context.
#     # This displays the form with the user's current information and allows them to update it.
#     return render(request, 'store/update-user.html', {'form':form})
	


# # views for STORE PAGE

# def store(request):
	

#     # productSearch = Product.objects.filter(
#     #     Q(name__icontains=q)
#     # )
#     '''
#     Search
#     '''
#     # This line retrieves all instances of the Product model from the database and assigns them to the products variable.
#     category = Category.objects.all()
#     print("=====category======",category)
#     products = Product.objects.all()
#     '''
#     This line retrieves the search query string from the GET request's parameters.
#     If the GET request contains a parameter called q,
#     the value of that parameter is assigned to the q variable.
#     '''
#     q = request.GET.get('q')            #if request.GET.get('q') != None else ''
#     cat = request.GET.get('category')            #if request.GET.get('q') != None else ''
#     if cat:
#         products=products.filter(category=cat)
#     '''
#     This line checks if the q variable contains a value.
#     If it does, this means that the user has entered a search query,
#     and the product list should be filtered based on that query.
#     '''
#     if q:
#         '''
#         This line filters the products queryset by the search query.
#         The filter() method takes a set of keyword arguments that define the filtering conditions.
#         In this case, we are filtering the queryset by the name attribute,
#         using the __icontains lookup to match products with names that contain the search query,
#         regardless of case.
#         '''
#         # category = category.filter(name__icontains=q)
#         products = products.filter(name__icontains=q)

#     # check if user is authenticated
#     if request.user.is_authenticated:
#         # set the customer value
#         try:
#             customer = request.user.customer
#             # order, created - because we want to either create an order or get an order if it exists 
#             # get_or_create - creating an object or quering one
#             order, created = Order.objects.get_or_create(customer=customer, complete=False)
#             # get the items attached to that order
#             items = order.orderitem_set.all()
#             # create a variable called cartItems, pass in cartItems in every single template
			
#             cartItems = order.get_cart_items
#         except:
#             items = []
#             order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
#             # for cart item totals
#             cartItems = order['get_cart_items']
#             # if the user is not authenticated
#     else:
#         items = []
#         order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
#         # for cart item totals
#         cartItems = order['get_cart_items']
	
	
#     context = {
#         'products':products,
#         'category':category,
#         'cartItems':cartItems,
#         # 'productSearch':productSearch,
		
#         }
#     return render(request, 'store/store.html', context)


# # views for PRODUCT PAGE

# # def productPage(request, pk):
# #     product = Product.objects.get(id=pk)
# #     context = {
# #         'product':product
# #     }
# #     return render(request, 'store/product.html',context)

# class ProductPage(View):
#     def get(self, request,pk):
#         product = Product.objects.get(id=pk)
#         context = {
#             'product':product
#         }
#         return render(request, 'store/product.html',context)



# # views for CREATE PRODUCT
# def createProduct(request):
#     form = ProductForm()
#     if request.method == "POST":
#         form=ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('store')
#     context={
#         'form':form
#     }
#     return render(request, 'store/product_form.html', context)



# # views for UPDATE PRODUCT

# def updateProduct(request, pk):
#     province = Product.objects.get(id=pk)
#     form = ProductForm(instance=province)
#     if request.method == 'POST':
#         form=ProductForm(request.POST, instance=province)
#         if form.is_valid():
#             form.save()
#             return redirect('store')
#     context={
#         'form':form
#     }
#     return render(request, 'store/product_form.html', context)



# # views for DELETE PRODUCT

# def deleteProduct(request, pk):
#     province= Product.objects.get(id=pk)
#     if request.method == 'POST':
#         province.delete()
#         return redirect('srksapp:provincePage')
#     return render(request, 'store/delete.html',{'obj':province})


# # views for CART

# @login_required(login_url='login')

# def cart(request):
#     # check if user is authenticated
#     user=request.user
#     if user.is_authenticated:
#         # If the user is authenticated,
#         # the code retrieves the customer object associated
#         # with the user using the has_customer function

#         customer= has_customer(user)

#         # set the customer value
#         if customer:

#             # customer = request.user.customer
#         # order, created - because we want to either create an order or get an order if it exists 
#         # get_or_create - creating an object or quering one
#             order= Order.objects.filter(customer=customer, complete=False).first()
#             items = order.orderitem_set.all()
#             cartItems = order.get_cart_items
#         else:

#             items = []
#             order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
#             cartItems = order['get_cart_items']

#     #for a not logged in user


#     else:
#         '''
#         When we first log into our page we don't have the cart value
#         and if we remove cart cookie from our browser we will receive an error
#         to fix it
#         we need to say try:
#                             ....
#                         except:
#                             ....
#                             we will create a dummy value until it is set
#                             this gets set in main.html
#                             -   cart = { }
#                             so if we don't have that cookie
#                             we will create an object here and it's going to be empty
#         '''
#         try:
#             '''
#             first we will get our cookies with - request.COOKIES and then 
#             getting the cookie name - ['cart']
#             we will then set this to the variable of (cart)
#             - cart = request.COOKIES['cart']
#             Once we have that, we need to remember that our cookies is a string
#             so we need to parse it in order to get value in a python dictionary
#             so we will do - json.loads()
#             -
#             '''
#             cart = json.loads(request.COOKIES['cart'])
#         except:
#             cart={}
#         print('Cart:', cart)
#         items = []
#         order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
#         cartItems = order['get_cart_items']

#         # for cart icon updating in the page
#         '''
#         we will loop through this cart right now
#         and update cart items
#         we can loop through the python dictionary just like we would a list
#         except for on each iteration we're going to get the key
#         and in this case the key is going to be the product id
#         so we will access it this way - cart[i]
#         and get the quantity
#         and then we will...
#         update cart items in each iteration'''
#         for i in cart:
#             cartItems += cart[i]["quantity"]

#         '''
#         Now we will continue this loop
#         and then we will query the products
#         setting the totals and updating the values in our [ order ] above
#         '''

#     context = {
#         'items':items,
#         'order':order,
#         'cartItems':cartItems,
#     }
#     return render(request, 'store/cart.html', context)



# # views for CHECKOUT

# '''
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# '''

# @login_required(login_url='login')

# def checkout(request):
#     '''
#     This line checks if the user is authenticated.
#     If they are, this means that they are logged in,
#     and we can proceed with the checkout process.
#     '''
#     if request.user.is_authenticated:
#         '''
#         This line retrieves the Customer instance associated with the currently logged in user.
#         '''
#         customer = request.user.customer
#         '''
#         This line retrieves an existing order for the current user,
#         or creates a new order if one does not already exist. 
#         The get_or_create() method returns a tuple containing the order instance
#         and a boolean value indicating whether the order was created or retrieved from the database.
#         '''
#         '''
#         the get_or_create method :
#         The get_or_create() method is a convenient method provided by Django's QuerySet API
#         that can be used to retrieve an object from the database, or create a new one if it doesn't exist.

#         The method takes a set of keyword arguments that define the lookup criteria for the object.
#         If an object exists in the database that matches the lookup criteria,
#         the method returns a tuple containing the object and a boolean value of False,
#         indicating that the object was retrieved from the database.

#         If an object does not exist in the database that matches the lookup criteria,
#         the method creates a new object using the same keyword arguments,
#         and returns a tuple containing the new object and a boolean value of True,
#         indicating that the object was created.
#         '''
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         '''
#         This line retrieves all OrderItem instances associated with the current order.
#         '''
#         items = order.orderitem_set.all()
#         '''
#         This line retrieves the number of items in the cart using the get_cart_items method of the Order instance.
#         '''
#         cartItems = order.get_cart_items

#             # Else :
#                 # If the user is not authenticated,
#                 # the function sets the items variable to an empty list
#                 # and creates a dummy order dictionary with some default values.
#     else:
#         items = []
#         order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
#         cartItems = order['get_cart_items']

#     context = {
#         'items':items,
#         'order':order,
#         'cartItems':cartItems,
#     }
#     print(order)
#     return render(request, 'store/checkout.html', context)



# # views for UPDATE ITEM

# def updateItem(request):


#     # set the value of data to that response
# 	data = json.loads(request.body) #parsing data

#     #getting data of productId and action
# 	productId = data['productId']
# 	action = data['action']
	
# 	print('Action:', action)
# 	print('Product:', productId)

#     # get the logged in customer
# 	customer = request.user.customer
#     # get the product
# 	product = Product.objects.get(id=productId)
#     # get or create the order
# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)
#     # get or create the orderItem
# 	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

# 	if action == 'add':
# 		orderItem.quantity = (orderItem.quantity + 1)
# 	elif action == 'remove':
# 		orderItem.quantity = (orderItem.quantity - 1)

# 	orderItem.save()

# 	if orderItem.quantity <= 0:
# 		orderItem.delete()

# 	return JsonResponse('Item was added', safe=False)



# # views for PROCESS ORDER

# def processOrder(request):
#     transaction_id = datetime.datetime.now().timestamp()
#     data = json.loads(request.body)

#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         total = float(data['form']['total'])
#         order.transaction_id = transaction_id

#         if total == float(order.get_cart_total):
#             order.complete = True
#         order.save()

#         if order.shipping == True:
#             ShippingAddress.objects.create(
#                 customer=customer,
#                 order=order,
#                 address=data['shipping']['address'],
#                 city=data['shipping']['city'],
#                 state=data['shipping']['state'],
#                 zipcode=data['shipping']['zipcode'],
#             )

#     else:
#         print('User is not logged in..')
#     return JsonResponse('Payment submitted..', safe=False)
