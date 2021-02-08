from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saved an new user"""
        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(self.db)

        return user

    def create_superuser(self, email, password):
        """Create and saves new superuser"""
        print("SuperUsr")
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
