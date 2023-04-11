from rest_framework import serializers
from . models import Player

# Player Serializer
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'first_name',
            'last_name',
            'age',
            'height',
            'weight'
            ]

# Basketball player serializer
class BasketballPlayerSerializer(PlayerSerializer):
    class Meta(PlayerSerializer.Meta):
        fields = PlayerSerializer.Meta.fields + [
            'position',
            'rating'
            ]

class NBAPlayerSerializer(BasketballPlayerSerializer):
    class Meta(BasketballPlayerSerializer.Meta):
        fields = BasketballPlayerSerializer.Meta.fields + [
            'team',
            'manager'
            ]
