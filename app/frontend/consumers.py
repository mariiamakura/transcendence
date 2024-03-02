import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class PongConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'pong_room'

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.accept()

        # self.send(text_data=json.dumps({
        #     'type': 'connection established',
        #     'message': 'You are now connected to the server'
        # }))

    # def disconnect(self, close_code):
    #     pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'pong_message',
                'message': message
            }
        )

    def pong_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'pong_message',
            'message': message
        }))
