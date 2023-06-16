from django import forms
from .models import Game


class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['start_date_time', 'end_date_time', 'progress', 'room']
