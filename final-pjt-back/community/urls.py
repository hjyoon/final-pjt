from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_article),
    path('<int:article_pk>/', views.detail_article),
    path('<int:article_pk>/comments/', views.list_comment),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.detail_comment),
]
