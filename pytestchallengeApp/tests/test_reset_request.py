import pytest
from django.urls import reverse

from .factories import UserFactory

@pytest.mark.django_db
def test_existing_user_can_request_password_reset(client):
    user = UserFactory(
        email="Conrad@example.com"
    )

    response = client.post(
        reverse("password-reset-request"),
        {
            "email": user.email
        }
    )

    assert response.status_code == 200
    assert b"Password reset email sent" in response.content