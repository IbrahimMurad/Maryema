import logging
from profile.serializers import UserSerializer
from profile.services import refresh_token, set_tokens
from typing import Any, Optional

from django.conf import settings
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import exceptions, views

from core.permissions import IsAdmin
from feedback.serializers import FeedbackSerializer
from product.serializers import VariantSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    A view set for admin dashboard to manage users
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["username", "email", "first_name", "last_name"]
    filterset_fields = ["is_active", "profile__role"]

    @action(detail=True, serializer_class=FeedbackSerializer)
    def feedback(self, request, pk):
        """
        List all the feedbacks for a user
        """
        user = self.get_object()
        feedbacks = user.profile.feedbacks.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def wishlist(self, request, pk):
        """
        List all the product variants in the whishlist of a user
        """
        user = self.get_object()
        whishlist = user.profile.wishlist
        serializer = VariantSerializer(whishlist, many=True)
        return Response(serializer.data)


class CurrentUserView(APIView):

    def check_authentication(self, request: Request) -> Optional[Response]:
        """
        Check if the current user is authenticated
        """
        if not request.user.is_authenticated:
            return Response(
                "Unauthorized",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return None

    def get(self, request: Request) -> Response:
        """
        This view returns the current user's information for the profile page
        """
        auth_response = self.check_authentication(request)
        if auth_response:
            return auth_response
        serializer = UserSerializer(request.user, context={"request": request})
        data = serializer.data.copy()
        data.pop("url")
        return Response(data)

    def patch(self, request: Request) -> Response:
        """
        This view updates the current user's information in the profile page
        """
        auth_response = self.check_authentication(request)
        if auth_response:
            return auth_response

        try:
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        """
        This view deletes the current user's account
        """
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePassword(APIView):
    """
    This view changes the current user's password
    """

    def post(self, request: Request) -> Response:
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response(
                {"detail": "Both old and new passwords are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.check_password(old_password):
            return Response(
                {"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Register(APIView):

    def post(self, request: Request) -> Response:
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"detail": str(e) if settings.DEBUG else "Registration failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ObtainToken(views.TokenObtainPairView):
    """
    Handle user login by providing JWT tokens in cookies.
    Implements secure token storage using HTTP-only cookies.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            response = super().post(request, *args, **kwargs)
            return set_tokens(response)
        except Exception as e:
            # Log the actual error in production
            logger.error(f"Token obtainment failed: {str(e)}")
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class RefreshToken(views.TokenRefreshView):
    """
    Handle token refresh requests by validating refresh token from cookies
    and providing a new access token.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        refresh = request.COOKIES.get("refresh")
        if not refresh:
            return Response(
                {"detail": "No refresh token found in cookies"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data["refresh"] = refresh
        try:
            response = super().post(request, *args, **kwargs)
            return refresh_token(response)
        except exceptions.InvalidToken:
            return Response(
                {"detail": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            # Log the actual error in production
            logger.error(f"Token refresh failed: {str(e)}")
            return Response(
                {"detail": "Token refresh failed"}, status=status.HTTP_400_BAD_REQUEST
            )


class Logout(APIView):

    def post(self, request: Request) -> Response:
        response = Response({"details": "logged out successfully"})
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
