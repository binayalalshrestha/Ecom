from django.contrib import admin
from .models import (
    Singer, 
    Song,
    League,
    Team,
    Player,
    Student
)

@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display = ['id','name','gender']

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['id','title','singer','duration']

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name','league']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name','team','kitNumber']

    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'roll', 'city']