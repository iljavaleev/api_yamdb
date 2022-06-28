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

    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
    )

    role = models.CharField(
        max_length=20,
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

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_user(self):
        return self.role == User.USER
