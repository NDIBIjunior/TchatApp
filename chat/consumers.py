# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extraction des paramètres nommés
        self.room_name  = self.scope["url_route"]["kwargs"]["room_name"]
        self.user_name  = self.scope["url_route"]["kwargs"]["user_name"]

        # Groupe Channels pour la diffusion
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data    = json.loads(text_data)
        message_type = data.get('message_type', 'text')
        message = data["message"]
        filename = data.get('filename', '')
        file_type    = data.get('file_type', '')
        display_name = data.get('display_name', '')

        # Send message to room group, en ajoutant le nom de l'expéditeur
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":     "chat_message",
                "username": self.user_name,
                "message":  message,
                "message_type": message_type,
                "filename": filename,
                'file_type':    file_type,
                'display_name': display_name,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username':     event['username'],
            'message':      event['message'],
            'message_type': event['message_type'],
            'filename':     event['filename'],
            'file_type':    event['file_type'],
            'display_name': event['display_name'],
        }))
