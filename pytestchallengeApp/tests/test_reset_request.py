import pytest
from django.urls import reverse

from .factories import UserFactory


@pytest.mark.django_db
def test_password_reset_page_loads(
    client
):
    response = client.get(
        reverse(
            "password-reset-request"
        )
    )

    assert response.status_code == 200

    assert (
        b"Reset your password"
        in response.content
    )


@pytest.mark.django_db
def test_existing_user_receives_reset_email(
    client,
    mocker
):
    user = UserFactory(
        email="aisha@example.com"
    )

    reset_url = (
        "http://testserver/"
        "password-reset/example/token/"
    )

    mock_build_url = mocker.patch(
        "pytestchallengeApp.views.build_reset_url",
        return_value=reset_url
    )

    mock_send_email = mocker.patch(
        "pytestchallengeApp.views.send_reset_email"
    )

    response = client.post(
        reverse(
            "password-reset-request"
        ),
        {
            "email": user.email
        }
    )

    assert response.status_code == 200

    mock_build_url.assert_called_once()

    mock_send_email.assert_called_once_with(
        user.email,
        reset_url
    )


@pytest.mark.django_db
def test_unknown_user_does_not_receive_email(
    client,
    mocker
):
    mock_build_url = mocker.patch(
        "pytestchallengeApp.views.build_reset_url"
    )

    mock_send_email = mocker.patch(
        "pytestchallengeApp.views.send_reset_email"
    )

    response = client.post(
        reverse(
            "password-reset-request"
        ),
        {
            "email": "unknown@example.com"
        }
    )

    assert response.status_code == 200

    mock_build_url.assert_not_called()

    mock_send_email.assert_not_called()

    assert (
        b"If an account exists"
        in response.content
    )