from django.urls import path

from .views import password_reset_request


urlpatterns = [
    path(
        "password-reset/",
        password_reset_request,
        name="password-reset-request",
    ),
]