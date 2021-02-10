from rest_framework import generics
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
