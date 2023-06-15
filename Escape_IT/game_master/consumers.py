import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

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
        hint = text_data_json['hint'];

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'hint_message',
                'message': hint
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