from django.urls import path
from . import views
# from store.views import registerPage, verify_email

app_name='store'


urlpatterns = [
    path('', views.store, name="store"),

    # to make staff

    path('make-staff/', views.make_users_staff, name='make-staff'),

    # for email verification

    # path('verify-email/<int:user_id>/<str:token>/', views.verify_email, name='verify_email'),


# for admin dashboard

    # path('adminDashboard2/', views.AboutView.as_view(), name="adminDashboard2"),

    path('adminDashboard2/', views.adminDashboard, name="adminDashboard2"),


    path('adminPage/', views.adminPage, name="adminPage"),


# for user
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    # path('verify_email/<int:user_id>/<str:token>/', verify_email, name='verify_email'),

    path('profile<int:pk>/', views.userProfile, name="user-profile"),
    path('update-user/<int:pk>/', views.updateUser, name="update-user"),
    path('deleteUser/<str:pk>/', views.deleteUser, name="deleteUser"),



    path('product/<int:pk>', views.ProductPage.as_view(), name="productPage"),  #.as_view() 

# CRUD for product

    path('createProduct/', views.createProduct, name="createProduct"),
    path('updateProduct/<str:pk>/', views.updateProduct,name="updateProduct"),
    path('deleteProduct/<str:pk>/', views.deleteProduct, name="deleteProduct"),

# Cart and Checkout views

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
    
    path('process_order/', views.processOrder, name="process_order"),
]
 