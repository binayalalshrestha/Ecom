from rest_framework import generics
from .models import Player
from .serializers import PlayerSerializer, BasketballPlayerSerializer, NBAPlayerSerializer

class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class BasketballPlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = BasketballPlayerSerializer

class BasketballPlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = BasketballPlayerSerializer

class NBAPlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = NBAPlayerSerializer

class NBAPlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = NBAPlayerSerializer
