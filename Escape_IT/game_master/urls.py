from django.urls import path
from . import views as game_master_views

urlpatterns = [
    path('', game_master_views.home),
    path('notifications/', game_master_views.notifications, name='notifications'),
    path('settings/', game_master_views.settings, name='settings'),
    path('rooms/', game_master_views.rooms, name='rooms'),
    path('rooms/<int:room_id>/', game_master_views.room_detail, name='room-detail')
]
