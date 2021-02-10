from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializers, AuthTokenSerializer


class CreateTokenViewSets(ObtainAuthToken):
    """Create a new token for user"""
    serializer_class = AuthTokenSerializer


class CreateUserViewSets(generics.CreateAPIView):
    """Create new user in system"""
    serializer_class = UserSerializers
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authentication user"""
    serializer_class = UserSerializers
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_object(self):
        """Retrieve or return authentication user object"""

        return self.request.user
