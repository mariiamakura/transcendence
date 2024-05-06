import json
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import time
from datetime import datetime
# from database.models import User
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class GameRoomManagerPong:

    rooms = {}  # Stores room_name: host_name

    @classmethod
    def create_room_pong(cls, host_name):
        room_id = f"{host_name}_Game"
        cls.rooms[room_id] = {"host": host_name, "guest": None}
        return room_id

    @classmethod
    def list_rooms_pong(cls):
        logger.debug("Enters list_rooms_pong")
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
        # self.last_alive_time = datetime.now()
        self.alive_timeout = 30  # seconds
        self.check_interval = 5  # seconds
        self.keep_alive_task = None
        self.flag = False

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'{self.room_name}'
        self.user = await self.get_user(self.room_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.set_user_online(True)
        # if self.keep_alive_task and not self.keep_alive_task.done():
        #     self.keep_alive_task.cancel()
        # await self.set_user_online(False)
        self.last_alive_time = datetime.now()
        # self.check_alive()
        if not self.flag:
            self.keep_alive_task = asyncio.create_task(self.check_alive())

    async def disconnect(self, close_code):
        logger.debug(f"WebSocket disconnect invoked for user: {self.user}, close_code: {close_code}")
        # await self.set_user_online(False)
        try:
            # Cancel the task
            self.keep_alive_task.cancel()
            logger.debug(f"****************trying to cancel task************* {self.user}")
        except Exception as e:
            logger.error(f"Error cancelling keep_alive_task: {e}")
        # self.keep_alive_task = None
        await super().disconnect(close_code)

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
        # code = data.get('code')

        if action == 'alive':
            self.last_alive_time = datetime.now()
            logger.debug(f"received function update: { self.last_alive_time}")
            await asyncio.sleep(1)
            await self.send(text_data=json.dumps({'action': 'keep_alive'}))

    async def keep_alive(self, event):
        await self.send(text_data=json.dumps({
            'action': 'keep_alive'
        }))

    async def check_alive(self):
        self.flag = True
        while True:
            await asyncio.sleep(self.check_interval)
            logger.debug(f"SECONDS DIFFERECE: { (datetime.now() - self.last_alive_time).total_seconds() } for {self.room_name}")
            if (datetime.now() - self.last_alive_time).total_seconds() > self.alive_timeout:
                logger.debug(f"Keep-alive timeout reached for user: {self.user}")
                await self.set_user_online(False)
                self.flag = False
                self.keep_alive_task.cancel()  # Cancel the task
                await super().disconnect()
                # await self.close()
                break
            else:
                await self.set_user_online(True)

    @database_sync_to_async
    def get_user(self, username):
        from database.models import User
        return User.objects.get(display_name=username)

    @database_sync_to_async
    def set_user_online(self, online):
        if self.user:
            self.user.online = online
            self.user.save()


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        logger.debug(f"Room name in connect: {self.room_name}")
        self.room_group_name = f'game_{self.room_name}'
        self.heartbeat_task = None
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        self.start_heartbeat()

    async def disconnect(self, close_code):
        logger.debug("Enters disconnect")
        logger.debug("self.room_name: " + self.room_name)
        self.user = await self.get_user(self.room_name)
        logger.debug("self.room_name: " + self.room_name)
        if self.user is not None:
            logger.debug("self.user: " + self.user.username)
        else:
            logger.debug("self.user is None")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_left',
                'action': 'player_left',
                # 'who': who,
                'channel_name': self.channel_name
            }
        )

        # Perform other disconnect logic as needed
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Handle any additional logic, such as closing the room or updating game state
        if self.user is not None:
            logger.debug("self.user found " + self.user.username)
            room = None
            if self.room_name in GameRoomManagerPong.rooms:
                logger.debug("self.room_name in GameRoomManagerPong.rooms")
                room = GameRoomManagerPong.rooms[self.room_name]
                if room is not None:
                    logger.debug("room closing Pong")
                    del GameRoomManagerPong.rooms[self.room_name]
            if self.room_name in GameRoomManagerMemory.rooms:
                logger.debug("self.room_name in GameRoomManagerMemory.rooms")
                room = GameRoomManagerMemory.rooms[self.room_name]
                if room is not None:
                    logger.debug("room closing Memory ")
                    del GameRoomManagerMemory.rooms[self.room_name]

        if self.heartbeat_task:
            self.heartbeat_task.cancel()

        # await self.disconnect(close_code=None)

    @database_sync_to_async
    def get_user(self, username):
        username = username
        logger.debug("Enters get_user")
        logger.debug("username: " + username)
        if username == "lobby":
            return None
        if username.endswith("_Game"):
            username = username[:-5]
        from database.models import User
        return User.objects.get(display_name=username)

    @database_sync_to_async
    def close_room_pong(self, room_name):
        # Logic to close the Pong room
        logger.debug("Enters close_room_pong")
        if room_name in GameRoomManagerPong.rooms:
            del GameRoomManagerPong.rooms[room_name]

    @database_sync_to_async
    def close_room_memory(self, room_name):
        # Logic to close the Memory room
        if room_name in GameRoomManagerMemory.rooms:
            del GameRoomManagerMemory.rooms[room_name]

    async def send_heartbeat(self):
        await self.send(text_data=json.dumps({'action': 'heartbeat'}))

    def start_heartbeat(self):
        async def heartbeat():
            while True:
                await self.send_heartbeat()
                await asyncio.sleep(5)

        self.heartbeat_task = asyncio.create_task(heartbeat())

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
                    'winner': data['winner'],
                    'scoreUpdate': data['scoreUpdate']
                }
            )

        elif action == 'game_ended_memory':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_ended_memory',
                    'winner': data['winner'],
                    'scoreUpdate': data['scoreUpdate']

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

        elif action == 'player_left':
            # host_name = data.get('host_name')
            logger.debug("enters Player left in action elif ")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'player_left',
                    'action': 'player_left'
                }
            )
            await self.disconnect(1001)
            # await self.close_room_pong(self.room_name)
            # await self.send(text_data=json.dumps({'action': 'disconnect', 'room_id': room_id}))

    async def notify_winner(self, event):
        winner = event['winner']
        # Assuming `winner` is something you can use to send a message directly to them.
        # You need to implement the logic to actually send a WebSocket message to the winner.
        await self.send(text_data=json.dumps({
            'action': 'game_over',
            'winner': winner,
            'message': 'Congratulations! The other player has disconnected, you win!'
        }))

    async def player_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_left',
            'action': 'player_left',
            'message': 'player left!'
        }))
        logger.debug("Message send and now in HOST, disconnecting...")
        await self.disconnect(1001)

    async def game_ended_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'game_ended_memory',
            'winner': event['winner'],
            'scoreUpdate': event['scoreUpdate']
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
            'winner': event['winner'],
            'scoreUpdate': event['scoreUpdate']
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

    async def player_joined_memory(self, event):
        await self.send(text_data=json.dumps({
            'action': 'player_joined_memory',
            'room_id': event['room_id'],
            'guest_name': event['guest_name'],
            'message': f"{event['guest_name']} has joined the game."
        }))

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
