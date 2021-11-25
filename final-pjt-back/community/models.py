from django.conf import settings
from django.db import models

from movies.models import Movie, Rating


class Article(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_articles'
    )

    # 게시글 정보
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 관련된 영화 정보 (선택적으로 추가 가능)
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.SET_NULL,
        related_name='movie_articles', 
        null=True,
        blank=True
    )
    movie_title = models.CharField(max_length=100, null=True, blank=True)
    rating = models.PositiveIntegerField(null=True)
    rating_info = models.OneToOneField(
        Rating,
        on_delete=models.SET_NULL,
        related_name='article',
        null=True,
        blank=True
    )
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.content


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.content