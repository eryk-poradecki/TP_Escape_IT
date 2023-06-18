import os

from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404, HttpResponse
from .models import Room, Game
from datetime import datetime
from django.conf import settings as django_settings


def home(request):
    context = {
        'rooms': Room.objects.all(),
        'games': Game.objects.all(),
        'active_page': 'home'
    }
    return render(request, 'game_master/home.html', context)


def notifications(request):
    context = {
        'rooms': Room.objects.all(),
        'active_page': 'notifications'
    }
    return render(request, 'game_master/notifications.html', context)


def settings(request):
    context = {
        'rooms': Room.objects.all(),
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
    

def get_item(dictionary, key):
    return dictionary.get(key)


def return_hint_audio(request):
    audio_path = os.path.join(django_settings.MEDIA_ROOT, 'hint.mp3')
    if os.path.exists(audio_path):
        with open(audio_path, 'rb') as audio_file:
            return HttpResponse(audio_file, content_type='audio/mpeg')
    else:
        raise Http404('Audio file not found.')