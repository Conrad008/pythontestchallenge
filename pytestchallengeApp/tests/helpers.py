from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def make_reset_url(user, token=None):
    uidb64 = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    if token is None:
        token = default_token_generator.make_token(
            user
        )

    return reverse(
        "password-reset-confirm",
        kwargs={
            "uidb64": uidb64,
            "token": token,
        }
    )