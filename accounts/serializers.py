from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'image', 'role']
        read_only_fields = ['id', 'email', 'role']