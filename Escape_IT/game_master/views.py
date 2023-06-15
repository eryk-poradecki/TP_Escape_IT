from django.shortcuts import render, redirect,get_object_or_404
from .models import Room, Game
from .forms import CreateGameForm


def home(request):
    context = {
        'rooms': Room.objects.all(),
        'games': Game.objects.all(),
        'active_page': 'home',
        'active_games': Game.objects.all().filter(active=True).count()
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
    games = Game.objects.filter(room=room_id)
    current_game = Game.objects.filter(room=room_id, active=True).first()

    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            form.instance.room = room
            form.save()
    else:
        form = CreateGameForm()

    context = {
        'room': room,
        'games': games,
        'current_game': current_game,
        'form': form
    }
    return render(request, 'game_master/room-panel-view.html', context)


def rooms(request):
    context = {
        'rooms': Room.objects.all()
    }

    return render(request, 'game_master/home.html', context)
    

def get_item(dictionary, key):
    return dictionary.get(key)


