from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

# url for api
urlpatterns = [
    # path('listproductapi/',views.product_list),

    path('listproductapi/',views.ProductList.as_view()),

    path('product_description/',views.ProductDescription.as_view()),

    path('product_add/', views.CreateProduct.as_view()),

    path('productapi/<int:id>', views.ProductGetPutDel.as_view()),

    path('category/<str:category_name>/', views.ProductListByCategory.as_view(), name='product_list_by_category'),

    # http://localhost:8000/api/products/?q=search_query&category=category_id
    # search_query is the product we want, eg., (bmw)     http://127.0.0.1:8000/api/products/?q=bmw
    # category is the category id, eg., (3)       http://127.0.0.1:8000/api/products/?category=3
    path('api/products/', views.SearchProduct.as_view(), name='product-list-api'),

    path('api/user/register/', views.UserRegistrationAPIView.as_view(), name='user_registration_api'),

    path('api/login/', views.LoginAPIView.as_view()),

    # path('logout/', views.LogoutAPIView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)