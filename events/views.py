from rest_framework import generics
from .models import Event
from core.permissions import *
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import EventFilter

# Create your views here.

class EventListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsParent]
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['time', 'created_at']

    def get_queryset(self):
        return Event.objects.filter(members=self.request.user).prefetch_related('images', 'members')


class EventCreateView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsParent]

    def perform_create(self, serializer):
        serializer.save(members=[self.request.user], admin=self.request.user)


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all().prefetch_related('images', 'members')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsEventAdmin]

    def get_queryset(self):
        return super().get_queryset().filter(admin=self.request.user)

