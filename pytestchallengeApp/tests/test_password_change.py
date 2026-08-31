import pytest
from django.contrib.auth.tokens import (
    default_token_generator,
)
from django.urls import reverse

from .factories import UserFactory
from .helpers import make_reset_url


@pytest.mark.django_db
def test_reset_form_is_displayed_for_valid_token(
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

    assert (
        b"Change password"
        in response.content
    )


@pytest.mark.django_db
def test_passwords_must_match(
    client
):
    user = UserFactory()

    url = make_reset_url(
        user
    )

    response = client.post(
        url,
        {
            "password1": "NewStrongPass123!",
            "password2": "DifferentPass123!",
        }
    )

    assert response.status_code == 200

    assert (
        b"Passwords do not match"
        in response.content
    )

    user.refresh_from_db()

    assert user.check_password(
        "StrongPass123!"
    ) is True


@pytest.mark.django_db
def test_short_password_is_rejected(
    client
):
    user = UserFactory()

    url = make_reset_url(
        user
    )

    response = client.post(
        url,
        {
            "password1": "abc",
            "password2": "abc",
        }
    )

    assert response.status_code == 200

    assert (
        b"too short"
        in response.content.lower()
    )

    user.refresh_from_db()

    assert user.check_password(
        "StrongPass123!"
    ) is True


@pytest.mark.django_db
def test_numeric_password_is_rejected(
    client
):
    user = UserFactory()

    url = make_reset_url(
        user
    )

    response = client.post(
        url,
        {
            "password1": "123456789012",
            "password2": "123456789012",
        }
    )

    assert response.status_code == 200

    assert (
        b"entirely numeric"
        in response.content.lower()
    )

    user.refresh_from_db()

    assert user.check_password(
        "StrongPass123!"
    ) is True


@pytest.mark.django_db
def test_valid_password_changes_password(
    client
):
    user = UserFactory()

    url = make_reset_url(
        user
    )

    response = client.post(
        url,
        {
            "password1": "NewStrongPass456!",
            "password2": "NewStrongPass456!",
        }
    )

    assert response.status_code == 302

    assert response.url == reverse(
        "password-reset-complete"
    )

    user.refresh_from_db()

    assert user.check_password(
        "NewStrongPass456!"
    ) is True

    assert user.check_password(
        "StrongPass123!"
    ) is False


@pytest.mark.django_db
def test_token_becomes_invalid_after_password_change(
    client
):
    user = UserFactory()

    token = (
        default_token_generator.make_token(
            user
        )
    )

    url = make_reset_url(
        user,
        token=token
    )

    user.set_password(
        "AnotherStrongPass789!"
    )

    user.save()

    response = client.get(
        url
    )

    assert response.status_code == 400