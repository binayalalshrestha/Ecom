'''
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('apiJWT/register/', RegisterView.as_view(), name='register'),
    path('apiJWT/login/', LoginView.as_view(), name='login'),
    path('apiJWT/logout/', LogoutView.as_view(), name='logout'),

    path('apiJWT/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('apiJWT/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
'''

from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Register SingerViewSet and SongViewSet with Router

# router.register('singer', views.SingerViewSet, basename='singer')
# router.register('Song', views.SongViewSet, basename='song')

router.register('League', views.LeagueViewSet, basename='league')
router.register('Team', views.TeamViewSet, basename='team')
router.register('Player', views.PlayerViewSet, basename='player')
router.register('Student',views.StudentViewSet, basename='student')



# url for api
urlpatterns = [

    path('store/', include('store.urls')),

    # to learn serializer relation
    path('myRouter/', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]