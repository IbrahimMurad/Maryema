from django.contrib.auth import authenticate, login, logout
from rest_framework import status, views, viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import AdminSerializer, CustomerSerializer


class AdminUsersView(viewsets.ModelViewSet):
    """View for admin contol over users
    admin can list, retrieve, create, update and delete users"""

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]


class RegisterUserView(CreateAPIView):
    """View for registering new users"""

    serializer_class = CustomerSerializer


class CustomerProfileView(RetrieveUpdateDestroyAPIView):
    """View for customer to view, update and delete their profile"""

    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogInView(views.APIView):
    """View for user login"""

    def post(self, request):
        user = authenticate(
            request,
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if user:
            login(request, user)
            return Response({"detail": "User logged in"}, status=200)
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class LogOutView(views.APIView):
    """View for user logout"""

    def post(self, request):
        logout(request)
        return Response({"detail": "User logged out"}, status=200)
