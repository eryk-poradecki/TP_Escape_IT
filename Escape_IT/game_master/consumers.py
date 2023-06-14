import json
from channels.generic.websocket import WebsocketConsumer

class UnityConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        hint = text_data_json['hint'];

        print('Hint:', hint)
        self.send(text_data=json.dumps({
            'hint': hint
        }))

    # def disconnect(self, close_code):
    #     pass