from django.contrib import admin
from .models import Genre, Movie, Rating


class GenreModelAdmin(admin.ModelAdmin):
    list_display = (
        'tmdb_id',
        'name',
    )


class MovieModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'poster_path',
        'release_date',
        'tmdb_id',
        'imdb_id',
    )


class RatingModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'movie',
        'rating',
    )


admin.site.register(Genre, GenreModelAdmin)
admin.site.register(Movie, MovieModelAdmin)
admin.site.register(Rating, RatingModelAdmin)
