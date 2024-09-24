from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User, Group
from channels.db import database_sync_to_async
import json
from .models import MessageModel

class UserChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def is_user_in_group(self, user, group_name):
        return user.groups.filter(name=group_name).exists()

    async def connect(self):
        self.user = self.scope['user']
        
        if self.user.is_authenticated:
            self.room_name = f"user_{self.user.id}"
            self.room_group_name = f"chat_{self.room_name}"

            if await self.is_user_in_group(self.user, 'Менеджеры'):
                self.room_group_name = self.scope['url_route']['kwargs']['room_name']

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')  # Используем .get() для безопасности

        # Проверка, что сообщение не пустое
        if message:
            try:
                # Сохраняем сообщение в базе данных
                msg = await database_sync_to_async(MessageModel.objects.create)(
                    sender=self.user,
                    room_name=self.room_group_name,
                    content=message
                )
            except Exception as e:
                await self.send(text_data=json.dumps({'error': str(e)}))
                return

            # Отправляем сообщение в группу
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.user.username
                }
            )
        else:
            await self.send(text_data=json.dumps({'error': 'Empty message not allowed'}))

    async def chat_message(self, data):
        message = data['message']
        sender = data['sender']

        await self.send(
            text_data=json.dumps({
                'message': message,
                'sender': sender
            })
        )

class UserNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'user_{self.user.id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name          
        )

    async def availability_notification(self, event):

        message = event['message']

        await self.send(
            text_data=json.dumps({
                'message' : message
            })     
        )