import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .repositories.roomListRepository import RoomListRepository
from .models import RoomList
from channels.db import database_sync_to_async
# リアルタイムで描写している
class ChatConsumer(AsyncWebsocketConsumer):

    room = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == "room_list":
            room_name = text_data_json['room_name']
            password = text_data_json['password']
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'room_list',
                    'room_name': room_name,
                    'password': password
                }
            )
        elif type == "draw":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'draw',
                    "d": '', 
		   	        "fill": text_data_json["fill"],
		 	        "stroke": text_data_json["stroke"],
			        "stroke-width": "3",
			        "stroke-linecap": "round",
                    "id": text_data_json["id"],
                }
            )
        elif type == "drawing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'drawing',
                    "d": text_data_json["d"]
                }
            )
        elif type == "delete":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'delete',
                    "id": text_data_json["id"]
                }
            )
        elif type == "moveContent":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'moveContent',
                    "id": text_data_json["id"],
                    "dx": text_data_json["dx"],
                    "dy": text_data_json["dy"]
                }
            )
        elif type == "image":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'image',
                    "id": text_data_json["id"],
                    "href": text_data_json["href"],
                    "cx": text_data_json["cx"],
                    "cy": text_data_json["cy"],
                    "x": text_data_json["x"],
                    "y": text_data_json["y"],
                    "width": text_data_json["width"],
                    "height": text_data_json["height"],
                }
            )
        elif type == "textBox":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'textBox',
                    "id": text_data_json["id"],
                    "text": text_data_json["text"],
                    "cx": text_data_json["cx"],
                    "cy": text_data_json["cy"],
                    "x": text_data_json["x"],
                    "y": text_data_json["y"],
                }
            )
        elif type == "writing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'writing',
                    "id": text_data_json["id"],
                    "text": text_data_json["text"],
                }
            )
        elif type == "resize":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'resize',
                    "id": text_data_json["id"],
                    "w": text_data_json["w"],
                    "h": text_data_json["h"],
                }
            )
        elif type == "shareData":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'shareData',
                    "data": text_data_json["data"],
                }
            )
        elif type == "clear":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'clear'
                }
            )
        elif type == "message":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message', 
                    'message': text_data_json["message"]
                }
            )
        elif type == "create or join":
            repos = RoomListRepository()
            now_participants = repos.addParticipants(self.room_name)
            if now_participants == 1:
                await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'create',
                    'message': 'create',
                    'number' : now_participants,
                    'room_name' : self.room_name,
                }
            )
            else:
                await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'join',
                    'message': 'join',
                    'number' : now_participants,
                    'room_name' : self.room_name,
                }
            )
        elif type == "bye":
            repos = RoomListRepository()
            now_participants = repos.removeParticipants(self.room_name)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'bye', 
                    'number': now_participants
                }
            )


    # Receive message from room group
    async def room_list(self, event):
        rlrepos = RoomListRepository()
        result = rlrepos.insert(event)
        self.send(text_data=json.dumps(result))

    async def draw(self, event):
        await self.send(text_data=json.dumps(event))

    async def drawing(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def clear(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def delete(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def moveContent(self, event):
        await self.send(text_data=json.dumps(event))

    async def image(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def textBox(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def writing(self, event):
        await self.send(text_data=json.dumps(event))

    async def resize(self, event):
        await self.send(text_data=json.dumps(event))

    async def shareData(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def message(self, event):
        await self.send(text_data=json.dumps(event))

    async def join(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def create(self, event):
        await self.send(text_data=json.dumps(event))

    async def bye(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def hello(self, event):
        await self.send(text_data=json.dumps(event))

class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        if type == "join":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'join',
                    'message': 'join',
                    'room_name' : self.room_name,
                    'user_name': text_data_json['user_name']
                }
            )
        elif type == "hello":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'hello',
                    'message': 'hello',
                    'to': text_data_json['to'],
                    'from': text_data_json['from']
                }
            )
        elif type == "message":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message',
                    'message': text_data_json['message'],
                    'to': text_data_json['to'],
                    'from': text_data_json['from']
                }
            )
        elif type == "bye":
            now_participants = await self.removeParticipantFromRepository(self.room_name)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'bye', 
                    'to': text_data_json['to'],
                    'from': text_data_json['from']
                }
            )
        elif type == "image":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'image',
                    "id": text_data_json["id"],
                    "href": text_data_json["href"],
                    "cx": text_data_json["cx"],
                    "cy": text_data_json["cy"],
                    "x": text_data_json["x"],
                    "y": text_data_json["y"],
                    "width": text_data_json["width"],
                    "height": text_data_json["height"],
                }
            )
    
    async def join(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def hello(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def create(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def message(self, event):
        await self.send(text_data=json.dumps(event))

    async def bye(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def image(self, event):
        await self.send(text_data=json.dumps(event))
    
    @database_sync_to_async
    def addParticipantFromRepository(self, room_name):
        repos = RoomListRepository()
        now_participants = repos.addParticipants(room_name)
        return now_participants
    
    @database_sync_to_async
    def removeParticipantFromRepository(self, room_name):
        repos = RoomListRepository()
        now_participants = repos.removeParticipants(room_name)
        return now_participants
    
class RoomListConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == "room_list":
            room_name = text_data_json['room_name']
            password = text_data_json['password']
            data = {"room_name": room_name, "password": password}
            result = await self.insertRoom(data)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'room_list',
                    'room_name': room_name,
                    'password': password,
                    'url_token': result["url_token"]
                }
            )

    async def room_list(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def insertRoom(self, event):
        rlrepos = RoomListRepository()
        result = rlrepos.insert(event)
        print(result)
        return result


    
        