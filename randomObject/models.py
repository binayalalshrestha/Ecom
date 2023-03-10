from django.db import models

class RandomObject(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.name
