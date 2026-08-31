from django.shortcuts import render
from django.contrib.auth import get_user_model

from .forms import PasswordResetRequestForm
from .services import (
    build_reset_url,
    send_reset_email,
)

User = get_user_model()

# def password_reset_request(request):
#     email = request.POST.get("email")

#     user = User.objects.filter(
#         email=email
#     ).first()

#     if user:
#         return HttpResponse(
#             "Password reset email sent"
#         )

#     return HttpResponse("Password reset request received")

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
                "If an account exists for that email, "
                "a password reset link has been sent."
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

def password_reset_confirm(
    request,
    uidb64,
    token
):
    return render(
        request,
        "reset_password.html"
    )