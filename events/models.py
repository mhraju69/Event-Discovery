from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    time = models.DateTimeField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='event_images/')


class EventGroup(models.Model):
    TYPE = (
        ('school', 'School'),
        ('sports', 'Sports'),
        ('social', 'Social'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE, default='other')
    members = models.ManyToManyField(User, related_name='groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name