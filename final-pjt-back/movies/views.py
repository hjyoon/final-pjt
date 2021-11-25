from pprint import pprint

from django.db.models import Avg, Count
from django.db.models.query import Prefetch
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import Movie
from .serializers import (
    GenreSerializer,
    MovieListSerializer,
    MovieSimpleListSerializer,
    MovieSerializer,
)
from utils.tmdb import TMDB
from utils.paginator import split_into_pages
from utils.recommender import Recommender


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_movies_id_title(request):
    """
    전체 영화 목록을 반환합니다. 
    
    DB에 있는 모든 영화를 불러오므로 느릴 수 있습니다.
    """
    movies = get_list_or_404(Movie)
    serializer = MovieSimpleListSerializer(movies, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def index_movies(request):
    """
    전체 영화 목록을 페이지 단위로 반환합니다.
    """
    # 평가한 사람 수 추가
    movies = get_list_or_404(
        Movie.objects
            .prefetch_related(Prefetch('likers'))
            .prefetch_related(Prefetch('movie_ratings'))
            .annotate(rating_count=Count('movie_ratings'))
            .annotate(rating_average=Avg('movie_ratings__rating'))
    )
    
    # 좋아요 여부 추가: 기존 방식 활용
    for movie in movies:
        movie.is_liked = movie.likers.filter(pk=request.user.pk).exists()

    # 영화 리스트 페이지 수만큼 쪼개기
    page_object_list = split_into_pages(request, movies)
    serializer = MovieListSerializer(page_object_list, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def detail_movie(request, movie_pk):
    """
    개별 영화의 상세 정보를 반환합니다.
    """
    movie = get_object_or_404(
        Movie.objects
            .filter(pk=movie_pk)
            .prefetch_related(Prefetch('likers'))
            .annotate(likes_count=Count('likers'))
            .prefetch_related(Prefetch('movie_ratings'))
            .annotate(rating_count=Count('movie_ratings'))
            .annotate(rating_average=Avg('movie_ratings__rating'))
    )

    # 좋아요 여부 추가
    movie.is_liked = movie.likers.filter(pk=request.user.pk).exists()
    
    # 평가 여부랑, 평가했을 시 평점 추가
    user_rating = movie.movie_ratings.filter(user=request.user.pk)
    movie.is_rated = user_rating.exists()
    if movie.is_rated:
        movie.my_rating = user_rating.get().rating
    else:
        movie.my_rating = 0

    serializer = MovieSerializer(movie)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
def like_movie(request, movie_pk):
    # 영화를 좋아요한 유저 목록 확인
    movie = get_object_or_404(
        Movie.objects
        .prefetch_related('likers')
        .prefetch_related(Prefetch('movie_ratings'))
        .annotate(rating_average=Avg('movie_ratings__rating')), 
        pk=movie_pk
    )


    # 좋아요 유저 목록에 포함되어 있으면, 좋아요 취소
    if movie.likers.filter(pk=request.user.id).exists():
        # DELETE일 때만 취소 가능
        if request.method == 'DELETE':
            movie.likers.remove(request.user)
            is_liked = False
        else:
            return Response({'detail': 'DELETE method is needed when removing like'}, status.HTTP_405_METHOD_NOT_ALLOWED)

    # 유저 목록에 없으면, 좋아요
    else:
        # POST일 때만 취소 가능
        if request.method == 'POST':
            movie.likers.add(request.user)
            is_liked = True
        else:
            return Response({'detail': 'POST method is needed when adding like'}, status.HTTP_405_METHOD_NOT_ALLOWED)

    return Response({'is_liked': is_liked}, status.HTTP_200_OK)


@api_view(['GET'])
def list_liked_movies(request):
    """
    좋아요한 영화 리스트를 반환합니다.
    """
    liked_movies = get_list_or_404(
        request.user.liked_movies
            .prefetch_related(Prefetch('movie_ratings'))
            .annotate(rating_count=Count('movie_ratings'))
            .annotate(rating_average=Avg('movie_ratings__rating'))
    )
    
    # 좋아요 여부 추가
    for movie in liked_movies:
        movie.is_liked = True

    serializer = MovieListSerializer(liked_movies, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recommend_movies(request):
    """
    장르 목록, 혹은 영화로부터 추천 영화 목록을 만들어 반환합니다.
    """
    # 추천 개수 인자 받기
    if request.query_params.get('count'):
        count = request.query_params.get('count')
        if not (1 <= int(count) <= 10):
            return Response(
                {'detail': 'count should be in range from 1 to 10'},
                status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
            )
    else:
        count = None

    # 영화가 주어질 때는 영화 기반 목록 추천
    if request.query_params.get('source'):
        movie_pk = request.query_params.get('source')
        if request.user.is_authenticated:
            return Recommender(user=request.user, movie_pk=movie_pk, count=count).get_recommendation()
        else:
            return Recommender(movie_pk=movie_pk, count=count).get_recommendation()
    # 그렇지 않을 때는 유저 기반 목록 추천
    elif request.user.is_authenticated:
        if request.user.liked_movies.count() >= 3:
            return Recommender(user=request.user, count=count).get_recommendation()
        else:
            # 좋아요 개수가 3개가 안 되면 
            return Response(
                {'detail': 'At least 3 liked movies are needed for recommendation'},
                status.HTTP_400_BAD_REQUEST
            )
    # 어느 쪽도 아닌 경우 추천 불가
    else:
        return Response(
            {'detail': 'Login is needed for user-optimized recommendation'}, 
            status.HTTP_403_FORBIDDEN
        )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def sample_genres(request):
    """
    TMDB 장르 목록을 수집해 DB에 저장합니다.
    """
    # genre 파일 읽기
    tmdb = TMDB()
    genre_list = tmdb.load_genre_list()

    # 모델에 저장
    serializer = GenreSerializer(data=genre_list, many=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def sample_movies(request):
    """
    TMDB 영화 데이터를 샘플링해 DB에 저장합니다.
    이때 원하는 정보를 추가/삭제하여 데이터를 가공합니다.
    """
    tmdb = TMDB()
    movies = tmdb.get_sample_movies()

    serializer = MovieSerializer(data=movies, many=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
