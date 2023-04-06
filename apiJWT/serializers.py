from . models import (
    # Singer,
    # Song,
    League,
    Team,
    Player,
    Student
)
from rest_framework import serializers

# class SingerSerializer(serializers.ModelSerializer):
#     song = serializers.StringRelatedField(many=True, read_only=True)
#     # song = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     # song = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='song-detail')
#     # song = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
#     # song = serializers.HyperlinkedIdentityField(view_name='song-detail')

#     class Meta:
#         model = Singer
#         fields = ['id', 'name', 'gender', 'song']

# class SongSerializer(serializers.ModelSerializer):
#     singer = SingerSerializer()
#     class Meta:
#         model = Song
#         fields = ['id', 'title','duration','singer']


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['name']


class TeamSerializer(serializers.ModelSerializer):
    league = LeagueSerializer()
    class Meta:
        model = Team
        fields = [
            'name',
            'league'
            ]



class PlayerSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    class Meta:
        model = Player
        fields = [
            'name',
            'team',
            'kitNumber'
            ]




class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'name',
            'roll',
            'city'
            ]


'''
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
'''


# from rest_framework import serializers
# from django.contrib.auth.models import User

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')

#     def create(self, validate_data):
#         user = User.objects.create(
#             username=validate_data['username'],
#             email=validated_data['email']
#         )
#         user.set_password(validated_data['password'])
#         user.save()

#         return user