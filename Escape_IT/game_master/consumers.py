import json
import os

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .text_to_speech import generate_tts_audio
from django.conf import settings
from urllib.parse import parse_qs
from .models import Notification, Room, Game
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
        type = event['event_type']
        message = event['message']

        self.send(text_data=json.dumps({
            'type': type,
            'room_id': event['room_id'],
            'notification_id': event['notification_id'],
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
            notification_message = f"Players in Room {self.room_id} need help!"
            Notification.objects.create(
                type=type,
                message=notification_message,
                date_time=timezone.now().__add__(timezone.timedelta(hours=2)),
                room=Room.objects.filter(id=self.room_id).first(),
                resolved=False
            )

            async_to_sync(self.channel_layer.group_send)(
                'web',
                {
                    'type': 'event_handler',
                    'event_type': type,
                    'room_id': self.room_id,
                    'notification_id': Notification.objects.latest('date_time').id,
                    'message': notification_message
                }
            )
        elif type =='custom_help_request':
            notification_message = f"Room {self.room_id} " + text_data_json['message']
            Notification.objects.create(
                type=type,
                message=notification_message,
                date_time=timezone.now().__add__(timezone.timedelta(hours=2)),
                room=Room.objects.filter(id=self.room_id).first(),
                resolved=False
            )

            async_to_sync(self.channel_layer.group_send)(
                'web',
                {
                    'type': 'event_handler',
                    'event_type': type,
                    'room_id': self.room_id,
                    'notification_id': Notification.objects.latest('date_time').id,
                    'message': notification_message
                }
            )
        elif type == 'progress':
            current_date_time = timezone.now().__add__(timezone.timedelta(hours=2))
            try:
                game = Game.objects.filter(
                    room_id=self.room_id,
                    start_date_time__lte=current_date_time,
                    end_date_time__gte=current_date_time,
                ).latest('start_date_time')
                game.progress += 25
                game.save()
                notification_message = f'Players in Room {self.room_id} made progress. Current progress: {game.progress}%'
                Notification.objects.create(
                    type=type,
                    message=notification_message,
                    date_time=current_date_time,
                    room=Room.objects.filter(id=self.room_id).first(),
                    resolved=True
                )
                async_to_sync(self.channel_layer.group_send)(
                    'web',
                    {
                        'type': 'event_handler',
                        'event_type': type,
                        'message': notification_message
                    }
                )
            except (Game.DoesNotExist):
                print("Game does not exist")
            

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
