# import pytest
# from django.urls import reverse

# from .factories import UserFactory

# @pytest.mark.django_db
# def test_existing_user_can_request_password_reset(client):
#     user = UserFactory(
#         email="Conrad@example.com"
#     )

#     response = client.post(
#         reverse("password-reset-request"),
#         {
#             "email": user.email
#         }
#     )

#     assert response.status_code == 200
#     assert b"Password reset email sent" in response.content

import pytest
from django.urls import reverse

from .factories import UserFactory


@pytest.mark.django_db
def test_password_reset_page_loads(client):
    response = client.get(
        reverse("password-reset-request")
    )

    assert response.status_code == 200
    assert b"Reset your password" in response.content


@pytest.mark.django_db
def test_existing_user_receives_reset_email(client, mocker):
    user = UserFactory(
        email="conrad@example.com"
    )

    mock_build_url = mocker.patch(
        "pytestchallengeApp.views.build_reset_url",
        return_value="http://testserver/reset/example-token/"
    )

    mock_send_email = mocker.patch(
        "pytestchallengeApp.views.send_reset_email"
    )

    response = client.post(
        reverse("password-reset-request"),
        {
            "email": user.email
        }
    )

    assert response.status_code == 200

    mock_build_url.assert_called_once_with(
        response.wsgi_request,
        user
    )

    mock_send_email.assert_called_once_with(
        user.email,
        "http://testserver/reset/example-token/"
    )


@pytest.mark.django_db
def test_unknown_user_does_not_receive_reset_email(client, mocker):
    mock_send_email = mocker.patch(
        "pytestchallengeApp.views.send_reset_email"
    )

    response = client.post(
        reverse("password-reset-request"),
        {
            "email": "unknown@example.com"
        }
    )

    assert response.status_code == 200

    mock_send_email.assert_not_called()

    assert (
        b"If an account exists for that email"
        in response.content
    )