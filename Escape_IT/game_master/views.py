from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import Room, Game
from datetime import datetime


def home(request):
    return render(request, 'game_master/home.html', get_rooms())


def notifications(request):
    return render(request, 'game_master/notifications.html')


def settings(request):
    return render(request, 'game_master/settings.html')


def room_panel(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    context = {
        'room': room,
        'games': Game.objects.filter(room=room_id),
        'current_game': Game.objects
            .filter(room=room_id)
            .filter(start_date_time__lte=datetime.now())
            .filter(end_date_time__gte=datetime.now())[0]
    }
    return render(request, 'game_master/room-panel-view.html', context)


def rooms(request):
    context = {
        'rooms': Room.objects.all()
    }

    return render(request, 'game_master/home.html', context)
    

def get_rooms():
    context = {
        'rooms': Room.objects.all()
    }
    return context

