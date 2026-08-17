from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, EventRegistration
from .permissions import IsOrganizerOrReadOnly
from .serializers import EventSerializer
from .tasks import send_event_registration_email


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("date")
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["date", "location"]
    search_fields = ["title", "description"]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=["post"])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        if event.date < timezone.now():
            return Response(
                {"detail": "Cannot register for a past event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if EventRegistration.objects.filter(event=event, user=user).exists():
            return Response(
                {"detail": "You are already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        EventRegistration.objects.create(event=event, user=user)

        send_event_registration_email.delay(user.email, event.title)
        return Response(
            {"detail": "Successfully registered!"},
            status=status.HTTP_201_CREATED,
        )
