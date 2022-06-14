# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .repositories.roomListRepository import RoomListRepository

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']

        if type == "room_list":
            # print(text_data_json)
            room_name = text_data_json['room_name']
            password = text_data_json['password']
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'room_list',
                    'room_name': room_name,
                    'password': password
                }
            )
        elif type == "draw":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'draw',
                    "d": "", 
		   	        "fill": text_data_json["fill"],
		 	        "stroke": text_data_json["stroke"],
			        "stroke-width": "3",
			        "stroke-linecap": "round"
                }
            )
        elif type == "drawing":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'drawing',
                    "d": text_data_json["d"]
                }
            )
        elif type == "clear":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'clear'
                }
            )


    # Receive message from room group
    def room_list(self, event):
        rlrepos = RoomListRepository()
        print(event)
        result = rlrepos.insert(event)
        self.send(text_data=json.dumps(result))

    def draw(self, event):
        self.send(text_data=json.dumps(event))

    def drawing(self, event):
        self.send(text_data=json.dumps(event))
    
    def clear(self, event):
        self.send(text_data=json.dumps(event))
        