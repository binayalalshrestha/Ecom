from django.urls import path, include

from .views import RandomObjectListView,RandomObjectDetailView,RandomObjectCreateView,RandomObjectUpdateView,RandomObjectDeleteView

app_name='randomObject'


urlpatterns = [

    path('store/', include('store.urls')),

    path('randomObject/list/', RandomObjectListView.as_view(), name='randomObject-list'),

    path('randomObject/detail/<int:pk>/', RandomObjectDetailView.as_view(), name='randomObject-detail'),

    path('randomObject/create/', RandomObjectCreateView.as_view(), name='randomObject-create'),

    path('randomObject/update/<int:pk>/', RandomObjectUpdateView.as_view(), name='randomObject-update'),

    path('randomObject/delete/<int:pk>/', RandomObjectDeleteView.as_view(), name='randomObject-delete'),

]
