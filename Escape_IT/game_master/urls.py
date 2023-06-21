from django.urls import path
from . import views as game_master_views

urlpatterns = [
    path('', game_master_views.home),
    path('notifications/', game_master_views.notifications, name='notifications'),
    path('settings/', game_master_views.settings, name='settings'),
    path('rooms/', game_master_views.rooms, name='rooms'),
    path('rooms/<int:room_id>/', game_master_views.room_panel, name='room-detail'),
    path('audio/', game_master_views.return_hint_audio, name='generate_audio'),
    path('notifications/resolve_notification/<int:id>/', game_master_views.resolve_notification, name='resolve_notification'),
    path('notifications/resolve_notification_last/<int:room_id>/', game_master_views.resolve_notification_last, name='resolve_notification_last')
]
