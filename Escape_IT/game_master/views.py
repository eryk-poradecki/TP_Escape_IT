import os

from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Game, Notification
from .forms import CreateGameForm
from datetime import datetime
from django.conf import settings as django_settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


def home(request):
    refresh_active_games()
    rooms = Room.objects.all()
    rooms_decorated = []

    for room in rooms:
        rooms_decorated.append({
            'room': room,
            'current_game': Game.objects.filter(room=room).filter(start_date_time__lte=datetime.now()).filter(end_date_time__gte=datetime.now()),
            'notification': Notification.objects.filter(room=room).filter(resolved=False),
        })

    rooms_need_help = len([room for room in rooms_decorated if room['notification']])

    context = {
        'rooms': rooms_decorated,
        'games': Game.objects.all(),
        'active_page': 'home',
        'active_games_count': Game.objects.all().filter(active=True).count(),
        'rooms_need_help': rooms_need_help,
        'title': 'Escape IT Home'
    }
    return render(request, 'game_master/home.html', context)


def notifications(request):
    rooms = Room.objects.all()
    rooms_decorated = []
    for room in rooms:
        rooms_decorated.append({
            'room': room,
        })

    context = {
        'rooms': rooms_decorated,
        'active_page': 'notifications',
        'title': 'Escape IT Notifications',
        'notifications': Notification.objects.all().order_by('-date_time')[:10],
        'current_game': Game.objects.filter(room=room).filter(start_date_time__lte=datetime.now()).filter(end_date_time__gte=datetime.now()),
    }
    return render(request, 'game_master/notifications.html', context)


def settings(request):
    context = {
        'rooms': Room.objects.all(),
        'active_page': 'settings',
        'title': 'Escape IT Settings'
    }
    return render(request, 'game_master/settings.html', context)


@csrf_exempt
def room_panel(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    games = Game.objects.filter(room=room_id)
    current_game = Game.objects.filter(room=room_id).filter(start_date_time__lte=datetime.now()).filter(end_date_time__gte=datetime.now())
    current_time = timezone.now()
    played_games = Game.objects.filter(room=room_id).filter(start_date_time__lte=datetime.now()).filter(end_date_time__lte=datetime.now())
    upcoming_games = Game.objects.filter(room=room_id).filter(start_date_time__gte=datetime.now()).filter(end_date_time__gte=datetime.now())
    notifications = Notification.objects.filter(room=room_id).filter(resolved=False).order_by('-date_time')[:10]
    custom_hint = Notification.objects.filter(room=room_id).filter(resolved=False).filter(type='custom_help_request').first()

    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            form.instance.room = room
            if (form.instance.start_date_time <= timezone.now() and form.instance.end_date_time >= timezone.now()):
                form.instance.active = True
            else:
                form.instance.active = False
            form.instance.progress = 0

            form.save()
    else:
        form = CreateGameForm()

    context = {
        'room': room,
        'games': games,
        'current_game': current_game,
        'current_time': current_time,
        'played_games': played_games,
        'upcoming_games': upcoming_games,
        'form': form,
        'title': f'Escape IT Room {room_id}',
        'notifications': notifications,
        'custom_hint': custom_hint,
    }
    return render(request, 'game_master/room-panel-view.html', context)


def rooms(request):
    context = {
        'rooms': Room.objects.all()
    }

    return render(request, 'game_master/home.html', context)
    

def get_item(dictionary, key):
    return dictionary.get(key)

def refresh_active_games(): 
    games = Game.objects.all()
    for game in games:
        if game.start_date_time <= timezone.now() and game.end_date_time >= timezone.now():
            game.active = True
        else:
            game.active = False
        game.save()


def return_hint_audio(request):
    audio_path = os.path.join(django_settings.MEDIA_ROOT, 'hint.mp3')
    if os.path.exists(audio_path):
        with open(audio_path, 'rb') as audio_file:
            return HttpResponse(audio_file, content_type='audio/mpeg')
    else:
        raise Http404('Audio file not found.')

@csrf_exempt
def resolve_notification(request, id):
    notification = Notification.objects.get(id=id)
    notification.resolved = True
    notification.save()
    return HttpResponse("Notification resolved")

@csrf_exempt
def resolve_notification_last(request, room_id):
    notification = Notification.objects.filter(room=room_id).filter(resolved=False).order_by('-date_time').first()
    if notification is not None:
        notification.resolved = True
        notification.save()
        return HttpResponse("Notification resolved")
    else:
        return HttpResponse("All notifications already resolved")