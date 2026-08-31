from datetime import (
    datetime,
    timedelta,
)

import pytest
from django.contrib.auth.tokens import (
    default_token_generator,
)
from django.test import override_settings

from .factories import UserFactory
from .helpers import make_reset_url


@pytest.mark.django_db
def test_valid_token_is_accepted(
    client
):
    user = UserFactory()

    url = make_reset_url(
        user
    )

    response = client.get(
        url
    )

    assert response.status_code == 200

    assert (
        b"Choose a new password"
        in response.content
    )


@pytest.mark.django_db
def test_invalid_token_is_rejected(
    client
):
    user = UserFactory()

    url = make_reset_url(
        user,
        token="this-is-not-valid"
    )

    response = client.get(
        url
    )

    assert response.status_code == 400

    assert (
        b"invalid or expired"
        in response.content.lower()
    )


@pytest.mark.django_db
@override_settings(
    PASSWORD_RESET_TIMEOUT=1
)
def test_expired_token_is_rejected(
    client,
    mocker
):
    user = UserFactory()

    old_time = (
        datetime.now()
        - timedelta(seconds=10)
    )

    mocker.patch.object(
        default_token_generator,
        "_now",
        return_value=old_time
    )

    token = (
        default_token_generator.make_token(
            user
        )
    )

    mocker.stopall()

    url = make_reset_url(
        user,
        token=token
    )

    response = client.get(
        url
    )

    assert response.status_code == 400

    assert (
        b"invalid or expired"
        in response.content.lower()
    )