from django.urls import path
from .views import NotificationAPIView, DeviceTokenAPIView

urlpatterns = [
    path('', NotificationAPIView.as_view(), name='notifications'),
    path('tokens/', DeviceTokenAPIView.as_view(), name='device-tokens'),
]
