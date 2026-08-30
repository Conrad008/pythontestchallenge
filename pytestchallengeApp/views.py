from django.shortcuts import render

from django.http import HttpResponse


def password_reset_request(request):
    return HttpResponse("Password reset request received")