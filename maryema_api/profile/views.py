from profile.serializers import UserSerializer

from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAdmin
from feedback.serializers import FeedbackSerializer


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

    def list(self, request):
        """
        List all the users with optional search, role, and is_active filters
        """
        queryset = User.objects.all()
        if request.query_params.get("role"):
            queryset = queryset.filter(profile__role=request.query_params["role"])
        if request.query_params.get("is_active"):
            queryset = queryset.filter(is_active=request.query_params["is_active"])

        serializer = UserSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, serializer_class=FeedbackSerializer)
    def feedback(self, request, pk):
        """
        List all the feedbacks for a user
        """
        user = self.get_object()
        feedbacks = user.profile.feedbacks.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)


class CurrentUserView(APIView):

    def check_authentication(self, request):
        """
        Check if the current user is authenticated
        """
        if not request.user.is_authenticated:
            return Response(
                "Unauthorized",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return None

    def get(self, request):
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

    def patch(self, request):
        """
        This view updates the current user's information in the profile page
        """
        auth_response = self.check_authentication(request)
        if auth_response:
            return auth_response
        serializer = UserSerializer(
            request.user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        """
        This view deletes the current user's account
        """
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePassword(APIView):
    """
    This view changes the current user's password
    """

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not user.check_password(old_password):
            return Response(
                {"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "me": request.build_absolute_uri("me/"),
        }
    )
