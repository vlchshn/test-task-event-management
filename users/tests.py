import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    response = client.post(
        "/api/users/register/",
        {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123!",
        },
    )
    assert response.status_code == 201
    assert User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
def test_user_login():
    User.objects.create_user(username="testuser", email="test@example.com", password="Password123!")
    client = APIClient()
    response = client.post(
        "/api/users/login/",
        {"username": "testuser", "password": "Password123!"},
    )
    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_login_wrong_password():
    User.objects.create_user(username="testuser", email="test@example.com", password="Password123!")
    client = APIClient()
    response = client.post(
        "/api/users/login/",
        {"username": "testuser", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
