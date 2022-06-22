from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    bio = models.TextField(
        'Биография',
        blank=True,
        max_length=100,
    )
    role = models.CharField(
        max_length=9,
        blank=False,
        choices=ROLES,
        default=USER,
    )
    email = models.EmailField(
        blank=False,
        max_length=254,
        unique=True,
    )
    
    confirmation_code = models.CharField(
        verbose_name='confirmation code',
        max_length=50,
        blank=True,
        null=True
    )
