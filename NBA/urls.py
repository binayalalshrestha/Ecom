from django.urls import path
from .views import (
    PlayerList,
    PlayerDetail,
    BasketballPlayerList,
    BasketballPlayerDetail,
    NBAPlayerList,
    NBAPlayerDetail,
)

urlpatterns = [
    path('players/', PlayerList.as_view(), name='player-list'),
    path('players/<int:pk>/', PlayerDetail.as_view(), name='player-detail'),
    path('basketball-players/', BasketballPlayerList.as_view(), name='basketballplayer-list'),
    path('basketball-players/<int:pk>/', BasketballPlayerDetail.as_view(), name='basketballplayer-detail'),
    path('nba-players/', NBAPlayerList.as_view(), name='nbaplayer-list'),
    path('nba-players/<int:pk>/', NBAPlayerDetail.as_view(), name='nbaplayer-detail'),
]
