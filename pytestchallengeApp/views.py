from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import (
    default_token_generator,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.utils.encoding import force_str
from django.utils.http import (
    urlsafe_base64_decode,
)

from .forms import (
    NewPasswordForm,
    PasswordResetRequestForm,
)
from .services import (
    build_reset_url,
    send_reset_email,
)


User = get_user_model()


def password_reset_request(request):
    message = None

    if request.method == "POST":
        form = PasswordResetRequestForm(
            request.POST
        )

        if form.is_valid():
            email = form.cleaned_data[
                "email"
            ]

            user = User.objects.filter(
                email__iexact=email
            ).first()

            if user:
                reset_url = build_reset_url(
                    request,
                    user
                )

                send_reset_email(
                    user.email,
                    reset_url
                )

            message = (
                "If an account exists for that "
                "email, a password reset link "
                "has been sent."
            )

    else:
        form = PasswordResetRequestForm()

    return render(
        request,
        "request_reset.html",
        {
            "form": form,
            "message": message,
        },
    )


def get_user_from_uid(uidb64):
    try:
        user_id = force_str(
            urlsafe_base64_decode(
                uidb64
            )
        )

        return User.objects.get(
            pk=user_id
        )

    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
    ):
        return None


def password_reset_confirm(
    request,
    uidb64,
    token
):
    user = get_user_from_uid(
        uidb64
    )

    token_is_valid = (
        user is not None
        and default_token_generator.check_token(
            user,
            token
        )
    )

    if not token_is_valid:
        return render(
            request,
            "reset_password.html",
            {
                "token_valid": False,
            },
            status=400,
        )

    if request.method == "POST":
        form = NewPasswordForm(
            request.POST,
            user=user
        )

        if form.is_valid():
            new_password = (
                form.cleaned_data[
                    "password1"
                ]
            )

            user.set_password(
                new_password
            )

            user.save(
                update_fields=["password"]
            )

            return redirect(
                "password-reset-complete"
            )

    else:
        form = NewPasswordForm(
            user=user
        )

    return render(
        request,
        "reset_password.html",
        {
            "token_valid": True,
            "form": form,
        },
    )


def password_reset_complete(request):
    return render(
        request,
        "password_reset_complete.html"
    )