from django.db import models

# Create your models here.


class Room(models.Model):
    room_number = models.IntegerField()
    room_name = models.CharField(max_length=200)
    room_description = models.CharField(max_length=200)


class Game(models.Model):
    active = models.BooleanField()
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    progress = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
