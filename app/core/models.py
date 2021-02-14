from django.conf import settings
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.db import models
import uuid
import os


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipes"""
    print("[INFO]:-------------------------- recipe_image_file_path --------------")
    print(f'FileName :{filename} , instance : {instance}')
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    print(f'FileName :{filename} , ext : {ext}  UUID {uuid.uuid4()}')

    return os.path.join('uploads/recipe/', filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saved an new users"""
        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(self.db)

        return user

    def create_superuser(self, email, password):
        """Create and saves new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom users model that support using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Tag(models.Model):
    """Tag should be use for a recipe"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=None)

    class Meta:
        db_table = "Tag"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = "Ingredients"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    link = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ingredients = models.ManyToManyField("Ingredient")
    tags = models.ManyToManyField("Tag")

    images = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "recipe"
