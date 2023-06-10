from .models import Rooms
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'game_master/home.html')

def notifications(request): 
    return render(request, 'game_master/notifications.html')

def settings(request):
    return render(request, 'game_master/settings.html')

def get_room_data(request):

    rooms_data = {
        'room_number': 1,
        'room_name': 'Room 1',
        'room_description': 'This is room 1',
    } #for all the records 
    template = loader.get_template('base.html')
    context={
      'rooms_data': rooms_data,    
    } 

    return HttpResponse(template.render(context, request))

def get_games_data(request):

    games_data = {
        'active': True,
        'start_date_time': '2021-10-10 10:10:10',
        'end_date_time': '2021-10-10 10:10:10',
        'progress': 1,
        'room': 1,
    } #for all the records 
    template = loader.get_template('base.html')
    context={
      'games_data': games_data,    
    } 

    return HttpResponse(template.render(context, request))