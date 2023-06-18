import json
import os

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .text_to_speech import generate_tts_audio
from django.conf import settings

class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == 'help_request':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'help_request',
                    'message': 'Help was requested by the players!'
                }
            )
        elif type == 'help_response':
            audio_content = generate_tts_audio(text_data_json['hint'])
            output_path = os.path.join(settings.MEDIA_ROOT, 'hint.mp3')
            with open(output_path, 'w+b') as audio_file:
                audio_file.write(audio_content)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'audio_ready',
                    'message': 'Audio with hint is ready!'
                }
            )

    def help_request(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'help_request',
            'message': message
        }))

    def audio_ready(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'audio_ready',
            'message': message
        }))