import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f"chat_{self.room_name}"

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

    @database_sync_to_async
    def save_message(self, sender, receiver, message):
        # Save the message to the database
        return ChatSave.objects.create(sender=sender, receiver=receiver, message=message)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender = data.get('sender')
        receiver = data.get('receiver')

        # Get sender and receiver user instances
        try:

            sender_instance = await database_sync_to_async(User.objects.get)(id=sender)
            receiver_instance = await database_sync_to_async(User.objects.get)(id=receiver)
            await self.channel_layer.group_send(
            self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'sender': sender,
                    'receiver': receiver,
                }
            )

            # Save the message to the database using the async function
            await self.save_message(sender_instance, receiver_instance, message)

        except:
            await self.channel_layer.group_send(
            self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': "sender or receiver not exist!",
                }
            )
        # import pdb;pdb.set_trace()

    async def chat_message(self, event):
        payload = {
            "message" : event.get('message'),
            "sender" : event.get('sender'),
            "receiver" : event.get('receiver')
        }

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
