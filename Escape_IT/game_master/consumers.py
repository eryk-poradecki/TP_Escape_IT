import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .text_to_speech import generate_tts_audio


class UnityConsumer(WebsocketConsumer):
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
        hint = text_data_json['hint']

        audio_content = generate_tts_audio(hint)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'audio_message',
                'audio_content': audio_content
            }
        )

        print('Hint:', hint)

    def hint_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'hint': 'hint',
            'message': message
        }))

    # def disconnect(self, close_code):
    #     pass