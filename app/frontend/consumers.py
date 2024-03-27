import json
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import time
from datetime import datetime
# from database.models import User
from channels.db import database_sync_to_async


class GameRoomManagerPong:

    rooms = {}  # Stores room_name: host_name

    @classmethod
    def create_room_pong(cls, host_name):
        room_id = f"{host_name}_Game"
        cls.rooms[room_id] = {"host": host_name, "guest": None}
        return room_id

    @classmethod
    def list_rooms_pong(cls):
        return [room_id for room_id, details in cls.rooms.items() if details["guest"] is None]

    @classmethod
    def join_room_pong(cls, room_id, guest_name):
        if room_id in cls.rooms and cls.rooms[room_id]["guest"] is None:
            cls.rooms[room_id]["guest"] = guest_name
            return True
        return False

    # @classmethod
    # def close_empty_rooms(cls):
    #     empty_rooms = [room_id for room_id, details in cls.rooms.items() if details["guest"] is None and not is_host_active(details["host"])]
    #     for room_id in empty_rooms:
    #         del cls.rooms[room_id]


class GameRoomManagerMemory:

    rooms = {}  # Stores room_name: host_name

    @classmethod
    def create_room_memory(cls, host_name, room_settings):
        room_id = f"{host_name}_Game"
        cls.rooms[room_id] = {"host": host_name, "guest": None, "room_settings": room_settings}
        return room_id

    @classmethod
    def list_rooms_memory(cls):
        # return [cls.rooms[room_id] for room_id, details in cls.rooms.items() if details["guest"] is None]
        return [(room_id, details['room_settings']) for room_id, details in cls.rooms.items() if details["guest"] is None]

    @classmethod
    def join_room_memory(cls, room_id, guest_name):
        if room_id in cls.rooms and cls.rooms[room_id]["guest"] is None:
            cls.rooms[room_id]["guest"] = guest_name
            return True
        return False


class KeepAliveConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.last_alive_time = datetime.now()
        self.alive_timeout = 5  # seconds
        self.check_interval = 1  # seconds

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'{self.room_name}'
        self.user = await self.get_user(self.room_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_left',
                'channel_name': self.channel_name
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.set_user_online(False)
        await asyncio.sleep(1)
        # Check if the disconnecting user is the host of a room and close the room if so
        if self.user == GameRoomManagerPong.rooms[self.room_name]["host"]:
            await self.close_room_pong(self.room_name)
        elif self.user == GameRoomManagerPong.rooms[self.room_name]["guest"]:
            await self.close_room_pong(self.room_name)
        elif self.user == GameRoomManagerMemory.rooms[self.room_name]["host"]:
            await self.close_room_memory(self.room_name)
        elif self.user == GameRoomManagerMemory.rooms[self.room_name]["guest"]:
            await self.close_room_memory(self.room_name)

    @database_sync_to_async
    def close_room_pong(self, room_name):
        # Logic to close the Pong room
        if room_name in GameRoomManagerPong.rooms:
            del GameRoomManagerPong.rooms[room_name]

    @database_sync_to_async
    def close_room_memory(self, room_name):
        # Logic to close the Memory room
        if room_name in GameRoomManagerMemory.rooms:
            del GameRoomManagerMemory.rooms[room_name]

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'alive':
            self.last_alive_time = datetime.now()
            await asyncio.sleep(1)
            await self.send(text_data=json.dumps({'action': 'keep_alive'}))

    async def keep_alive(self, event):
        await self.send(text_data=json.dumps({
            'action': 'keep_alive'
        }))

    async def check_alive(self):
        while True:
            await asyncio.sleep(self.check_interval)
            if (datetime.now() - self.last_alive_time).total_seconds() > self.alive_timeout:
                await self.set_user_online(False)
                await self.close()
                break

    @database_sync_to_async
    def get_user(self, username):
        from database.models import User
        return User.objects.get(username=username)

    @database_sync_to_async
    def set_user_online(self, online):
        if self.user:
            self.user.online = online
            self.user.save()


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # async def disconnect(self, close_code):
    #     # Leave room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'player_left',
    #             'channel_name': self.channel_name
    #         }
    #     )
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_left',
                'channel_name': self.channel_name
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.set_user_online(False)

        if self.user == GameRoomManagerPong.rooms[self.room_name]["host"]:
            await self.close_room_pong(self.room_name)
        elif self.user == GameRoomManagerPong.rooms[self.room_name]["guest"]:
            await self.close_room_pong(self.room_name)
        elif self.user == GameRoomManagerMemory.rooms[self.room_name]["host"]:
            await self.close_room_memory(self.room_name)
        elif self.user == GameRoomManagerMemory.rooms[self.room_name]["guest"]:
            await self.close_room_memory(self.room_name)

    @database_sync_to_async
    def close_room_pong(self, room_name):
        # Logic to close the Pong room
        if room_name in GameRoomManagerPong.rooms:
            del GameRoomManagerPong.rooms[room_name]

    @database_sync_to_async
    def close_room_memory(self, room_name):
        # Logic to close the Memory room
        if room_name in GameRoomManagerMemory.rooms:
            del GameRoomManagerMemory.rooms[room_name]

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'create_room_pong':
            host_name = data.get('host_name')
            room_id = GameRoomManagerPong.create_room_pong(host_name)
            await self.send(text_data=json.dumps({'action': 'room_created_pong', 'room_id': room_id}))

        elif action == 'create_room_memory':
            host_name = data.get('host_name')
            room_settings = data.get('room_settings')
            room_id = GameRoomManagerMemory.create_room_memory(host_name, room_settings)
            await self.send(text_data=json.dumps({'action': 'room_created_memory', 'room_id': room_id}))

        elif action == 'list_rooms_pong':
            rooms = GameRoomManagerPong.list_rooms_pong()
            await self.send(text_data=json.dumps({'action': 'list_rooms_pong', 'rooms': rooms}))

        elif action == 'list_rooms_memory':
            rooms = GameRoomManagerMemory.list_rooms_memory()
            await self.send(text_data=json.dumps({'action': 'list_rooms_memory', 'rooms': rooms}))

        elif action == 'join_room_pong':
            room_id = data.get('room_id')
            guest_name = data.get('guest_name')
            joined = GameRoomManagerPong.join_room_pong(room_id, guest_name)
            if joined:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'player_joined_pong',
                        'room_id': room_id,
                        'guest_name': guest_name,
                    }
                )
                await self.send(text_data=json.dumps({'action': 'joined_room_pong', 'room_id': room_id}))
            else:
                await self.send(text_data=json.dumps({'action': 'error', 'message': 'Room not found or full'}))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_countdown_pong',
                    'message': 'message'
                }
            )
            # await asyncio.sleep(1)
            # time.sleep(1)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'start_game_pong',
                    'message': 'start'
                }
            )

        elif action == 'join_room_memory':
            room_id = data.get('room_id')
            guest_name = data.get('guest_name')
            joined = GameRoomManagerMemory.join_room_memory(room_id, guest_name)
            if joined:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'player_joined_memory',
                        'room_id': room_id,
                        'guest_name': guest_name,
                    }
                )
                await self.send(text_data=json.dumps({'action': 'joined_room_memory', 'room_id': room_id}))
            else:
                await self.send(text_data=json.dumps({'action': 'error', 'message': 'Room not found or full'}))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_countdown_memory',
                    'message': 'message'
                }
            )
            # await asyncio.sleep(1)
            # time.sleep(1)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'start_game_memory',
                    'message': 'start'
                }
            )

        elif action == 'send_settings_memory':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_settings_memory',
                    'settings': data['settings']
                }
            )
        elif action == 'update_ball_position_pong':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ball_position',
                    'ball_x': data['ball_x'],
                    'ball_y': data['ball_y']
                }
            )
        elif action == 'update_player_scores_pong':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'player_scores_pong',
                    'player1': data['player1'],
                    'player2': data['player2']
                }
            )

        elif action == 'game_ended_pong':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_ended_pong',
                    'winner': data['winner']
                }
            )

        elif action == 'game_ended_memory':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_ended_memory',
                    'winner': data['winner']
                }
            )
        elif action == 'host_key_event':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'host_key_event',
                    'key': data['key']
                }
            )

        elif action == 'client_key_event':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'client_key_event',
                    'key': data['key']
                }
            )

        elif action == 'get_host_player':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'get_host_player',
                    'key': data['name']
                }
            )

        elif action == 'card_info':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_card_info',
                    'cards': data['cards'],
                    'settings': data['settings']
                }
            )

        elif action == 'player_turn_memory':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'player_turn_memory',
                    'player': data['player']
                }
            )

        elif action == 'card_clicked':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'card_clicked',
                    'card_id': data['card_id']
                }
            )

        elif action == 'card_returned':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'card_returned',
                    'card_id': data['card_id']
                }
            )

        elif action == 'update_score_memory':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_score_memory',
                    'score1': data['score1'],
                    'score2': data['score2']
                }
            )

    async def notify_winner(self, event):
        winner = event['winner']
        # Assuming `winner` is something you can use to send a message directly to them.
        # You need to implement the logic to actually send a WebSocket message to the winner.
        await self.send(text_data=json.dumps({
            'action': 'game_over',
            'winner': winner,
            'message': 'Congratulations! The other player has disconnected, you win!'
        }))

    async def game_ended_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'game_ended_memory',
            'winner': event['winner']
        }))

    async def update_score_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'update_score_memory',
            'score1': event['score1'],
            'score2': event['score2']
        }))

    async def card_returned(self, event):
        await self.send(text_data=json.dumps({
            'action': 'card_returned',
            'card_id': event['card_id']
        }))

    async def card_clicked(self, event):
        await self.send(text_data=json.dumps({
            'action': 'card_clicked',
            'card_id': event['card_id']
        }))

    async def player_turn_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'player_turn_memory',
            'player': event['player']
        }))

    async def send_card_info(self, event):
        await self.send(text_data=json.dumps({
            'action': 'card_info',
            'cards': event['cards'],
            'settings': event['settings']
        }))

    async def get_host_player(self, event):
        await self.send(text_data=json.dumps({
            'action': 'get_host_player',
            'key': event['key']
        }))

    async def client_key_event(self, event):
        await self.send(text_data=json.dumps({
            'action': 'client_key_event',
            'key': event['key']
        }))

    async def host_key_event(self, event):
        await self.send(text_data=json.dumps({
            'action': 'host_key_event',
            'key': event['key']
        }))

    async def game_ended_pong(self, event):
        await self.send(text_data=json.dumps({
            'action': 'game_ended_pong',
            'winner': event['winner']
        }))

    async def player_scores_pong(self, event):
        await self.send(text_data=json.dumps({
            'action': 'update_player_scores_pong',
            'player1': event['player1'],
            'player2': event['player2']
        }))

    async def ball_position(self, event):
        await self.send(text_data=json.dumps({
            'action': 'update_ball_position_pong',
            'ball_x': event['ball_x'],
            'ball_y': event['ball_y']
        }))

    async def player_joined_pong(self, event):
        await self.send(text_data=json.dumps({
            'action': 'player_joined_pong',
            'room_id': event['room_id'],
            'guest_name': event['guest_name'],
            'message': f"{event['guest_name']} has joined the game."
        }))
        # if GameRoomManagerPong.rooms[event['room_id']]['guest'] is not None:
        #     for i in range(5, 0, -1):
        #         await self.channel_layer.group_send(
        #             self.room_group_name,
        #             {
        #                 'type': 'game_countdown_pong',
        #                 'message': str(i)
        #             }
        #         )
        #         await asyncio.sleep(1)

        #     await self.channel_layer.group_send(
        #         self.room_group_name,
        #         {
        #             'type': 'start_game_pong',
        #             'message': 'start'
        #         }
        #     )

    async def player_joined_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'player_joined_memory',
            'room_id': event['room_id'],
            'guest_name': event['guest_name'],
            'message': f"{event['guest_name']} has joined the game."
        }))
        # if GameRoomManagerMemory.rooms[event['room_id']]['guest'] is not None:
        #     for i in range(5, 0, -1):
        #         await self.channel_layer.group_send(
        #             self.room_group_name,
        #             {
        #                 'type': 'game_countdown_memory',
        #                 'message': str(i)
        #             }
        #         )
        #         await asyncio.sleep(1)

        #     await self.channel_layer.group_send(
        #         self.room_group_name,
        #         {
        #             'type': 'start_game_memory',
        #             'message': 'start'
        #         }
        #     )

    async def game_countdown_pong(self, event):
        for i in range(5, 0, -1):
            await self.send(text_data=json.dumps({
                'action': 'game_countdown_pong',
                'message': str(i)
            }))
            await asyncio.sleep(1)

    async def start_game_pong(self, event):
        await self.send(text_data=json.dumps({
            'action': 'start_game_pong',
            'message': 'Game Starting!'
        }))

    async def game_countdown_memory(self, event):
        for i in range(5, 0, -1):
            await self.send(text_data=json.dumps({
                'action': 'game_countdown_memory',
                'message': str(i)
            }))
            await asyncio.sleep(1)

    async def start_game_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'start_game_memory',
            'message': 'Game Starting!'
        }))
