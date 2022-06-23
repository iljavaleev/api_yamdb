from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=200, default=None)
    slug = models.SlugField(unique=True, default=None)


class Category(models.Model):
    name = models.CharField(max_length=200, default=None)
    slug = models.SlugField(unique=True, default=None)


class Title(models.Model):
    name = models.CharField(max_length=200, default=None)
    year = models.IntegerField(default=None)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   related_name='title_genre',
                                   blank=True)
    description = models.TextField(blank=True)



class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


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
