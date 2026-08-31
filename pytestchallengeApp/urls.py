from django.urls import path

from .views import (
    password_reset_request,
    password_reset_confirm,
)

urlpatterns = [
    path(
        "password-reset/",
        password_reset_request,
        name="password-reset-request",
    ),

    path(
        "password-reset/<str:uidb64>/<str:token>/",
        password_reset_confirm,
        name="password-reset-confirm",
    ),
]