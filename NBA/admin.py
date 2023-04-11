from django.contrib import admin

from . models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'age',
        'height',
        'weight',
        'position',
        'rating',
        'team',
        'manager'
        ]