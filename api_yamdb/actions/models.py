from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256, blank=True,
                            default=None)
    slug = models.SlugField(max_length=50, unique=True,
                            blank=True, default=None)


class Category(models.Model):
    name = models.CharField(max_length=256, blank=False,
                            default=None)
    slug = models.SlugField(max_length=50, blank=True,
                            unique=True, default=None)


class Title(models.Model):
    name = models.CharField(max_length=200, default=None,
                            blank=True)
    year = models.IntegerField(
        default=None, blank=True,
        validators=[MinValueValidator(-2000),
                    MaxValueValidator(datetime.date.today().year)])
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    description = models.TextField(default=None)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   related_name='title_genre',
                                   blank=True)
    description = models.TextField(blank=True)



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
    score = models.IntegerField(
        choices=CHOICES,
        default=0,
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
