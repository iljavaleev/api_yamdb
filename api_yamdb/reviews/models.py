from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import datetime

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50,
                            unique=True)

    class Meta:
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=256, blank=False,)
    slug = models.SlugField(max_length=50, blank=False,
                            unique=True)

    class Meta:
        ordering = ['-id']


class Title(models.Model):
    name = models.CharField(max_length=200, blank=False)
    year = models.IntegerField(
        blank=False,
        validators=[MinValueValidator(-2000),
                    MaxValueValidator(datetime.date.today().year)])
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=False, null=True)
    description = models.TextField(default=None)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   related_name='title_genre',
                                   blank=False)

    class Meta:
        ordering = ['-id']


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)


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
        related_name='reviews',
    )
    score = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(
                10,
                message='Поставьте оценку в диапазоне от 0 до 10'
            )
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='one_review')
        ]


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

    class Meta:
        ordering = ['-id']
