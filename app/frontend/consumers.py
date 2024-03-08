import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"game_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send the list of active games to the client
        await self.send_active_games()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['type']

        if message == 'createGame':
            # Create a new game and send the game ID to the client
            game_id = self.create_game()
            await self.send_game_created(game_id)

    async def send_active_games(self):
        # Get the list of active games from Redis
        active_games = await self.channel_layer.redis.hgetall("active_games")
        game_ids = [int(game_id) for game_id in active_games.keys()]
        await self.send(text_data=json.dumps({
            'type': 'activeGames',
            'games': game_ids,
        }))

    async def send_game_created(self, game_id):
        await self.send(text_data=json.dumps({
            'type': 'gameCreated',
            'gameId': game_id,
        }))

    async def create_game(self):
        # Generate a unique game ID
        game_id = await self.generate_unique_id()

        # Add the game to the list of active games in Redis
        await self.channel_layer.redis.hset("active_games", game_id, self.room_group_name)

        return game_id

    async def generate_unique_id(self):
        # Increment the game counter using Redis atomic increments
        return await self.channel_layer.redis.incr("game_counter")

# class GameConsumer(AsyncWebsocketConsumer):
#     active_games = {}
#     game_counter = 0

#     async def connect(self):
#         # self.game_id = self.generate_unique_id()
#         # self.room_group_name = f'game_{self.game_id}'
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"game_{self.room_name}"

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#         await self.send(text_data=json.dumps({
#             'type': 'activeGames',
#             'games': list(self.active_games.keys()),
#         }))

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#         # Remove this game from the list of active games
#         del self.active_gamcomment %} let socket = null;


# es[self.game_id]

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['type']

#         if message == 'getActiveGames':
#             # Send the list of active games to the client
#             await self.send(text_data=json.dumps({
#                 'type': 'activeGames',
#                 'games': list(self.active_games.keys()),
#             }))

#         if message == 'createGame':
#             # Create a new game and send the game ID to the client
#             game_id = self.create_game()
#             await self.send(text_data=json.dumps({
#                 'type': 'gameCreated',
#                 'gameId': game_id,
#             }))

#         if message == 'clientConnected':
#             # Handle the new client connection
#             print('Client connected')
#             await self.send(text_data=json.dumps({
#                 'type': 'gameCreated',
#                 'gameId': game_id,
#             }))

#     def generate_unique_id(self):
#         self.__class__.game_counter += 1
#         return self.__class__.game_counter

#     def create_game(self):
#         game_id = self.generate_unique_id()
#         channel_name = f"game_{game_id}"
#         # Add the game to the list of active games
#         self.active_games[game_id] = channel_name

#         return game_id

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
