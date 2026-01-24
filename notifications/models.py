from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.

class Notification(models.Model):
    NOTIFICATION_TYPES = (('message', 'New Message'),('event', 'Event Update'),('invite', 'Invitation'),('system', 'System'),)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or 'Notification'} for {self.user.email}"
