from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model with email as the unique identifier.
    """

    def _create_user(
            self,
            email,
            password,
            is_staff,
            is_superuser,
            **extra_fields):
        """
        Create and return a user with the given email and password.
        """
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        """Create and return a regular user with an email and password."""
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a superuser with an email and password."""
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractUser):
    """
    Custom User model where email is the unique identifier.
    """
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, blank=True, unique=False)
    phone = models.CharField(max_length=20, blank=True, unique=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
