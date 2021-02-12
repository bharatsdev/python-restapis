from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Tag, Ingredient, Recipe


def sample_user(email="bharat@test.com", password="testpass"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        """Test Creating an users with an email successful.."""
        email = "test@mydata.com"
        password = "password"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for the new users is normalized"""
        email = "test.@EVERYTHINGISDATA.com"
        user = get_user_model().objects.create_user(email, "password123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating users with no email raises errors"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "123post")

    def test_create_new_superuser(self):
        """Test Creating a new super users"""
        user = get_user_model().objects.create_superuser(
            "bharatqq@every.com",
            'test'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag string representation"""
        tag = Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test ingredients string representation """
        ingredients = Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )
        self.assertEqual(str(ingredients), ingredients.name)

    def test_recipe_str(self):
        """Test recipe string representation"""
        recipe = Recipe.objects.create(
            title="Steak an Mushroom sauce",
            time_minutes=5,
            price=5.00,
            user=sample_user()
        )

        self.assertEqual(str(recipe), recipe.title)
