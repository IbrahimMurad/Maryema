from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """Custom JWTAuthentication class to authenticate users using cookies"""

    def authenticate(self, request):
        """overriden authenticate method to authenticate users using cookies"""
        access_token = request.COOKIES.get("access")
        if not access_token:
            return None

        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token
