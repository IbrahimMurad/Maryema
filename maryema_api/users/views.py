from django.contrib.auth.models import User
from rest_framework import viewsets

from users.models import Profile
from users.serializers import UserSerializer


# users viewset for admin
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class AdminUsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]
    # authentication_classes = [TokenAuthentication]
