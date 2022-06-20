from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    user = 'u'
    moderator = 'm'
    admin = 'a'

    roles = [
    (user, 'user'),
    (moderator, 'moderator'),
    (admin, 'admin'),
    ]


    bio = models.TextField(
        'Биография',
        blank=True,
        max_length=100,
    )
    role = models.CharField(
        max_length=1,
        blank=False,
        choices=roles,
        default=user,
    )


