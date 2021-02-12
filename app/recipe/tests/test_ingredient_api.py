from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.serializers import IngredientSerializer
from core.models import Ingredient

INGREDIENT_URL = reverse("recipe:ingredient-list")


class PublicIngredientApiTest(TestCase):
    """Test The publicly available ingredients api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access ingredients apis"""
        resp = self.client.get(INGREDIENT_URL)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """ Test the private ingredient api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="user.ingredient#@test.com",
            name="Ingredient test"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieve a list for ingredients. """
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        resp = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user are returned"""
        user2 = get_user_model().objects.create(
            email="user2.ingredient#@test.com",
            name="Ingredient test"
        )
        Ingredient.objects.create(user=user2, name='Vinegar')
        ingredient = Ingredient.objects.create(user=self.user, name='Salt_1')

        resp = self.client.get(INGREDIENT_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(ingredient.name, resp.data[0]['name'])
        self.assertEqual(len(resp.data), 1)

    def test_creating_ingredient_successfully(self):
        """Test create a new ingredient"""
        payload = {'name': "cabbage"}
        self.client.post(INGREDIENT_URL, payload)
        exist = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exist)

    def test_creating_ingredient_invalid(self):
        """Test create a new ingredient  invalid"""
        payload = {'name': ""}
        resp = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
