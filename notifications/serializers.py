from .models import *
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ['token', 'platform']

    def create(self, validated_data):
        user = self.context['request'].user
        token = validated_data.get('token')
        platform = validated_data.get('platform')
        
        device_token, created = DeviceToken.objects.update_or_create(
            token=token,
            defaults={'user': user, 'platform': platform}
        )
        return device_token