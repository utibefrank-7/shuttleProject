import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone



class ComplaintConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.room_group_name =f'complaint_{self.ticket_id}'


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        async  def disconnect(self, close_code):
            await self.channel_layer.group_disard(
                self.room_group_name,
                self.channel_name
            )
        async def receive(self, text_data):
            data = json.loads(text_data)
            message = data.get('message', '')
            sender = self.scope['user']

            # Save message to database
            await self.save_message(sender, message)

            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username,
                    'timestamp': timezone.now().strftime('%H:%M'),
                    'is_admin': sender.role == 'admin',
                }
            )

        async def chat_message(self, event):
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'sender': event['sender'],
                'timestamp': event['timestamp'],
                'is_admin': event['is_admin'],
            }))

        @database_sync_to_async
        def save_message(self, sender, message):
            from .models import ComplaintMessage, ComplaintTicket
            ticket = ComplaintTicket.objects.get(id=self.ticket_id)
            ComplaintMessage.objects.create(
                ticket=ticket,
                sender=sender,
                message=message
            )