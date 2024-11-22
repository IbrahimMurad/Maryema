from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.models import User
from users.servecies import refresh_token, remove_tokens, set_tokens

from .serializers import AdminUserSerializer, UserSerializer


class AdminCustomersViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        """
        Retrieve all users with pagination.
        """
        paginator = PageNumberPagination()
        paginator.page_size = 10
        users = User.objects.all()
        result_page = paginator.paginate_queryset(users, request)
        serializer = AdminUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def customer(self, request, pk=None):
        """
        Retrieve, update, or delete a specific user by ID.
        """
        try:
            user = User.objects.get(pk=pk)
            if request.method == "GET":
                serializer = AdminUserSerializer(user)
                return Response(serializer.data)
            elif request.method == "PUT":
                serializer = AdminUserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request.method == "DELETE":
                user.delete()
                return Response({"details": "User deleted"})
        except ObjectDoesNotExist:
            return Response(
                {"details": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"details": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class ProfileViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving, updating, and deleting the current user's profile.
    """

    permission_classes = [IsAuthenticated]

    def profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == "PUT":
            print(request.data)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            password = request.data.get("password")
            if not password:
                return Response(
                    {"details": "Password is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not user.check_password(password):
                return Response(
                    {"details": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
                )
            user.delete()
            return Response({"details": "User deleted"})
        return Response(
            {"details": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class UserAuthViewSet(viewsets.ViewSet):
    """
    ViewSet for user authentication actions: register, login, logout.
    """

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """logout view"""
        auth.logout(request)
        return remove_tokens(request)


class CustomOptainToken(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            response = super().post(request, *args, **kwargs)
            return set_tokens(response)
        except Exception:
            return Response(
                {"details": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class CustomRefreshToken(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh = request.COOKIES.get("refresh")
        if not refresh:
            return Response(
                {"details": "Refresh token is not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.data["refresh"] = refresh
        try:
            response = super().post(request, *args, **kwargs)
            return refresh_token(response)

        except InvalidToken:
            return Response(
                {"details": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class ChangePassword(viewsets.ViewSet):
    """
    ViewSet for changing the password of the user.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def change_password(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            return Response(
                {"details": "Old and new passwords are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.check_password(old_password):
            return Response(
                {"details": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user.set_password(new_password)
            user.save()
            return Response({"details": "Password changed"})
        except Exception:
            return Response(
                {"details": "Password not changed"}, status=status.HTTP_400_BAD_REQUEST
            )
