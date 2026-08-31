from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def build_reset_url(request, user):
    uidb64 = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    token = default_token_generator.make_token(
        user
    )

    reset_path = reverse(
        "password-reset-confirm",
        kwargs={
            "uidb64": uidb64,
            "token": token,
        }
    )

    return request.build_absolute_uri(
        reset_path
    )


def send_reset_email(email, reset_url):
    subject = "Reset your password"

    message = (
        f"Use the following link to reset "
        f"your password:\n\n{reset_url}"
    )

    send_mail(
        subject,
        message,
        None,
        [email],
    )