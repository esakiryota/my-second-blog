import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .repositories.roomListRepository import RoomListRepository
# リアルタイムで描写している
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
                    "d": '', 
		   	        "fill": text_data_json["fill"],
		 	        "stroke": text_data_json["stroke"],
			        "stroke-width": "3",
			        "stroke-linecap": "round",
                    "id": text_data_json["id"],
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
        elif type == "delete":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'delete',
                    "id": text_data_json["id"]
                }
            )
        elif type == "moveContent":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'moveContent',
                    "id": text_data_json["id"],
                    "dx": text_data_json["dx"],
                    "dy": text_data_json["dy"]
                }
            )
        elif type == "image":
            async_to_sync(self.channel_layer.group_send)(
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
            async_to_sync(self.channel_layer.group_send)(
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
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'writing',
                    "id": text_data_json["id"],
                    "text": text_data_json["text"],
                }
            )
        elif type == "resize":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'resize',
                    "id": text_data_json["id"],
                    "w": text_data_json["w"],
                    "h": text_data_json["h"],
                }
            )
        elif type == "shareData":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'shareData',
                    "data": text_data_json["data"],
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
    
    def delete(self, event):
        self.send(text_data=json.dumps(event))
    
    def moveContent(self, event):
        self.send(text_data=json.dumps(event))

    def image(self, event):
        self.send(text_data=json.dumps(event))
    
    def textBox(self, event):
        self.send(text_data=json.dumps(event))
    
    def writing(self, event):
        self.send(text_data=json.dumps(event))

    def resize(self, event):
        self.send(text_data=json.dumps(event))

    def shareData(self, event):
        self.send(text_data=json.dumps(event))
        