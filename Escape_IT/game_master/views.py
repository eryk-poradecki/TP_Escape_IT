from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'game_master/home.html')

def notifications(request): 
    return render(request, 'game_master/notifications.html')

def settings(request):
    return render(request, 'game_master/settings.html')
