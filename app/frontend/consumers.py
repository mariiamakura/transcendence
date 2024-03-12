import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import asyncio


class GameRoomManager:
    rooms = {}  # Stores room_name: host_name

    @classmethod
    def create_room(cls, host_name):
        room_id = f"{host_name}_Game"
        cls.rooms[room_id] = {"host": host_name, "guest": None}
        return room_id

    @classmethod
    def list_rooms(cls):
        return [room_id for room_id, details in cls.rooms.items() if details["guest"] is None]

    @classmethod
    def join_room(cls, room_id, guest_name):
        if room_id in cls.rooms and cls.rooms[room_id]["guest"] is None:
            cls.rooms[room_id]["guest"] = guest_name
            return True
        return False


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

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'create_room':
            host_name = data.get('host_name')
            room_id = GameRoomManager.create_room(host_name)
            await self.send(text_data=json.dumps({'action': 'room_created', 'room_id': room_id}))

        elif action == 'list_rooms':
            rooms = GameRoomManager.list_rooms()
            await self.send(text_data=json.dumps({'action': 'list_rooms', 'rooms': rooms}))

        elif action == 'join_room':
            room_id = data.get('room_id')
            guest_name = data.get('guest_name')
            joined = GameRoomManager.join_room(room_id, guest_name)
            if joined:
                # Notify all subscribers of the room, including the host, that a new player has joined.
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'player_joined',
                        'room_id': room_id,
                        'guest_name': guest_name,
                    }
                )
                await self.send(text_data=json.dumps({'action': 'joined_room', 'room_id': room_id}))
            else:
                await self.send(text_data=json.dumps({'action': 'error', 'message': 'Room not found or full'}))
        elif action == 'update_ball_position':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ball_position',
                    'ball_x': data['ball_x'],
                    'ball_y': data['ball_y']
                }
            )
        elif action == 'update_player_scores':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'player_scores',
                    'player1': data['player1'],
                    'player2': data['player2']
                }
            )

    async def player_scores(self, event):
        await self.send(text_data=json.dumps({
            'action': 'update_player_scores',
            'player1': event['player1'],
            'player2': event['player2']
        }))

    async def ball_position(self, event):
        await self.send(text_data=json.dumps({
            'action': 'update_ball_position',
            'ball_x': event['ball_x'],
            'ball_y': event['ball_y']
        }))

    async def player_joined(self, event):
        # Broadcast the join message to all users in the room
        await self.send(text_data=json.dumps({
            'action': 'player_joined',
            'room_id': event['room_id'],
            'guest_name': event['guest_name'],
            'message': f"{event['guest_name']} has joined the game."
        }))

        # Check if both players are present, then start countdown
        if GameRoomManager.rooms[event['room_id']]['guest'] is not None:
            # Start a 5-second countdown
            for i in range(5, 0, -1):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'game_countdown',
                        'message': str(i)
                    }
                )
                await asyncio.sleep(1)

            # Notify players to start the game
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'start_game',
                    'message': 'start'
                }
            )

    async def game_countdown(self, event):
        await self.send(text_data=json.dumps({
            'action': 'countdown',
            'message': event['message']
        }))

    async def start_game(self, event):
        await self.send(text_data=json.dumps({
            'action': 'start_game',
            'message': 'Game Starting!'
        }))
