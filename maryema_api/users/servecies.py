from django.conf import settings
from rest_framework.response import Response

# from rest_framework_simplejwt.tokens import RefreshToken

ACCESS_EXPIRY = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
REFRESH_EXPIRY = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()

options = {
    "httponly": True,
    "secure": False if settings.DEBUG else True,
    "samesite": None if settings.DEBUG else "Strict",
    "path": "/",
}


def set_tokens(response):
    access_token = response.data.get("access")
    refresh_token = response.data.get("refresh")
    response.set_cookie(
        key="access",
        value=access_token,
        max_age=ACCESS_EXPIRY,
        **options,
    )
    response.set_cookie(
        key="refresh",
        value=refresh_token,
        max_age=REFRESH_EXPIRY,
        **options,
    )
    response.data = {"details": "logged in successfully"}

    return response


def refresh_token(response):
    """refreshes access token and sets it in cookies"""
    access_token = response.data.get("access")
    response.set_cookie(
        key="access",
        value=access_token,
        max_age=ACCESS_EXPIRY,
        **options,
    )
    response.data = {"details": "token refreshed"}

    return response


def remove_tokens(request):
    """removes tokens from cookies and returns the response"""
    response = Response({"details": "logged out successfully"})
    response.delete_cookie("access")
    response.delete_cookie("refresh")

    return response
