from django.urls import path

from apiJWT.views import *

app_name='apiJWT'


urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    # path('apiJWT/user', UserAPIView.as_view(), name='user'),

]
