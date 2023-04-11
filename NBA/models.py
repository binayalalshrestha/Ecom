from django.db import models

class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    position = models.CharField(max_length=100)
    rating = models.IntegerField()
    team = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

