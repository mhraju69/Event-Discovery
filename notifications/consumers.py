import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .serializers import NotificationSerializer
from messaging.consumers import get_user_from_token


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            token = self.scope['query_string'].decode().split('token=')[-1]
            self.user = await get_user_from_token(token)

            if not self.user:
                await self.close()
                return

            self.notification_group_name = f"user_notifications_{self.user.id}"
            await self.channel_layer.group_add(self.notification_group_name, self.channel_name)

            await self.accept()
            print(f"✅ Notification Socket Connected for {self.user.email}")

        except Exception as e:
            print(f"❌ Notification Connection Error: {e}")
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'notification_group_name'):
            await self.channel_layer.group_discard(self.notification_group_name, self.channel_name)
        print(f"✅ Notification Socket Disconnected for {getattr(self.user, 'email', 'Unknown')}")

    async def send_notification(self, event):

        notification_data = event.get('notification')
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': notification_data
        }))
