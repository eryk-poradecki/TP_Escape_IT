from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import Room, Game
from datetime import datetime


def home(request):
    context = {
        'rooms': Room.objects.all(),
        'active_page': 'home'
    }
    return render(request, 'game_master/home.html', context)


def notifications(request):
    context = {
        'active_page': 'notifications'
    }
    return render(request, 'game_master/notifications.html', context)


def settings(request):
    context = {
        'active_page': 'settings'
    }
    return render(request, 'game_master/settings.html', context)


def room_panel(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    context = {
        'room': room,
        'games': Game.objects.filter(room=room_id),
        'current_game': Game.objects
            .filter(room=room_id)
            .filter(start_date_time__lte=datetime.now())
            .filter(end_date_time__gte=datetime.now())
    }
    return render(request, 'game_master/room-panel-view.html', context)


def rooms(request):
    context = {
        'rooms': Room.objects.all()
    }

    return render(request, 'game_master/home.html', context)
    


