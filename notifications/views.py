from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification, DeviceToken
from .serializers import NotificationSerializer, DeviceTokenSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class NotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications[:20], many=True)
        return Response(serializer.data)

    def patch(self, request):
        id = request.query_params.get('id')
        if not id:
            return Response({'success': False, 'log': 'Notification ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        notification = Notification.objects.filter(id=id, user=request.user).first()

        if not notification:
            return Response({'success': False, 'log': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

        notification.is_read = True
        notification.save()
        return Response({'success': True, 'log': 'Notification marked as read'}, status=status.HTTP_200_OK)

    def delete(self, request):
        id = request.query_params.get('id')
        if not id:
            return Response({'success': False, 'log': 'Notification ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        notification = Notification.objects.filter(id=id, user=request.user).first()

        if not notification:
            return Response({'success': False, 'log': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

        notification.delete()
        return Response({'success': True, 'log': 'Notification deleted'}, status=status.HTTP_200_OK)

class DeviceTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeviceTokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Device token registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'success': False, 'message': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        DeviceToken.objects.filter(token=token, user=request.user).delete()
        return Response({'success': True, 'message': 'Device token removed successfully'}, status=status.HTTP_200_OK)