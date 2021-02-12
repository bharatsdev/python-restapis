from core.models import Recipe, Tag, Ingredient
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPE_URL = reverse("recipe:recipe-list")


def sample_tag(user, name="Main Course"):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name="Cinnamon"):
    """Create and return a sample Ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **param):
    """Create and return a sample recipe"""
    default = {
        "title": "SampleRecipe",
        "time_minutes": 10,
        "price": 10.00
    }
    default.update(default)
    return Recipe.objects.create(user=user, **default)


class PublicRecipeApiTest(TestCase):
    """Test UnAuthorize access of API"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test Authentication required to access recipe apis"""
        resp = self.client.get(RECIPE_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test Unauthorized recipe api access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="bharat.singh@robosoft.in.com",
            password="bharat.singh@robosoft.in.com"
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        """Test retrieve list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        resp = self.client.get(RECIPE_URL)

        Recipe.objects.all().order_by("-id")
        # serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # self.assertEqual(resp.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test Retrieving recipes for users"""

        user2 = get_user_model().objects.create(
            email="test42!@test.com",
            password="test42!@test.com"
        )

        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        resp = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(len(resp.data), 1)
