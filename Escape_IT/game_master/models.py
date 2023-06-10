from django.db import models

# Create your models here.

class Game(models.Model):
    active = models.BooleanField()
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    progress = models.IntegerField()
    room_number = models.IntegerField()
