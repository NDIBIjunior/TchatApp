from channels.db import database_sync_to_async
from .models import Room, Message
import json
from channels.generic.websocket import AsyncWebsocketConsumer

def get_room_and_messages(room_name):
    room = Room.objects.get(name=room_name)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    return room, list(messages)
get_room_and_messages_async = database_sync_to_async(get_room_and_messages)

def save_message(room_name, sender, content,
                 file_url=None, file_name=None, file_type=None):
    room = Room.objects.get(name=room_name)
    return Message.objects.create(
        room=room,
        sender=sender,
        content=content if file_url is None else "",
        file_url=file_url or "",
        file_name=file_name or "",
        file_type=file_type or ""
    )
save_message_async = database_sync_to_async(save_message)

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

        # Récupérer la salle et les messages de manière asynchrone
        try:
            room, messages = await get_room_and_messages_async(self.room_name)
            # Envoyer les informations de la salle au client
            messages_data = [msg.to_dict() for msg in messages]
            await self.send(text_data=json.dumps({
                'type': 'message_history',
                'messages': messages_data
            }))
        except Room.DoesNotExist:
        # Gérer le cas où la salle n'existe pas
            pass



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
        print(f"Received message: {message} from {self.user_name} in room {self.room_name}")

        # on récupère tous les champs du JSON text_data
        if message_type == 'file':
            print('fichier *******************************************\n\n')
            await save_message_async(
                self.room_name, self.user_name, "",
                file_url      = data['message'],
                file_name     = data['filename'],
                file_type     = data['file_type']
            )
        else:
            await save_message_async(self.room_name, self.user_name, data['message'])


        # Sauvegarder le message dans la base de données
        if message_type == 'text' and not message.endswith("est en train d'écrire..."):
            await save_message_async(self.room_name, self.user_name, message)

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
