from datetime import datetime, timedelta
import pytest
from django.contrib.auth.tokens import default_token_generator
from django.test import override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .factories import UserFactory


def make_reset_url(user, token):
    uidb64 = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    return reverse(
        "password-reset-confirm",
        kwargs={
            "uidb64": uidb64,
            "token": token,
        }
    )


@pytest.mark.django_db
def test_valid_token_is_accepted(client):
    user = UserFactory()

    token = default_token_generator.make_token(
        user
    )

    url = make_reset_url(
        user,
        token
    )

    response = client.get(url)

    assert response.status_code == 200
    assert b"Choose a new password" in response.content


@pytest.mark.django_db
def test_invalid_token_is_rejected(client):
    user = UserFactory()

    url = make_reset_url(
        user,
        "this-is-not-a-valid-token"
    )

    response = client.get(url)

    assert response.status_code == 400

    assert (
        b"invalid or expired"
        in response.content.lower()
    )


@pytest.mark.django_db
@override_settings(PASSWORD_RESET_TIMEOUT=1)
def test_expired_token_is_rejected(client, mocker):
    user = UserFactory()

    old_time = datetime.now() - timedelta(
        seconds=10
    )

    mocker.patch.object(
        default_token_generator,
        "_now",
        return_value=old_time
    )

    token = default_token_generator.make_token(
        user
    )

    mocker.stopall()

    url = make_reset_url(
        user,
        token
    )

    response = client.get(url)

    assert response.status_code == 400

    assert (
        b"invalid or expired"
        in response.content.lower()
    )