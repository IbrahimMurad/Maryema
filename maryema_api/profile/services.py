from django.conf import settings
from rest_framework.response import Response

ACCESS_EXPIRY = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
REFRESH_EXPIRY = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()


options = {
    "secure": not settings.DEBUG,
    "httponly": True,
    "samesite": None if settings.DEBUG else "Strict",
    "path": "/",
}


def set_tokens(response: Response) -> Response:
    """
    Set access and refresh tokens in cookies and remove it from response data

    Args:
        response: Response object containing access and refresh tokens
    Returns:
        Modified response with cookies set
    """
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


def refresh_token(response: Response) -> Response:
    """
    Refresh access token and set it in cookies and remove it from response data

    Args:
        response: Response object containing new access token
    Returns:
        Modified response with new access token cookie
    """
    access_token = response.data.get("access")
    response.set_cookie(
        key="access",
        value=access_token,
        max_age=ACCESS_EXPIRY,
        **options,
    )
    response.data = {"details": "token refreshed"}

    return response
