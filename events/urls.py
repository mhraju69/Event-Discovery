from django.urls import path
from .views import EventListCreateAPIView, EventRetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('create/', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('update/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event-retrieve-update-destroy'),
]