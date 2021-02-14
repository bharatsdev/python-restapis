from core.models import Recipe, Tag, Ingredient
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeSerializer, RecipeDetailsSerializer
from rest_framework import status
from rest_framework.test import APIClient
import tempfile
import os
from PIL import Image

RECIPES_URL = reverse("recipe:recipe-list")


# api/recipe/recipes
# api/recipe/recipes/1

def upload_image_url(recipe_id):
    """Return URL for recipe image upload"""
    return reverse("recipe:recipe-upload-image", args=[recipe_id])


def recipe_details_url(recipe_id):
    """Retrieve recipe details"""
    return reverse("recipe:recipe-detail", args=[recipe_id])


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
    default.update(param)
    return Recipe.objects.create(user=user, **default)


class PublicRecipeApiTest(TestCase):
    """Test UnAuthorize access of API"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test Authentication required to access recipe apis"""
        resp = self.client.get(RECIPES_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test Unauthorized recipe api access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="user.ingredient#@test.com",
            name="Ingredient test"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieve list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        resp = self.client.get(RECIPES_URL)

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

        resp = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(len(resp.data), 1)

    def test_recipe_details(self):
        """Test viewing a recipe details """
        recipe = sample_recipe(self.user)
        recipe.tags.add(sample_tag(self.user))
        recipe.ingredients.add(sample_ingredient(self.user))

        url = recipe_details_url(recipe_id=recipe.id)
        resp = self.client.get(url)
        serializer = RecipeDetailsSerializer(recipe, many=False)

        self.assertEqual(resp.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating recipe"""
        payload = {
            'title': 'Test My recipe',
            'time_minutes': 30,
            'price': 10.00,
        }

        resp = self.client.post(RECIPES_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=resp.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """Test creating a recipes with tags"""
        tags1 = sample_tag(user=self.user, name="Vegan")
        tags2 = sample_tag(user=self.user, name="Dessert")

        payload = {
            'title': 'Avocado lime cheesecake ',
            'tags': [tags1.id, tags2.id],
            'time_minutes': 60,
            'price': 80.0
        }

        resp = self.client.post(RECIPES_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.get(id=resp.data['id'])
        tags = recipes.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tags1, tags)
        self.assertIn(tags2, tags)

    def test_create_recipe_with_ingredient(self):
        """Test create Recipe with ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name="Prawns")
        ingredient2 = sample_ingredient(user=self.user, name="N0-Prawns")
        payload = {
            'title': 'Thai prawn red corry ',
            'ingredients': [ingredient2.id, ingredient1.id],
            'time_minutes': 60,
            'price': 80.0
        }

        resp = self.client.post(RECIPES_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=resp.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    def test_partial_update_recipe(self):
        """Test updating a recipe with patch"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(self.user))
        new_tag = sample_tag(self.user, name="Curry")
        payload = {
            'title': 'Paneer Tikka',
            'tags': [new_tag.id]
        }
        url = recipe_details_url(recipe_id=recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        tags = recipe.tags.all()

        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_filter_recipe_by_tags(self):
        """Test returning  recipes by given tag"""
        recipe1 = sample_recipe(self.user, title="Thai vegetable curry")
        recipe2 = sample_recipe(self.user, title="Aubergine with tahini")
        tags1 = sample_tag(user=self.user, name="Vegan")
        tags2 = sample_tag(user=self.user, name="Vegetarian")
        recipe1.tags.add(tags1)
        recipe2.tags.add(tags2)

        recipe3 = sample_recipe(self.user, title="Fish and Chips")
        resp = self.client.get(RECIPES_URL, {'tags': f'{tags1.id},{tags2.id}'})

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)

        self.assertIn(serializer1.data, resp.data)
        self.assertIn(serializer2.data, resp.data)
        self.assertNotIn(serializer3.data, resp.data)

    def test_filter_recipe_by_ingredients(self):
        """Test returning  recipes by given tag"""
        recipe1 = sample_recipe(user=self.user, title="Thai vegetable curry")
        recipe2 = sample_recipe(user=self.user, title="Aubergine with tahini")
        ingredient1 = sample_ingredient(user=self.user, name="Vegan")
        ingredient2 = sample_ingredient(user=self.user, name="Vegetarian")
        recipe1.ingredients.add(ingredient1)
        recipe2.ingredients.add(ingredient2)

        recipe3 = sample_recipe(self.user, title="Fish and Chips")
        resp = self.client.get(RECIPES_URL, {'ingredients': f'{ingredient1.id},{ingredient2.id}'})

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)

        self.assertIn(serializer1.data, resp.data)
        self.assertIn(serializer2.data, resp.data)
        self.assertNotIn(serializer3.data, resp.data)


class RecipeImageUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email='bharat.email@test.com',
            name='bharatpass',
        )
        self.client.force_authenticate(self.user)
        self.recipe = sample_recipe(self.user)

    def tearDown(self):
        print("Tear Down executed...!")
        self.recipe.image.delete()

    def test_upload_image_to_recipe(self):
        """Test uploading a image to recipe"""
        print(f'Recipe Id :{self.recipe.id}')
        url = upload_image_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            resp = self.client.post(url, {'image': ntf}, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('image', resp.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))
        print(f'File path : {self.recipe.image.path}')

    def test_recipe_upload_image_bad_request(self):
        """Test """
        url = upload_image_url(self.recipe.id)
        resp = self.client.post(url, {'image': 'testdata'}, format='multipart')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
