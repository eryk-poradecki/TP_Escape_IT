import json
import os

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .text_to_speech import generate_tts_audio
from django.conf import settings
from urllib.parse import parse_qs
from .models import Notification, Room
from django.utils import timezone


class WebConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.room_group_name = 'web'

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

        if type == 'help_response':
            audio_content = generate_tts_audio(text_data_json['hint'])
            output_path = os.path.join(settings.MEDIA_ROOT, 'hint.mp3')
            with open(output_path, 'w+b') as audio_file:
                audio_file.write(audio_content)
            async_to_sync(self.channel_layer.group_send)(
                'unity',
                {
                    'type': 'audio_ready',
                    'message': 'Audio with hint is ready!'
                }
            )

    def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def event_handler(self, event):
        type = event['type']
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'help_request',
            'message': message
        }))


class UnityConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.room_group_name = 'unity'
        room_id = self.scope['query_string'].decode('utf-8')
        parsed_qs = parse_qs(room_id)
        self.room_id = parsed_qs.get('room_id', [''])[0]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!',
            'room_id': room_id
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == 'help_request':
            notification_message = f"Players in room {self.room_id} need help!"
            Notification.objects.create(
                type=type,
                message=notification_message,
                date_time=timezone.now(),
                room=Room.objects.filter(id=self.room_id).first(),
            )

            async_to_sync(self.channel_layer.group_send)(
                'web',
                {
                    'type': 'event_handler',
                    'request_type': type,
                    'message': notification_message
                }
            )
        elif type =='custom_help_request':
            notification_message = text_data_json['message']
            Notification.objects.create(
                type=type,
                message=notification_message,
                date_time=timezone.now(),
                room=Room.objects.filter(id=self.room_id).first(),
            )

            async_to_sync(self.channel_layer.group_send)(
                'web',
                {
                    'type': 'event_handler',
                    'request_type': type,
                    'message': notification_message
                }
            )


    def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def audio_ready(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'audio_ready',
            'message': message
        }))
