from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification
from .serializers import NotificationSerializer

def send_notification(user, title, message, notification_type='system'):
    """
    Saves a notification to the database and broadcasts it via WebSocket.
    """
    # 1. Save to DB
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        type=notification_type
    )

    # 2. Serialize
    serializer = NotificationSerializer(notification)
    notification_data = serializer.data

    # 3. Broadcast
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_notifications_{user.id}",
        {
            "type": "send_notification",
            "notification": notification_data
        }
    )
    return notification


