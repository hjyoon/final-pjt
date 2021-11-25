from django.contrib import admin
from .models import Article, Comment


class ArticleModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user', 
        'content', 
        'movie', 
        'movie_title',
        'rating_info',
        'image',
    )


class CommentModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'article',
        'user',
        'content',
    )


admin.site.register(Article, ArticleModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
