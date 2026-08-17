import pytest
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from rest_framework.test import APIClient

from .models import Event, EventRegistration

User = get_user_model()


def make_future_event(organizer, days=1, **kwargs):
    defaults = {
        "title": "Test Event",
        "description": "Test description",
        "date": now() + timedelta(days=days),
        "location": "Kyiv",
        "organizer": organizer,
    }
    defaults.update(kwargs)
    return Event.objects.create(**defaults)


@pytest.mark.django_db
def test_create_event():
    user = User.objects.create_user(username="org", password="pass")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        "/api/events/",
        {
            "title": "Test Event",
            "description": "Test Desc",
            "date": now() + timedelta(days=1),
            "location": "Kyiv",
        },
    )

    assert response.status_code == 201
    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_create_event_in_past():
    user = User.objects.create_user(username="org", password="pass")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        "/api/events/",
        {
            "title": "Past Event",
            "description": "Should fail",
            "date": now() - timedelta(days=1),
            "location": "Kyiv",
        },
    )

    assert response.status_code == 400
    assert "date" in response.data


@pytest.mark.django_db
def test_list_events_unauthenticated():
    client = APIClient()
    response = client.get("/api/events/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_event_by_organizer():
    organizer = User.objects.create_user(username="organizer", password="pass")
    event = make_future_event(organizer)
    client = APIClient()
    client.force_authenticate(user=organizer)

    response = client.patch(f"/api/events/{event.pk}/", {"title": "Updated Title"})

    assert response.status_code == 200
    event.refresh_from_db()
    assert event.title == "Updated Title"


@pytest.mark.django_db
def test_update_event_by_non_organizer():
    organizer = User.objects.create_user(username="organizer", password="pass")
    other = User.objects.create_user(username="other", password="pass")
    event = make_future_event(organizer)
    client = APIClient()
    client.force_authenticate(user=other)

    response = client.patch(f"/api/events/{event.pk}/", {"title": "Hacked Title"})

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_event_by_organizer():
    organizer = User.objects.create_user(username="organizer", password="pass")
    event = make_future_event(organizer)
    client = APIClient()
    client.force_authenticate(user=organizer)

    response = client.delete(f"/api/events/{event.pk}/")

    assert response.status_code == 204
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_delete_event_by_non_organizer():
    organizer = User.objects.create_user(username="organizer", password="pass")
    other = User.objects.create_user(username="other", password="pass")
    event = make_future_event(organizer)
    client = APIClient()
    client.force_authenticate(user=other)

    response = client.delete(f"/api/events/{event.pk}/")

    assert response.status_code == 403
    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_register_for_event(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    organizer = User.objects.create_user(username="organizer", password="pass")
    attendee = User.objects.create_user(username="attendee", password="pass")
    event = make_future_event(organizer)
    client = APIClient()
    client.force_authenticate(user=attendee)

    response = client.post(f"/api/events/{event.pk}/register/")

    assert response.status_code == 201
    assert EventRegistration.objects.filter(event=event, user=attendee).exists()


@pytest.mark.django_db
def test_register_for_past_event():
    organizer = User.objects.create_user(username="organizer", password="pass")
    attendee = User.objects.create_user(username="attendee", password="pass")
    event = Event.objects.create(
        title="Past Event",
        description="Already over",
        date=now() - timedelta(days=1),
        location="Kyiv",
        organizer=organizer,
    )
    client = APIClient()
    client.force_authenticate(user=attendee)

    response = client.post(f"/api/events/{event.pk}/register/")

    assert response.status_code == 400
    assert "Cannot register for a past event." in response.data["detail"]


@pytest.mark.django_db
def test_register_for_event_twice(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    organizer = User.objects.create_user(username="organizer", password="pass")
    attendee = User.objects.create_user(username="attendee", password="pass")
    event = make_future_event(organizer)
    EventRegistration.objects.create(event=event, user=attendee)
    client = APIClient()
    client.force_authenticate(user=attendee)

    response = client.post(f"/api/events/{event.pk}/register/")

    assert response.status_code == 400
    assert "already registered" in response.data["detail"]
