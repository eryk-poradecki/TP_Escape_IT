from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import Room, Game


def home(request):
    return render(request, 'game_master/home.html')


def notifications(request):
    return render(request, 'game_master/notifications.html')


def settings(request):
    return render(request, 'game_master/settings.html')


def rooms(request):
    context = {
        'rooms': Room.objects.all()
    }

    return render(request, 'game_master/rooms.html', context)


def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    context = {
        'room': room
    }

    return render(request, 'game_master/room-detail.html', context)
