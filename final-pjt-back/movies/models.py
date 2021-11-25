from django.core import validators
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

# Create your models here.
class Genre(models.Model):
    tmdb_id = models.PositiveIntegerField(primary_key=True)  # TMDB ID 저장
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    genres = models.ManyToManyField(Genre, related_name='movies')

    tmdb_id = models.PositiveIntegerField(null=True)
    imdb_id = models.CharField(max_length=20, null=True)

    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.CharField(max_length=100)
    release_date = models.DateField()
    adult = models.BooleanField()
    videos = models.JSONField(null=True)
    credits = models.JSONField()

    likers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies')
    
    def __str__(self) -> str:
        return self.title


class Rating(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='movie_ratings'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='user_ratings'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(5)
        ]
    )

    def __str__(self) -> str:
        return f'{self.movie} = {self.rating} by {self.user}'