from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_ROLES = (
         ('user', 'user'),
         ('moderator', 'moderator'),
         ('admin', 'admin'),
    )
    role = models.CharField(
        choices=USER_ROLES,
        default='user',
        max_length=10,
    )
