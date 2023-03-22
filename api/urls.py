from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

# url for api
urlpatterns = [
    # path('listproductapi/',views.product_list),

    # Product List:
    path('listproductapi/',views.ListProductView.as_view()),

    # path('product_description/',views.DescribeProductView.as_view()),

    # Product Add:
    path('product_add/', views.CreateProductView.as_view()),

    # Product Get, Update and Delete:
    path('productapi/<int:id>', views.ProductRetrieveUpdateAndDeleteView.as_view()),

    # Product search by category:
    path('category/<str:category_name>/', views.ListProductByCategoryView.as_view(), name='product_list_by_category'),

    # Product search functionality:
    # http://localhost:8000/api/products/?q=search_query&category=category_id
    # search_query is the product we want, eg., (bmw)     http://127.0.0.1:8000/api/products/?q=bmw
    # category is the category id, eg., (3)       http://127.0.0.1:8000/api/products/?category=3
    path('api/products/', views.ProductSearchView.as_view(), name='product-list-api'),

    path('api/user/register/', views.UserRegistrationAPIView.as_view(), name='user_registration_api'),

    path('api/login/', views.LoginAPIView.as_view()),

    # path('logout/', views.LogoutAPIView.as_view()),

    path('users/', views.CreateUserView.as_view(), name='create_user'),

]

urlpatterns = format_suffix_patterns(urlpatterns)