from core.models import Tag
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import TagSerializer
from rest_framework import status
from rest_framework.test import APIClient

TAGS_URL = reverse("recipe:tag-list")


class PublicTagsTests(TestCase):
    """Test The publicly available api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags. """
        resp = self.client.get(TAGS_URL)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsTests(TestCase):
    """Test the Authorized user API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="bharat.singh@test.com",
            password="bharat.singh@test.com",
            name="Bharat Singh"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessq")

        resp = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-name")
        serializers = TagSerializer(tags, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        print(resp.data)
        print(serializers.data)
        self.assertEqual(resp.data, serializers.data)

    def test_tage_retrieve_login_user_tags(self):
        """Test tags returned are for the authentication user"""
        user2 = get_user_model().objects.create_user(
            email="user2@test.com",
            password="user2"
        )
        Tag.objects.create(user=user2, name="Fru")

        tags = Tag.objects.create(user=self.user, name="Login")

        resp = self.client.get(TAGS_URL)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['name'], tags.name)
