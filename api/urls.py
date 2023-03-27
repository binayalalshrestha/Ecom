from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

# url for api
urlpatterns = [
    # PRODUCT LIST
    path('list_product_api/',views.ListProductView.as_view()),

    # PRODUCT ADD
    path('add_product_api/', views.CreateProductView.as_view()),

    # PRODUCT GET UPDATE AND DELETE
    path('product_RUD_api/<int:id>/', views.ProductRetrieveUpdateAndDeleteView.as_view()),

    # PRODUCT SEARCH BY CATEGORY
    path('search_api/<str:category_name>/', views.ListProductByCategoryView.as_view(), name='product_list_by_category'),

    # PRODUCT SEARCH FUNCTIONALITY
    path('api_search/products/', views.ProductSearchView.as_view(), name='product-list-api'),
    # http://localhost:8000/api/products/?q=search_query&category=category_id
    # search_query is the product we want, eg., (bmw)     http://127.0.0.1:8000/api_search/products/?q=test
    # category is the category id, eg., (3)     http://127.0.0.1:8000/api_search/products/?category=3

    # REGISTER
    path('api/user/register/', views.UserRegistrationAPIView.as_view(), name='user_registration_api'),

    # LOGIN
    path('api/login/', views.LoginAPIView.as_view()),

    # LOGOUT
    path('api/logout/', views.LogoutAPIView.as_view()),

    # CREATE USER
    path('api/create_users/', views.CreateUserView.as_view(), name='create_user'),

    # CUSTOMER LIST
    path('api/list_customers/', views.CustomerListView.as_view()),

    # DEACTIVATE USER
    path('deactivate/<int:pk>/', views.UserActivationView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)