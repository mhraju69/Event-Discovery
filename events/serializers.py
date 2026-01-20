from .models import Event, EventImage
from rest_framework import serializers

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id', 'event', 'image']


class EventSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'time', 'location', 'images']
        read_only_fields = ['id']