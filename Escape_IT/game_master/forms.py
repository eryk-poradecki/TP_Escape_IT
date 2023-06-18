from django import forms
from .models import Game
from django.forms import Textarea, DateTimeField


class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['start_date_time', 'end_date_time', 'progress']
        widgets = {
            'start_date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        
