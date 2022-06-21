from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    pass


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Review(models.Model):
    CHOICES = [(i, i) for i in range(11)]
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        choices=CHOICES
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
