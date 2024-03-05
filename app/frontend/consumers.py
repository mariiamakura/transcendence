import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class GameConsumer(AsyncWebsocketConsumer):
    active_games = set()

    async def connect(self):
        # ...

        # Add this game to the list of active games
        self.active_games.add(self.room_group_name)

        await self.accept()

    async def disconnect(self, close_code):
        # ...

        # Remove this game from the list of active games
        self.active_games.remove(self.room_group_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message == 'getActiveGames':
            # Send the list of active games to the client
            await self.send(text_data=json.dumps({
                'type': 'activeGames',
                'games': list(self.active_games),
            }))
        
        if message == 'createGame':
            # Create a new game and send the game ID to the client
            game_id = self.create_game()
            await self.send(text_data=json.dumps({
                'type': 'gameCreated',
                'gameId': game_id,
            }))
    
    async def send_game_update(self, event):
        # Send game updates to the client
        await self.send(text_data=json.dumps({
            'type': 'gameUpdate',
            'state': event['state'],
        }))
        
    async def send_game_over(self, event):
        # Send game over message to the client
        await self.send(text_data=json.dumps({
            'type': 'gameOver',
            'winner': event['winner'],
        }))
        
    async def send_game_created(self, event):
        # Send game created message to the client
        await self.send(text_data=json.dumps({
            'type': 'gameCreated',
            'gameId': event['gameId'],
        }))
        
        


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
