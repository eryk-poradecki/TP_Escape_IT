from django import forms
from .models import Game
from django.forms import Textarea


class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['start_date_time', 'end_date_time', 'progress']
        
