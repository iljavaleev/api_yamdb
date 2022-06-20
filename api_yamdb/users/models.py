from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    USER = 'u'
    MODERATOR = 'm'
    ADMIN = 'a'

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
        max_length=1,
        blank=False,
        choices=ROLES,
        default=USER,
    )
    email = models.EmailField(
        blank=False,
        max_length=254,
    )


