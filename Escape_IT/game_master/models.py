from django.db import models


class Room(models.Model):
    room_number = models.IntegerField()
    room_name = models.CharField(max_length=200)
    room_description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='room_images', blank=True, null=True)


class Game(models.Model):
    active = models.BooleanField()
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    progress = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
