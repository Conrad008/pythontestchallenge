from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()

def password_reset_request(request):
    email = request.POST.get("email")

    user = User.objects.filter(
        email=email
    ).first()

    if user:
        return HttpResponse(
            "Password reset email sent"
        )

    return HttpResponse("Password reset request received")