from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_movies),
    path('list/', views.get_all_movies_id_title),
    
    path('<int:movie_pk>/', views.detail_movie),
    path('<int:movie_pk>/like/', views.like_movie),
    path('like/', views.list_liked_movies),
    path('recommend/', views.recommend_movies),
        
    # 데이터 수집용 URL
    path('sample/genres/', views.sample_genres),
    path('sample/movies/', views.sample_movies),
]
