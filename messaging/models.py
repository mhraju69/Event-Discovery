from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class ChatRoom(models.Model):
    CONVERSATION_TYPE_CHOICES = (("direct", "Direct Chat"),("group", "Group Chat"),("event", "Event Chat"),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_type = models.CharField(max_length=10, choices=CONVERSATION_TYPE_CHOICES)
    name = models.CharField(max_length=255, blank=True, null=True)  
    event = models.ForeignKey("events.Event",on_delete=models.CASCADE,null=True,blank=True,related_name="conversations",)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name="created_conversations",)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    MESSAGE_TYPE_CHOICES = (("text", "Text"),("image", "Image"),("file", "File"),("voice", "Voice"),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name="messages",)
    sender = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="sent_messages",)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default="text")
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

