from django.urls import path
from . import views as gamemaster_views

urlpatterns = [
	path('', gamemaster_views.home, name='gamemaster_home'),
]
